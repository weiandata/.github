import base64
import contextlib
import io
import unittest
import urllib.error
from pathlib import Path

from operations.waef.models import RepositoryRecord
from operations.waef.upgrade import (
    ADAPTER_PATHS,
    build_upgrade,
    main,
    render_lock,
    render_upgrade_files,
    render_workflow,
    upgrade_repository,
)


OLD_COMMIT = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
NEW_COMMIT = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
CHANGED_RULES = "- WAEF-MUST-001 now requires signed validation evidence."
MIGRATION_STEPS = "1. Regenerate the validation evidence before approval."
ROOT = Path(__file__).resolve().parents[3]


def repository_record():
    return RepositoryRecord(
        name="DCC",
        owner="package-maintainers",
        lifecycle="active",
        profiles=("r-package",),
        expected_waef_check="WAEF Compliance",
        migration_wave=1,
    )


def marked_file(label="project-specific content"):
    return (
        f"before {label}\n"
        "<!-- WAEF:START -->\n"
        "<!-- Generated from WAEF 3.0; do not edit this block directly. -->\n"
        "required governed content\n"
        "<!-- WAEF:END -->\n"
        f"after {label}\n"
    )


def current_files():
    files = {path: marked_file(path) for path in ADAPTER_PATHS}
    files[".waef/waef.lock.yml"] = render_lock(
        "3.0",
        "v3.0",
        OLD_COMMIT,
        ("r-package",),
        "https://github.com/weiandata/DCC/pull/1",
    )
    files[".github/workflows/waef-compliance.yml"] = render_workflow(OLD_COMMIT)
    return files


class FakeUpgradeClient:
    def __init__(
        self, existing_pull=False, unexpected_branch_path=None, wrap_base64=False
    ):
        self.files = current_files()
        self.existing_pull = existing_pull
        self.unexpected_branch_path = unexpected_branch_path
        self.requests = []
        self.blob_count = 0
        self.tree_count = 0
        self.commit_count = 0
        self.wrap_base64 = wrap_base64

    @staticmethod
    def not_found(path):
        return urllib.error.HTTPError(path, 404, "not found", {}, io.BytesIO(b"{}"))

    def request(self, method, path, body=None):
        self.requests.append((method, path, body))
        if method == "GET" and path == "/repos/weiandata/DCC":
            return {"default_branch": "main"}
        if method == "GET" and "/pulls?" in path:
            if self.existing_pull:
                return [
                    {
                        "number": 12,
                        "html_url": "https://github.com/weiandata/DCC/pull/12",
                        "draft": True,
                    }
                ]
            return []
        if method == "GET" and "/git/ref/heads/automation" in path:
            if not self.existing_pull:
                raise self.not_found(path)
            return {"object": {"sha": "cccccccccccccccccccccccccccccccccccccccc"}}
        if method == "GET" and path.endswith("/git/ref/heads/main"):
            return {"object": {"sha": "dddddddddddddddddddddddddddddddddddddddd"}}
        if method == "GET" and "/compare/" in path:
            files = [{"filename": path} for path in ADAPTER_PATHS]
            if self.unexpected_branch_path:
                files.append({"filename": self.unexpected_branch_path})
            return {"status": "ahead", "files": files}
        if method == "GET" and "/contents/" in path:
            file_path = path.split("/contents/", 1)[1].split("?", 1)[0]
            content = base64.b64encode(self.files[file_path].encode()).decode()
            if self.wrap_base64:
                content = "\n".join(
                    content[index : index + 60]
                    for index in range(0, len(content), 60)
                )
            return {"type": "file", "encoding": "base64", "content": content}
        if method == "GET" and "/git/commits/" in path:
            return {"tree": {"sha": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}}
        if method == "POST" and path.endswith("/git/blobs"):
            self.blob_count += 1
            return {"sha": f"{self.blob_count:040x}"}
        if method == "POST" and path.endswith("/git/trees"):
            self.tree_count += 1
            return {"sha": f"{100 + self.tree_count:040x}"}
        if method == "POST" and path.endswith("/git/commits"):
            self.commit_count += 1
            return {"sha": f"{200 + self.commit_count:040x}"}
        if method == "POST" and path.endswith("/git/refs"):
            return {"ref": body["ref"], "object": {"sha": body["sha"]}}
        if method == "PATCH" and "/git/refs/heads/" in path:
            return {"object": {"sha": body["sha"]}}
        if method == "POST" and path.endswith("/pulls"):
            return {
                "number": 13,
                "html_url": "https://github.com/weiandata/DCC/pull/13",
                "draft": True,
            }
        if method == "PATCH" and path.endswith("/pulls/12"):
            return {
                "number": 12,
                "html_url": "https://github.com/weiandata/DCC/pull/12",
                "draft": True,
            }
        raise AssertionError(f"unexpected request: {method} {path}")


class UpgradeTests(unittest.TestCase):
    def test_github_wrapped_base64_content_is_accepted(self):
        pull = upgrade_repository(
            FakeUpgradeClient(wrap_base64=True),
            build_upgrade(
                repository_record(),
                "4.0",
                "v4.0",
                NEW_COMMIT,
                "https://github.com/weiandata/WAEF/blob/v4.0/MIGRATION.md",
                CHANGED_RULES,
                MIGRATION_STEPS,
            ),
        )
        self.assertEqual(13, pull["number"])

    def test_render_lock_contains_exact_release_and_preserved_profiles(self):
        rendered = render_lock(
            "4.0",
            "v4.0",
            NEW_COMMIT,
            ("r-package", "research-repository"),
            "https://github.com/weiandata/DCC/pull/9",
        )
        self.assertIn('version: "4.0"', rendered)
        self.assertIn("tag: v4.0", rendered)
        self.assertIn(f"commit: {NEW_COMMIT}", rendered)
        self.assertIn("  - r-package", rendered)
        self.assertIn("  - research-repository", rendered)
        self.assertTrue(rendered.endswith("\n"))

    def test_render_workflow_uses_exact_reusable_workflow_sha(self):
        rendered = render_workflow(NEW_COMMIT)
        self.assertIn(
            f"uses: weiandata/WAEF/.github/workflows/compliance.yml@{NEW_COMMIT}",
            rendered,
        )
        self.assertIn(f"waef_commit: {NEW_COMMIT}", rendered)
        self.assertIn("on: [pull_request, push]", rendered)
        self.assertNotIn("@main", rendered)

    def test_build_upgrade_rejects_invalid_release_identity(self):
        for version, tag, commit in (
            ("4.0", "4.0", NEW_COMMIT),
            ("4.0", "v4.1", NEW_COMMIT),
            ("4.0", "v4.0", "short"),
            ("v4", "vv4", NEW_COMMIT),
        ):
            with self.subTest(version=version, tag=tag, commit=commit):
                with self.assertRaises(ValueError):
                    build_upgrade(
                        repository_record(),
                        version,
                        tag,
                        commit,
                        "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
                        CHANGED_RULES,
                        MIGRATION_STEPS,
                    )

    def test_upgrade_change_has_one_review_only_purpose_and_migration_link(self):
        change = build_upgrade(
            repository_record(),
            "4.0",
            "v4.0",
            NEW_COMMIT,
            "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
            CHANGED_RULES,
            MIGRATION_STEPS,
        )
        body = change.pull_request_body(
            old_version="3.0", old_tag="v3.0", old_commit=OLD_COMMIT
        )
        self.assertEqual("automation/waef-4.0", change.branch)
        self.assertEqual("chore: upgrade WAEF to 4.0", change.commit_message)
        self.assertIn("v3.0", body)
        self.assertIn(OLD_COMMIT, body)
        self.assertIn("v4.0", body)
        self.assertIn(NEW_COMMIT, body)
        self.assertIn("docs/migration.md", body)
        self.assertIn("Changed MUST rules", body)
        self.assertIn(CHANGED_RULES, body)
        self.assertIn("Migration steps", body)
        self.assertIn(MIGRATION_STEPS, body)
        self.assertIn("repository CI: pending", body)
        self.assertIn("git revert <merged-upgrade-commit-sha>", body)
        self.assertNotIn("auto-merge", body.casefold())

    def test_rendered_upgrade_preserves_project_content_and_updates_markers(self):
        change = build_upgrade(
            repository_record(),
            "4.0",
            "v4.0",
            NEW_COMMIT,
            "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
            CHANGED_RULES,
            MIGRATION_STEPS,
        )
        rendered = render_upgrade_files(
            change,
            current_files(),
            "https://github.com/weiandata/DCC/pull/9",
        )
        self.assertEqual(set(current_files()), set(rendered))
        self.assertIn("before AGENTS.md", rendered["AGENTS.md"])
        self.assertIn("after AGENTS.md", rendered["AGENTS.md"])
        self.assertIn("Generated from WAEF 4.0", rendered["AGENTS.md"])
        self.assertIn("  - r-package", rendered[".waef/waef.lock.yml"])

    def test_new_upgrade_opens_draft_pr_then_records_its_url_without_merge(self):
        client = FakeUpgradeClient()
        change = build_upgrade(
            repository_record(),
            "4.0",
            "v4.0",
            NEW_COMMIT,
            "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
            CHANGED_RULES,
            MIGRATION_STEPS,
        )
        pull = upgrade_repository(client, change)
        self.assertEqual(13, pull["number"])
        pull_posts = [item for item in client.requests if item[0] == "POST" and item[1].endswith("/pulls")]
        self.assertEqual(1, len(pull_posts))
        self.assertTrue(pull_posts[0][2]["draft"])
        self.assertNotIn("merge", pull_posts[0][2])
        self.assertTrue(
            all("/merge" not in path and not (body or {}).get("force") for _, path, body in client.requests)
        )

    def test_existing_upgrade_pr_is_reused(self):
        client = FakeUpgradeClient(existing_pull=True)
        change = build_upgrade(
            repository_record(),
            "4.0",
            "v4.0",
            NEW_COMMIT,
            "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
            CHANGED_RULES,
            MIGRATION_STEPS,
        )
        pull = upgrade_repository(client, change)
        self.assertEqual(12, pull["number"])
        self.assertFalse(
            any(method == "POST" and path.endswith("/pulls") for method, path, _ in client.requests)
        )
        self.assertTrue(
            any(method == "PATCH" and path.endswith("/pulls/12") for method, path, _ in client.requests)
        )

    def test_existing_branch_with_non_waef_changes_is_rejected(self):
        client = FakeUpgradeClient(existing_pull=True, unexpected_branch_path="src/backdoor.R")
        change = build_upgrade(
            repository_record(),
            "4.0",
            "v4.0",
            NEW_COMMIT,
            "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
            CHANGED_RULES,
            MIGRATION_STEPS,
        )
        with self.assertRaisesRegex(ValueError, "contains non-WAEF paths"):
            upgrade_repository(client, change)
        self.assertFalse(
            any(method in {"POST", "PATCH"} for method, _, _ in client.requests)
        )

    def test_upgrade_rejects_missing_obligation_or_migration_summary(self):
        for changed_rules, migration_steps in (
            ("", MIGRATION_STEPS),
            (CHANGED_RULES, "  "),
        ):
            with self.subTest(
                changed_rules=changed_rules, migration_steps=migration_steps
            ):
                with self.assertRaisesRegex(ValueError, "summary"):
                    build_upgrade(
                        repository_record(),
                        "4.0",
                        "v4.0",
                        NEW_COMMIT,
                        "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
                        changed_rules,
                        migration_steps,
                    )

    def test_validate_only_cli_accepts_review_summaries(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result = main(
                [
                    "--version",
                    "4.0",
                    "--tag",
                    "v4.0",
                    "--commit",
                    NEW_COMMIT,
                    "--migration-url",
                    "https://github.com/weiandata/WAEF/blob/v4.0/docs/migration.md",
                    "--changed-rules",
                    CHANGED_RULES,
                    "--migration-steps",
                    MIGRATION_STEPS,
                    "--validate-only",
                ]
            )
        self.assertEqual(0, result)
        self.assertIn('"validated_repositories"', stdout.getvalue())

    def test_dispatch_workflow_verifies_tag_before_upgrade_and_scopes_writes(self):
        workflow = (ROOT / ".github" / "workflows" / "waef-upgrade.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", workflow)
        for field in (
            "version",
            "tag",
            "commit",
            "migration_url",
            "changed_rules",
            "migration_steps",
        ):
            self.assertIn(f"      {field}:", workflow)
        self.assertIn(
            '"refs/tags/${RELEASE_TAG}^{}"',
            workflow,
        )
        for field in (
            "version",
            "tag",
            "commit",
            "migration_url",
            "changed_rules",
            "migration_steps",
        ):
            self.assertNotIn(f'"${{{{ inputs.{field} }}}}"', workflow)
        lines = workflow.splitlines()
        run_blocks = []
        index = 0
        while index < len(lines):
            line = lines[index]
            if line.lstrip().startswith("run:"):
                indent = len(line) - len(line.lstrip())
                block = [line]
                index += 1
                while index < len(lines):
                    next_line = lines[index]
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_line.strip() and next_indent <= indent:
                        break
                    block.append(next_line)
                    index += 1
                run_blocks.append("\n".join(block))
                continue
            index += 1
        self.assertTrue(run_blocks)
        self.assertNotIn("${{ inputs.", "\n".join(run_blocks))
        self.assertIn('--version "${WAEF_VERSION}"', workflow)
        self.assertIn('--changed-rules "${CHANGED_RULES}"', workflow)
        self.assertLess(workflow.index("Test upgrade implementation"), workflow.index("git ls-remote"))
        self.assertLess(workflow.index("git ls-remote"), workflow.rindex("python3 -m operations.waef.upgrade"))
        self.assertIn("repositories: |", workflow)
        self.assertIn("permission-contents: write", workflow)
        self.assertIn("permission-pull-requests: write", workflow)
        self.assertIn("permission-workflows: write", workflow)
        self.assertIn("secrets.WAEF_AUTOMATION_APP_ID", workflow)
        self.assertNotIn("secrets.WAEF_APP_ID", workflow)
        self.assertNotIn("/merge", workflow)
        self.assertNotIn("force:", workflow)


if __name__ == "__main__":
    unittest.main()
