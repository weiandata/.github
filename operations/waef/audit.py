"""Independent daily audit for organization-wide WAEF governance controls."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import re
import urllib.error
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import quote
from zoneinfo import ZoneInfo

from operations.waef.github_client import GitHubClient, decode_file_content
from operations.waef.models import AuditFinding, RepositoryRecord, load_inventory
from operations.waef.render_adapter import render_compliance_workflow


ORGANIZATION = "weiandata"
GOVERNANCE_OWNERS = frozenset(
    {"@weiandata/organization-governance", "@weiandata/waef-maintainers"}
)
REQUIRED_CODEOWNER_PATTERNS = {
    "/AGENTS.md": "AGENTS.md",
    "/.waef/": ".waef/waef.lock.yml",
    "/.github/workflows/waef-compliance.yml": ".github/workflows/waef-compliance.yml",
    "/.github/workflows/": ".github/workflows/release.yml",
    "/CODEOWNERS": "CODEOWNERS",
}
LICENSING_PATTERNS = ("/PROPRIETARY.md", "/LICENSE", "/COPYRIGHT", "/DESCRIPTION")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
EXPIRES_RE = re.compile(r"^\s*expires:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?\s*$", re.MULTILINE)
WORKFLOW_PATH = ".github/workflows/waef-compliance.yml"


@dataclass(frozen=True, slots=True)
class AuditReport:
    date: dt.date
    registered_repositories: int
    compliant_repositories: int
    findings: tuple[AuditFinding, ...]

    def to_json(self) -> str:
        return json.dumps(
            {
                "date": self.date.isoformat(),
                "registered_repositories": self.registered_repositories,
                "compliant_repositories": self.compliant_repositories,
                "findings": [asdict(finding) | {"fingerprint": finding.fingerprint} for finding in self.findings],
            },
            indent=2,
            sort_keys=True,
        ) + "\n"

    def to_markdown(self) -> str:
        lines = [
            "# WAEF organization audit",
            "",
            f"- Date: `{self.date.isoformat()}`",
            f"- Registered repositories: `{self.registered_repositories}`",
            f"- Compliant repositories: `{self.compliant_repositories}`",
            f"- Findings: `{len(self.findings)}`",
            "",
        ]
        if not self.findings:
            lines.append("All registered repositories satisfy the independent WAEF audit.")
        else:
            lines.extend(
                [
                    "| Repository | Rule | Path | Finding | Fingerprint |",
                    "|---|---|---|---|---|",
                ]
            )
            for finding in self.findings:
                message = finding.message.replace("|", "\\|").replace("\n", " ")
                lines.append(
                    f"| `{finding.repository}` | `{finding.rule_id}` | `{finding.path}` | "
                    f"{message} | `{finding.fingerprint}` |"
                )
        return "\n".join(lines) + "\n"


def _finding(repository: str, rule_id: str, path: str, message: str) -> AuditFinding:
    return AuditFinding(repository=repository, rule_id=rule_id, path=path, message=message)


def _read_file(client: GitHubClient, repository: str, branch: str, path: str) -> str | None:
    endpoint = (
        f"/repos/{ORGANIZATION}/{quote(repository, safe='')}/contents/{quote(path, safe='/')}"
        f"?ref={quote(branch, safe='')}"
    )
    try:
        response = client.request("GET", endpoint)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            error.close()
            return None
        raise
    if not isinstance(response, dict) or response.get("type") != "file":
        return None
    if response.get("encoding") != "base64" or not isinstance(response.get("content"), str):
        raise ValueError(f"unexpected contents response for {repository}/{path}")
    return decode_file_content(response["content"])


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_flat_yaml(text: str) -> dict[str, Any]:
    """Parse the small scalar/list subset used by WAEF lock and project files."""

    result: dict[str, Any] = {}
    active_list: str | None = None
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if active_list and re.match(r"^\s+-\s+", raw_line):
            result[active_list].append(_unquote(re.sub(r"^\s+-\s+", "", raw_line)))
            continue
        active_list = None
        if raw_line[:1].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            result[key] = []
            active_list = key
        elif value.startswith("[") and value.endswith("]"):
            result[key] = [_unquote(item) for item in value[1:-1].split(",") if item.strip()]
        elif value.isdigit():
            result[key] = int(value)
        else:
            result[key] = _unquote(value)
    return result


def _validate_agents(repository: str, text: str | None, profiles: Sequence[str]) -> list[AuditFinding]:
    path = "AGENTS.md"
    if text is None:
        return [_finding(repository, "WAEF-AUDIT-AGENTS", path, "AGENTS.md is missing")]
    folded = text.casefold()
    required = [".waef/waef.lock.yml", "stop", "strengthen", "weaken", *profiles]
    missing = [term for term in required if term.casefold() not in folded]
    if missing:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-AGENTS",
                path,
                f"AGENTS.md is missing locked bootstrap terms: {', '.join(missing)}",
            )
        ]
    return []


def _validate_lock(
    repository: str, text: str | None, expected_profiles: Sequence[str]
) -> tuple[dict[str, Any] | None, list[AuditFinding]]:
    path = ".waef/waef.lock.yml"
    if text is None:
        return None, [_finding(repository, "WAEF-AUDIT-LOCK", path, "WAEF lock is missing")]
    lock = _parse_flat_yaml(text)
    required = {"schema", "framework", "version", "repository", "tag", "commit", "profiles", "updated_by"}
    if set(lock) != required:
        return None, [
            _finding(repository, "WAEF-AUDIT-LOCK", path, "WAEF lock fields do not match the exact schema")
        ]
    valid = (
        lock["schema"] == 1
        and lock["framework"] == "WAEF"
        and lock["repository"] == "weiandata/WAEF"
        and isinstance(lock["version"], str)
        and lock["tag"] == f"v{lock['version']}"
        and isinstance(lock["commit"], str)
        and COMMIT_RE.fullmatch(lock["commit"])
        and tuple(lock["profiles"]) == tuple(expected_profiles)
        and isinstance(lock["updated_by"], str)
    )
    if not valid:
        return lock, [
            _finding(
                repository,
                "WAEF-AUDIT-LOCK",
                path,
                "WAEF lock is invalid or its profiles differ from the reviewed inventory",
            )
        ]
    return lock, []


def _validate_project(
    repository: str, text: str | None, expected_owner: str, lifecycle: str
) -> list[AuditFinding]:
    path = ".waef/project.yml"
    if text is None:
        return [_finding(repository, "WAEF-AUDIT-PROJECT", path, "project metadata is missing")]
    project = _parse_flat_yaml(text)
    required = {"name", "owner", "status", "purpose", "risk", "publication", "language"}
    if not required.issubset(project) or project.get("name") != repository:
        return [_finding(repository, "WAEF-AUDIT-PROJECT", path, "project metadata is incomplete")]
    findings = []
    if project.get("owner") != expected_owner:
        findings.append(
            _finding(
                repository,
                "WAEF-AUDIT-PROJECT-OWNER",
                path,
                f"project owner must equal reviewed inventory owner {expected_owner!r}",
            )
        )
    expected_status = "planned" if lifecycle == "planned" else "active"
    if project.get("status") != expected_status:
        findings.append(
            _finding(
                repository,
                "WAEF-AUDIT-PROJECT-STATUS",
                path,
                f"project status must be {expected_status!r}",
            )
        )
    return findings


def _validate_workflow(
    repository: str, text: str | None, lock: dict[str, Any] | None
) -> list[AuditFinding]:
    path = WORKFLOW_PATH
    if text is None:
        return [_finding(repository, "WAEF-AUDIT-WORKFLOW", path, "WAEF workflow caller is missing")]
    if lock is None or not isinstance(lock.get("commit"), str):
        return []
    commit = lock["commit"]
    if text != render_compliance_workflow(commit):
        return [
            _finding(
                repository,
                "WAEF-AUDIT-WORKFLOW",
                path,
                "workflow caller does not use the exact locked WAEF commit",
            )
        ]
    return []


def _codeowner_entries(text: str) -> list[tuple[str, tuple[str, ...]]]:
    entries = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split()
        if len(fields) >= 2:
            entries.append((fields[0], tuple(fields[1:])))
    return entries


def _matching_owners(entries: Sequence[tuple[str, tuple[str, ...]]], target: str) -> tuple[str, ...]:
    normalized_target = target.lstrip("/")
    matches = []
    for pattern, owners in entries:
        normalized_pattern = pattern.lstrip("/")
        matched = (
            normalized_target.startswith(normalized_pattern)
            if normalized_pattern.endswith("/")
            else fnmatch.fnmatchcase(normalized_target, normalized_pattern)
        )
        if matched:
            matches.append(owners)
    return matches[-1] if matches else ()


def _validate_codeowners(repository: str, text: str | None) -> list[AuditFinding]:
    path = "CODEOWNERS"
    if text is None:
        return [_finding(repository, "WAEF-AUDIT-CODEOWNERS", path, "CODEOWNERS is missing")]
    entries = _codeowner_entries(text)
    exact_patterns = {pattern for pattern, _ in entries}
    missing = []
    for required_pattern, representative in REQUIRED_CODEOWNER_PATTERNS.items():
        owners = _matching_owners(entries, representative)
        if required_pattern not in exact_patterns or not GOVERNANCE_OWNERS.intersection(owners):
            missing.append(required_pattern)
    licensing_protected = any(
        pattern in exact_patterns
        and GOVERNANCE_OWNERS.intersection(_matching_owners(entries, pattern))
        for pattern in LICENSING_PATTERNS
    )
    if not licensing_protected:
        missing.append("license/copyright declarations")
    if missing:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-CODEOWNERS",
                path,
                f"governance ownership is missing for: {', '.join(missing)}",
            )
        ]
    return []


def _validate_exceptions(repository: str, text: str | None, today: dt.date) -> list[AuditFinding]:
    if text is None:
        return []
    findings = []
    for raw_expiration in EXPIRES_RE.findall(text):
        try:
            expiration = dt.date.fromisoformat(raw_expiration)
        except ValueError:
            continue
        if expiration <= today:
            findings.append(
                _finding(
                    repository,
                    "WAEF-AUDIT-EXCEPTION-EXPIRED",
                    ".waef/exceptions.yml",
                    f"exception expired on {expiration.isoformat()}",
                )
            )
    return findings


def _resolve_tag(client: GitHubClient, tag: str) -> str:
    response = client.request("GET", f"/repos/{ORGANIZATION}/WAEF/git/ref/tags/{quote(tag, safe='')}")
    target = response.get("object", {}) if isinstance(response, dict) else {}
    for _ in range(5):
        object_type = target.get("type")
        sha = target.get("sha")
        if object_type == "commit" and isinstance(sha, str):
            return sha
        if object_type != "tag" or not isinstance(sha, str):
            break
        annotated = client.request("GET", f"/repos/{ORGANIZATION}/WAEF/git/tags/{sha}")
        target = annotated.get("object", {}) if isinstance(annotated, dict) else {}
    raise ValueError(f"WAEF tag {tag!r} does not resolve to a commit")


def _validate_provenance(
    client: GitHubClient,
    repository: str,
    lock: dict[str, Any] | None,
    tag_cache: dict[str, str],
) -> list[AuditFinding]:
    if lock is None or not isinstance(lock.get("tag"), str) or not isinstance(lock.get("commit"), str):
        return []
    try:
        if lock["tag"] not in tag_cache:
            tag_cache[lock["tag"]] = _resolve_tag(client, lock["tag"])
        resolved = tag_cache[lock["tag"]]
    except (urllib.error.HTTPError, ValueError, KeyError) as error:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-PROVENANCE",
                ".waef/waef.lock.yml",
                f"cannot verify WAEF tag provenance: {error}",
            )
        ]
    if resolved != lock["commit"]:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-PROVENANCE",
                ".waef/waef.lock.yml",
                f"tag {lock['tag']} resolves to {resolved}, not locked commit {lock['commit']}",
            )
        ]
    return []


def _validate_check(
    client: GitHubClient, record: RepositoryRecord, default_branch: str
) -> list[AuditFinding]:
    branch = client.request(
        "GET", f"/repos/{ORGANIZATION}/{quote(record.name, safe='')}/branches/{quote(default_branch, safe='')}"
    )
    sha = branch.get("commit", {}).get("sha") if isinstance(branch, dict) else None
    if not isinstance(sha, str):
        return [_finding(record.name, "WAEF-AUDIT-CHECK", default_branch, "default branch head is unavailable")]
    runs = []
    for page in range(1, 101):
        response = client.request(
            "GET",
            f"/repos/{ORGANIZATION}/{quote(record.name, safe='')}/commits/{sha}"
            f"/check-runs?per_page=100&page={page}",
        )
        page_runs = response.get("check_runs", []) if isinstance(response, dict) else []
        runs.extend(page_runs)
        if len(page_runs) < 100:
            break
    matching = [run for run in runs if run.get("name") == record.expected_waef_check]
    if len(matching) != 1 or matching[0].get("conclusion") != "success":
        return [
            _finding(
                record.name,
                "WAEF-AUDIT-CHECK",
                default_branch,
                f"default branch must have one successful {record.expected_waef_check!r} check",
            )
        ]
    workflow_name = quote(Path(WORKFLOW_PATH).name, safe="")
    workflow_response = client.request(
        "GET",
        f"/repos/{ORGANIZATION}/{quote(record.name, safe='')}/actions/workflows/{workflow_name}"
        f"/runs?branch={quote(default_branch, safe='')}&event=push"
        f"&head_sha={quote(sha, safe='')}&status=completed&per_page=100",
    )
    workflow_runs = (
        workflow_response.get("workflow_runs", [])
        if isinstance(workflow_response, dict)
        else []
    )
    source_runs = [
        run
        for run in workflow_runs
        if run.get("path") == f"{WORKFLOW_PATH}@{default_branch}"
        and run.get("head_branch") == default_branch
        and run.get("head_sha") == sha
        and run.get("event") == "push"
        and run.get("name") == record.expected_waef_check
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
    ]
    if len(source_runs) != 1:
        return [
            _finding(
                record.name,
                "WAEF-AUDIT-CHECK",
                default_branch,
                f"default branch must have one successful {record.expected_waef_check!r} run from {WORKFLOW_PATH}",
            )
        ]
    return []


def _issue_body(finding: AuditFinding, today: dt.date) -> str:
    return (
        f"<!-- waef-audit:{finding.fingerprint} -->\n"
        f"## WAEF daily audit finding\n\n"
        f"- Repository: `{finding.repository}`\n"
        f"- Rule: `{finding.rule_id}`\n"
        f"- Path: `{finding.path}`\n"
        f"- Fingerprint: `{finding.fingerprint}`\n"
        f"- Last observed: `{today.isoformat()}`\n\n"
        f"{finding.message}\n\n"
        "This Issue remains open until an independently verified daily audit no longer reports the finding."
    )


def synchronize_findings(client: GitHubClient, findings: Iterable[AuditFinding], today: dt.date) -> None:
    grouped: dict[str, list[AuditFinding]] = {}
    for finding in findings:
        destination = (
            ".github"
            if finding.rule_id in {"WAEF-AUDIT-UNREGISTERED", "WAEF-AUDIT-REPOSITORY-MISSING"}
            else finding.repository
        )
        grouped.setdefault(destination, []).append(finding)
    for repository, repository_findings in grouped.items():
        endpoint = f"/repos/{ORGANIZATION}/{quote(repository, safe='')}/issues"
        issues = []
        for page in range(1, 101):
            page_issues = client.request("GET", f"{endpoint}?state=open&per_page=100&page={page}")
            if not isinstance(page_issues, list):
                break
            issues.extend(page_issues)
            if len(page_issues) < 100:
                break
        issue_by_fingerprint = {}
        for issue in issues if isinstance(issues, list) else []:
            body = issue.get("body") or ""
            match = re.search(r"<!-- waef-audit:([0-9a-f]{20}) -->", body)
            if match and "pull_request" not in issue:
                issue_by_fingerprint[match.group(1)] = issue
        for finding in repository_findings:
            payload = {
                "title": f"[WAEF audit] {finding.rule_id}: {finding.path}",
                "body": _issue_body(finding, today),
                "labels": ["waef-audit"],
            }
            existing = issue_by_fingerprint.get(finding.fingerprint)
            if existing:
                client.request("PATCH", f"{endpoint}/{existing['number']}", payload)
            else:
                client.request("POST", endpoint, payload)


def _list_organization_repositories(client: GitHubClient) -> list[dict[str, Any]]:
    repositories = []
    for page in range(1, 101):
        response = client.request(
            "GET", f"/orgs/{ORGANIZATION}/repos?type=all&per_page=100&page={page}"
        )
        if not isinstance(response, list):
            raise ValueError("organization repository enumeration must return a list")
        repositories.extend(item for item in response if isinstance(item, dict))
        if len(response) < 100:
            return repositories
    raise ValueError("organization repository enumeration exceeded 10,000 repositories")


def audit_organization(
    client: GitHubClient,
    inventory: Sequence[RepositoryRecord],
    today: dt.date,
    *,
    synchronize_issues: bool = True,
    issue_client: GitHubClient | None = None,
) -> AuditReport:
    """Audit registered repositories independently of their local workflow callers."""

    organization_repositories = _list_organization_repositories(client)
    actual = {
        item["name"]: item
        for item in organization_repositories
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    registered = {record.name: record for record in inventory}
    findings: list[AuditFinding] = []
    for name in sorted(set(actual) - set(registered)):
        findings.append(
            _finding(
                ".github",
                "WAEF-AUDIT-UNREGISTERED",
                "operations/waef/repositories.json",
                f"organization repository {name!r} is not registered",
            )
        )

    tag_cache: dict[str, str] = {}
    for record in inventory:
        metadata = actual.get(record.name)
        if metadata is None:
            findings.append(
                _finding(
                    record.name,
                    "WAEF-AUDIT-REPOSITORY-MISSING",
                    "operations/waef/repositories.json",
                    f"registered repository {record.name!r} was not returned by GitHub",
                )
            )
            continue
        if metadata.get("archived") is True:
            findings.append(
                _finding(
                    record.name,
                    "WAEF-AUDIT-ARCHIVED",
                    "repository",
                    "repository is archived but the reviewed inventory declares it active or planned",
                )
            )
            continue
        default_branch = metadata.get("default_branch")
        if not isinstance(default_branch, str) or not default_branch:
            findings.append(
                _finding(record.name, "WAEF-AUDIT-DEFAULT-BRANCH", "repository", "default branch is missing")
            )
            continue

        agents = _read_file(client, record.name, default_branch, "AGENTS.md")
        lock_text = _read_file(client, record.name, default_branch, ".waef/waef.lock.yml")
        project = _read_file(client, record.name, default_branch, ".waef/project.yml")
        workflow = _read_file(
            client, record.name, default_branch, ".github/workflows/waef-compliance.yml"
        )
        codeowners = _read_file(client, record.name, default_branch, "CODEOWNERS")
        exceptions = _read_file(client, record.name, default_branch, ".waef/exceptions.yml")

        findings.extend(_validate_agents(record.name, agents, record.profiles))
        lock, lock_findings = _validate_lock(record.name, lock_text, record.profiles)
        findings.extend(lock_findings)
        findings.extend(_validate_project(record.name, project, record.owner, record.lifecycle))
        findings.extend(_validate_workflow(record.name, workflow, lock))
        findings.extend(_validate_codeowners(record.name, codeowners))
        findings.extend(_validate_exceptions(record.name, exceptions, today))
        findings.extend(_validate_provenance(client, record.name, lock, tag_cache))
        findings.extend(_validate_check(client, record, default_branch))

    findings.sort(key=lambda item: (item.repository.casefold(), item.rule_id, item.path, item.message))
    findings = list({finding.fingerprint: finding for finding in findings}.values())
    repositories_with_findings = {finding.repository for finding in findings if finding.repository in registered}
    report = AuditReport(
        date=today,
        registered_repositories=len(inventory),
        compliant_repositories=len(inventory) - len(repositories_with_findings),
        findings=tuple(findings),
    )
    if synchronize_issues and findings:
        synchronize_findings(issue_client or client, findings, today)
    return report


def _write_report(path: str | None, content: str) -> None:
    if path:
        Path(path).write_text(content, encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--inventory",
        default=str(Path(__file__).with_name("repositories.json")),
        help="path to the reviewed repository inventory",
    )
    parser.add_argument(
        "--today",
        type=dt.date.fromisoformat,
        default=dt.datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).date(),
    )
    parser.add_argument("--no-sync-issues", action="store_true")
    parser.add_argument("--json-output")
    parser.add_argument("--markdown-output")
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        parser.error("GH_TOKEN or GITHUB_TOKEN is required")
    synchronize_issues = not args.no_sync_issues
    issue_token = os.environ.get("WAEF_ISSUE_TOKEN")
    if synchronize_issues and not issue_token:
        parser.error("WAEF_ISSUE_TOKEN is required unless --no-sync-issues is used")
    report = audit_organization(
        GitHubClient(token),
        load_inventory(args.inventory),
        args.today,
        synchronize_issues=synchronize_issues,
        issue_client=GitHubClient(issue_token) if issue_token else None,
    )
    json_report = report.to_json()
    markdown_report = report.to_markdown()
    _write_report(args.json_output, json_report)
    _write_report(args.markdown_output, markdown_report)
    if args.github_summary:
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if not summary:
            parser.error("GITHUB_STEP_SUMMARY is required with --github-summary")
        with Path(summary).open("a", encoding="utf-8") as handle:
            handle.write(markdown_report)
    print(json_report, end="")
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
