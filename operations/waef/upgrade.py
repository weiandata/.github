"""Open review-only WAEF upgrade Pull Requests through GitHub Git data APIs."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import quote

from operations.waef.audit import _parse_flat_yaml
from operations.waef.github_client import GitHubClient, decode_file_content
from operations.waef.models import RepositoryRecord, load_inventory
from operations.waef.render_adapter import render_compliance_workflow, update_generated_version


ORGANIZATION = "weiandata"
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
PROFILE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PR_URL_RE = re.compile(
    r"^https://github\.com/weiandata/[A-Za-z0-9._-]+/pull/[1-9][0-9]*$"
)
ADAPTER_PATHS = (
    "AGENTS.md",
    "CONTRIBUTING.md",
    ".github/ISSUE_TEMPLATE/waef-change.md",
    ".github/pull_request_template.md",
    ".waef/templates/VALIDATION_REPORT_TEMPLATE.md",
    ".waef/templates/DESIGN_DOC_TEMPLATE.md",
    ".waef/templates/ADR_TEMPLATE.md",
    ".waef/templates/RELEASE_TEMPLATE.md",
)
LOCK_PATH = ".waef/waef.lock.yml"
WORKFLOW_PATH = ".github/workflows/waef-compliance.yml"
UPGRADE_PATHS = (LOCK_PATH, WORKFLOW_PATH, *ADAPTER_PATHS)


@dataclass(frozen=True, slots=True)
class UpgradeChange:
    repository: RepositoryRecord
    version: str
    tag: str
    commit: str
    migration_url: str
    changed_rules: str
    migration_steps: str
    branch: str
    commit_message: str
    pull_request_title: str

    def pull_request_body(self, *, old_version: str, old_tag: str, old_commit: str) -> str:
        major_changed = old_version.split(".", 1)[0] != self.version.split(".", 1)[0]
        approvals = (
            "Project Owner and WAEF Maintainer approval are required (MAJOR upgrade)."
            if major_changed
            else "Project Owner approval is required."
        )
        return (
            "## WAEF reviewed upgrade\n\n"
            f"- Repository: `{self.repository.name}`\n"
            f"- Old pin: `{old_version}` / `{old_tag}` / `{old_commit}`\n"
            f"- New pin: `{self.version}` / `{self.tag}` / `{self.commit}`\n"
            f"- Migration instructions: {self.migration_url}\n\n"
            "### Changed MUST rules\n\n"
            f"{self.changed_rules}\n\n"
            "### Migration steps\n\n"
            f"{self.migration_steps}\n\n"
            "Automation changes only WAEF-owned adapters and exact pins; it does not approve semantic changes.\n\n"
            "### Validation results\n\n"
            "- release tag/SHA preflight: passed by the dispatch workflow\n"
            "- WAEF compliance: pending\n"
            "- repository CI: pending\n\n"
            "### Approval requirements\n\n"
            f"{approvals} The Pull Request must remain unmerged until required checks and review are green.\n\n"
            "### Rollback\n\n"
            "If regression is found after merge, open a reviewed rollback Pull Request using:\n\n"
            "```bash\n"
            "git revert <merged-upgrade-commit-sha>\n"
            "```\n"
        )


def _validate_release(version: str, tag: str, commit: str) -> None:
    if not VERSION_RE.fullmatch(version):
        raise ValueError("version must use MAJOR.MINOR")
    if tag != f"v{version}":
        raise ValueError("tag must equal 'v' plus version")
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("commit must be a full lowercase 40-character SHA")


def build_upgrade(
    repo: RepositoryRecord,
    version: str,
    tag: str,
    commit: str,
    migration_url: str,
    changed_rules: str,
    migration_steps: str,
) -> UpgradeChange:
    _validate_release(version, tag, commit)
    if not migration_url.startswith("https://github.com/weiandata/WAEF/"):
        raise ValueError("migration_url must point to the private weiandata/WAEF repository")
    changed_rules = changed_rules.strip()
    migration_steps = migration_steps.strip()
    if not changed_rules or not migration_steps:
        raise ValueError("changed-rules and migration-steps summary values are required")
    return UpgradeChange(
        repository=repo,
        version=version,
        tag=tag,
        commit=commit,
        migration_url=migration_url,
        changed_rules=changed_rules,
        migration_steps=migration_steps,
        branch=f"automation/waef-{version}",
        commit_message=f"chore: upgrade WAEF to {version}",
        pull_request_title=f"chore: upgrade WAEF to {version}",
    )


def render_lock(
    version: str,
    tag: str,
    commit: str,
    profiles: Sequence[str],
    updated_by: str,
) -> str:
    _validate_release(version, tag, commit)
    if not profiles or len(profiles) != len(set(profiles)) or not all(
        PROFILE_RE.fullmatch(profile) for profile in profiles
    ):
        raise ValueError("profiles must be unique WAEF profile identifiers")
    if not PR_URL_RE.fullmatch(updated_by):
        raise ValueError("updated_by must be a weiandata Pull Request URL")
    profile_lines = "\n".join(f"  - {profile}" for profile in profiles)
    return (
        "schema: 1\n"
        "framework: WAEF\n"
        f'version: "{version}"\n'
        "repository: weiandata/WAEF\n"
        f"tag: {tag}\n"
        f"commit: {commit}\n"
        "profiles:\n"
        f"{profile_lines}\n"
        f"updated_by: {updated_by}\n"
    )


def render_workflow(commit: str) -> str:
    return render_compliance_workflow(commit)


def _current_lock(files: Mapping[str, str]) -> dict[str, Any]:
    if LOCK_PATH not in files:
        raise ValueError(f"missing required upgrade file {LOCK_PATH}")
    lock = _parse_flat_yaml(files[LOCK_PATH])
    required = {"version", "tag", "commit", "profiles", "updated_by"}
    if not required.issubset(lock):
        raise ValueError("current WAEF lock is incomplete")
    return lock


def render_upgrade_files(
    change: UpgradeChange, current: Mapping[str, str], updated_by: str
) -> dict[str, str]:
    missing = sorted(set(UPGRADE_PATHS) - set(current))
    if missing:
        raise ValueError(f"missing required upgrade adapters: {', '.join(missing)}")
    lock = _current_lock(current)
    if tuple(lock["profiles"]) != change.repository.profiles:
        raise ValueError("current lock profiles differ from the reviewed repository inventory")
    rendered = dict(current)
    rendered[LOCK_PATH] = render_lock(
        change.version,
        change.tag,
        change.commit,
        change.repository.profiles,
        updated_by,
    )
    rendered[WORKFLOW_PATH] = render_workflow(change.commit)
    for path in ADAPTER_PATHS:
        rendered[path] = update_generated_version(current[path], change.version)
    return rendered


def _read_file(client: GitHubClient, repository: str, reference: str, path: str) -> str:
    endpoint = (
        f"/repos/{ORGANIZATION}/{quote(repository, safe='')}/contents/{quote(path, safe='/')}"
        f"?ref={quote(reference, safe='')}"
    )
    response = client.request("GET", endpoint)
    if not isinstance(response, dict) or response.get("type") != "file":
        raise ValueError(f"expected file at {repository}/{path}")
    if response.get("encoding") != "base64" or not isinstance(response.get("content"), str):
        raise ValueError(f"unexpected contents encoding at {repository}/{path}")
    return decode_file_content(response["content"])


def _get_ref(client: GitHubClient, repository: str, ref: str) -> dict[str, Any] | None:
    try:
        return client.request(
            "GET", f"/repos/{ORGANIZATION}/{quote(repository, safe='')}/git/ref/{quote(ref, safe='/')}"
        )
    except urllib.error.HTTPError as error:
        if error.code == 404:
            error.close()
            return None
        raise


def _commit_files(
    client: GitHubClient,
    repository: str,
    parent_sha: str,
    files: Mapping[str, str],
    message: str,
) -> tuple[str, str]:
    encoded_repository = quote(repository, safe="")
    parent = client.request(
        "GET", f"/repos/{ORGANIZATION}/{encoded_repository}/git/commits/{parent_sha}"
    )
    base_tree = parent.get("tree", {}).get("sha") if isinstance(parent, dict) else None
    if not isinstance(base_tree, str):
        raise ValueError(f"cannot resolve parent tree for {repository}@{parent_sha}")
    entries = []
    for path in sorted(files):
        blob = client.request(
            "POST",
            f"/repos/{ORGANIZATION}/{encoded_repository}/git/blobs",
            {"content": files[path], "encoding": "utf-8"},
        )
        entries.append(
            {"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]}
        )
    tree = client.request(
        "POST",
        f"/repos/{ORGANIZATION}/{encoded_repository}/git/trees",
        {"base_tree": base_tree, "tree": entries},
    )
    commit = client.request(
        "POST",
        f"/repos/{ORGANIZATION}/{encoded_repository}/git/commits",
        {"message": message, "tree": tree["sha"], "parents": [parent_sha]},
    )
    return commit["sha"], tree["sha"]


def _write_branch(
    client: GitHubClient,
    repository: str,
    branch: str,
    commit_sha: str,
    exists: bool,
) -> None:
    encoded_repository = quote(repository, safe="")
    if exists:
        client.request(
            "PATCH",
            f"/repos/{ORGANIZATION}/{encoded_repository}/git/refs/heads/{quote(branch, safe='')}",
            {"sha": commit_sha, "force": False},
        )
    else:
        client.request(
            "POST",
            f"/repos/{ORGANIZATION}/{encoded_repository}/git/refs",
            {"ref": f"refs/heads/{branch}", "sha": commit_sha},
        )


def upgrade_repository(client: GitHubClient, change: UpgradeChange) -> dict[str, Any]:
    """Create or update one review-only upgrade Pull Request without merging."""

    repository = change.repository.name
    encoded_repository = quote(repository, safe="")
    metadata = client.request("GET", f"/repos/{ORGANIZATION}/{encoded_repository}")
    default_branch = metadata.get("default_branch") if isinstance(metadata, dict) else None
    if not isinstance(default_branch, str) or not default_branch:
        raise ValueError(f"repository {repository} has no default branch")

    pulls = client.request(
        "GET",
        f"/repos/{ORGANIZATION}/{encoded_repository}/pulls?state=open"
        f"&head={quote(f'{ORGANIZATION}:{change.branch}', safe='')}&base={quote(default_branch, safe='')}",
    )
    if not isinstance(pulls, list):
        raise ValueError("Pull Request query must return a list")
    if len(pulls) > 1:
        raise ValueError(f"multiple open upgrade Pull Requests exist for {repository}")
    existing_pull = pulls[0] if pulls else None

    branch_ref = _get_ref(client, repository, f"heads/{change.branch}")
    default_ref = _get_ref(client, repository, f"heads/{default_branch}")
    if default_ref is None:
        raise ValueError(f"default branch ref is missing for {repository}")
    if branch_ref:
        comparison = client.request(
            "GET",
            f"/repos/{ORGANIZATION}/{encoded_repository}/compare/"
            f"{quote(default_branch, safe='')}...{quote(change.branch, safe='')}",
        )
        compared_files = comparison.get("files", []) if isinstance(comparison, dict) else []
        unexpected = sorted(
            item.get("filename")
            for item in compared_files
            if isinstance(item, dict)
            and isinstance(item.get("filename"), str)
            and item["filename"] not in UPGRADE_PATHS
        )
        if unexpected:
            raise ValueError(
                f"upgrade branch for {repository} contains non-WAEF paths: {', '.join(unexpected)}"
            )
    source_ref = change.branch if branch_ref else default_branch
    source_sha = (
        branch_ref.get("object", {}).get("sha")
        if branch_ref
        else default_ref.get("object", {}).get("sha")
    )
    if not isinstance(source_sha, str):
        raise ValueError(f"source branch SHA is missing for {repository}")

    current = {path: _read_file(client, repository, source_ref, path) for path in UPGRADE_PATHS}
    base_lock = _parse_flat_yaml(_read_file(client, repository, default_branch, LOCK_PATH))
    if not {"version", "tag", "commit"}.issubset(base_lock):
        raise ValueError(f"default-branch WAEF lock is incomplete for {repository}")
    current_lock = _current_lock(current)
    existing_url = existing_pull.get("html_url") if existing_pull else None
    initial_updated_by = existing_url or current_lock["updated_by"]
    rendered = render_upgrade_files(change, current, initial_updated_by)
    changes = {path: content for path, content in rendered.items() if content != current[path]}
    if changes:
        source_sha, _ = _commit_files(
            client, repository, source_sha, changes, change.commit_message
        )
        _write_branch(client, repository, change.branch, source_sha, branch_ref is not None)
    elif branch_ref is None:
        raise ValueError(f"upgrade for {repository} has no file changes")

    body = change.pull_request_body(
        old_version=str(base_lock["version"]),
        old_tag=str(base_lock["tag"]),
        old_commit=str(base_lock["commit"]),
    )
    if existing_pull:
        return client.request(
            "PATCH",
            f"/repos/{ORGANIZATION}/{encoded_repository}/pulls/{existing_pull['number']}",
            {"title": change.pull_request_title, "body": body, "base": default_branch},
        )

    pull = client.request(
        "POST",
        f"/repos/{ORGANIZATION}/{encoded_repository}/pulls",
        {
            "title": change.pull_request_title,
            "body": body,
            "head": change.branch,
            "base": default_branch,
            "draft": True,
        },
    )
    pull_url = pull.get("html_url") if isinstance(pull, dict) else None
    if not isinstance(pull_url, str) or not PR_URL_RE.fullmatch(pull_url):
        raise ValueError(f"GitHub did not return a valid Pull Request URL for {repository}")

    final_lock = render_lock(
        change.version,
        change.tag,
        change.commit,
        change.repository.profiles,
        pull_url,
    )
    if final_lock != rendered[LOCK_PATH]:
        final_sha, _ = _commit_files(
            client,
            repository,
            source_sha,
            {LOCK_PATH: final_lock},
            f"chore: record WAEF upgrade PR for {change.version}",
        )
        _write_branch(client, repository, change.branch, final_sha, True)
    return pull


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--migration-url", required=True)
    parser.add_argument("--changed-rules", required=True)
    parser.add_argument("--migration-steps", required=True)
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument(
        "--inventory", default=str(Path(__file__).with_name("repositories.json"))
    )
    args = parser.parse_args(argv)
    repositories = load_inventory(args.inventory)
    changes = [
        build_upgrade(
            repository,
            args.version,
            args.tag,
            args.commit,
            args.migration_url,
            args.changed_rules,
            args.migration_steps,
        )
        for repository in repositories
    ]
    if args.validate_only:
        print(json.dumps({"validated_repositories": [item.repository.name for item in changes]}))
        return 0
    token = os.environ.get("WAEF_UPGRADE_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        parser.error("WAEF_UPGRADE_TOKEN or GH_TOKEN is required")
    client = GitHubClient(token)
    results = []
    for change in changes:
        pull = upgrade_repository(client, change)
        results.append(
            {
                "repository": change.repository.name,
                "number": pull.get("number"),
                "url": pull.get("html_url"),
                "draft": pull.get("draft"),
            }
        )
    print(json.dumps({"upgrades": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
