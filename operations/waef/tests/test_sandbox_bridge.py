import copy
import datetime as dt
import io
import unittest
from contextlib import redirect_stderr

from operations.waef.models import APPROVED_REPOSITORIES
from operations.waef.sandbox_bridge import (
    CANDIDATE_COMMIT,
    SANDBOX_REPOSITORY,
    audit_candidate_sandbox,
    main,
    render_candidate_workflow,
)
from operations.waef.tests.test_audit import FakeGitHubClient, load_fixture


TODAY = dt.date(2026, 7, 15)


def candidate_fixture():
    fixture = copy.deepcopy(load_fixture("compliant-repository.json"))
    fixture["repository"] = {
        "name": SANDBOX_REPOSITORY,
        "archived": False,
        "default_branch": "main",
    }
    fixture["files"]["AGENTS.md"] = (
        "Read `.waef/waef.lock.yml` and the exact locked WAEF source before work. "
        "Profiles: planned-project. Stop if the source cannot be verified. "
        "Project rules may strengthen but never weaken WAEF.\n"
    )
    fixture["files"][".waef/waef.lock.yml"] = (
        "schema: 1\n"
        "framework: WAEF\n"
        'version: "4.0"\n'
        "repository: weiandata/WAEF\n"
        "tag: v4.0\n"
        f"commit: {CANDIDATE_COMMIT}\n"
        "profiles:\n"
        "  - planned-project\n"
        "updated_by: https://github.com/weiandata/waef-compliance-sandbox/pull/1\n"
    )
    fixture["files"][".waef/project.yml"] = (
        f"name: {SANDBOX_REPOSITORY}\n"
        "owner: sandbox-validation\n"
        "status: planned\n"
        "purpose: Validate the WAEF candidate bridge\n"
        "risk: controlled\n"
        "publication: prohibited\n"
        "language: Python\n"
    )
    fixture["files"][".github/workflows/waef-compliance.yml"] = (
        render_candidate_workflow()
    )
    fixture["waef_tags"] = {}
    return fixture


class CandidateSandboxBridgeTests(unittest.TestCase):
    def test_production_allowlist_remains_exactly_eleven_without_sandbox(self):
        self.assertEqual(11, len(APPROVED_REPOSITORIES))
        self.assertNotIn(SANDBOX_REPOSITORY, APPROVED_REPOSITORIES)

    def test_clean_candidate_push_audits_only_sandbox_without_tag_lookup(self):
        client = FakeGitHubClient(
            candidate_fixture(),
            organization_repositories=[
                {"name": "DCC", "archived": False, "default_branch": "main"},
                {"name": SANDBOX_REPOSITORY, "archived": False, "default_branch": "main"},
            ],
        )

        report = audit_candidate_sandbox(
            client, None, TODAY, synchronize_issues=False
        )

        self.assertEqual(1, report.registered_repositories)
        self.assertEqual(1, report.compliant_repositories)
        self.assertEqual((), report.findings)
        self.assertEqual(0, client.tag_reads)
        self.assertFalse(
            any(path.startswith("/orgs/") for _, path, _ in client.requests)
        )
        self.assertTrue(
            all(
                "/repos/weiandata/waef-compliance-sandbox/" in path
                for _, path, _ in client.requests
            )
        )

    def test_another_lock_sha_is_a_candidate_bridge_finding(self):
        fixture = candidate_fixture()
        fixture["files"][".waef/waef.lock.yml"] = fixture["files"][
            ".waef/waef.lock.yml"
        ].replace(CANDIDATE_COMMIT, "a" * 40)
        client = FakeGitHubClient(fixture)

        report = audit_candidate_sandbox(
            client, None, TODAY, synchronize_issues=False
        )

        self.assertIn(
            "WAEF-BRIDGE-CANDIDATE", {finding.rule_id for finding in report.findings}
        )
        self.assertEqual(0, client.tag_reads)

    def test_candidate_workflow_must_be_exact(self):
        fixture = candidate_fixture()
        fixture["files"][".github/workflows/waef-compliance.yml"] += "# extra\n"

        report = audit_candidate_sandbox(
            FakeGitHubClient(fixture), None, TODAY, synchronize_issues=False
        )

        self.assertIn(
            "WAEF-AUDIT-WORKFLOW", {finding.rule_id for finding in report.findings}
        )

    def test_cli_has_no_repository_or_candidate_sha_override(self):
        for arguments in (
            ["audit", "--repository", "DCC", "--no-sync-issues"],
            ["audit", "--candidate-commit", "a" * 40, "--no-sync-issues"],
        ):
            with self.subTest(arguments=arguments), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    main(arguments)
                self.assertEqual(2, raised.exception.code)

    def test_branch_ref_is_used_for_negative_scenario_evidence(self):
        fixture = candidate_fixture()
        branch = "sandbox/deleted-caller"
        del fixture["files"][".github/workflows/waef-compliance.yml"]
        fixture["workflow_runs"][0]["path"] = (
            f".github/workflows/waef-compliance.yml@{branch}"
        )
        fixture["workflow_runs"][0]["head_branch"] = branch
        client = FakeGitHubClient(fixture)

        report = audit_candidate_sandbox(
            client, None, TODAY, ref=branch, synchronize_issues=False
        )

        self.assertIn(
            "WAEF-AUDIT-WORKFLOW", {finding.rule_id for finding in report.findings}
        )
        content_paths = [path for _, path, _ in client.requests if "/contents/" in path]
        self.assertTrue(content_paths)
        self.assertTrue(all("ref=sandbox%2Fdeleted-caller" in path for path in content_paths))
        run_path = next(
            path for _, path, _ in client.requests if "/actions/workflows/" in path
        )
        self.assertIn("branch=sandbox%2Fdeleted-caller", run_path)

    def test_repeated_finding_creates_once_then_updates_once(self):
        fixture = candidate_fixture()
        del fixture["files"]["AGENTS.md"]
        first_issue_client = FakeGitHubClient(fixture)

        first_report = audit_candidate_sandbox(
            FakeGitHubClient(fixture), first_issue_client, TODAY
        )

        self.assertEqual(1, len(first_issue_client.writes))
        self.assertEqual("POST", first_issue_client.writes[0][0])
        marker = f"<!-- waef-audit:{first_report.findings[0].fingerprint} -->"
        self.assertIn(marker, first_issue_client.writes[0][2]["body"])

        fixture["issues"] = [{"number": 7, "body": marker, "state": "open"}]
        second_issue_client = FakeGitHubClient(fixture)
        audit_candidate_sandbox(FakeGitHubClient(fixture), second_issue_client, TODAY)

        self.assertEqual(1, len(second_issue_client.writes))
        self.assertEqual(
            ("PATCH", f"/repos/weiandata/{SANDBOX_REPOSITORY}/issues/7"),
            second_issue_client.writes[0][:2],
        )


if __name__ == "__main__":
    unittest.main()
