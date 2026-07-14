import base64
import copy
import datetime as dt
import io
import json
import unittest
import urllib.error
from pathlib import Path
from urllib.parse import unquote

from operations.waef.audit import audit_organization
from operations.waef.models import RepositoryRecord


FIXTURES = Path(__file__).with_name("fixtures")
ROOT = Path(__file__).resolve().parents[3]
TODAY = dt.date(2026, 7, 15)


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def record(**changes):
    values = {
        "name": "DCC",
        "owner": "package-maintainers",
        "lifecycle": "active",
        "profiles": ("r-package",),
        "expected_waef_check": "WAEF Compliance",
        "migration_wave": 1,
    }
    values.update(changes)
    return RepositoryRecord(**values)


class FakeGitHubClient:
    def __init__(self, fixture, organization_repositories=None):
        self.fixture = copy.deepcopy(fixture)
        self.organization_repositories = (
            [self.fixture["repository"]]
            if organization_repositories is None
            else organization_repositories
        )
        self.writes = []
        self.tag_reads = 0

    @staticmethod
    def not_found(path):
        return urllib.error.HTTPError(
            path,
            404,
            "not found",
            {},
            io.BytesIO(b'{"message":"not found"}'),
        )

    def request(self, method, path, body=None):
        if method == "GET" and path.startswith("/orgs/weiandata/repos?"):
            return self.organization_repositories
        if method == "GET" and "/contents/" in path:
            encoded_path = path.split("/contents/", 1)[1].split("?", 1)[0]
            file_path = unquote(encoded_path)
            if file_path not in self.fixture["files"]:
                raise self.not_found(path)
            content = base64.b64encode(self.fixture["files"][file_path].encode()).decode()
            return {"type": "file", "encoding": "base64", "content": content}
        if method == "GET" and "/branches/" in path:
            return {"commit": {"sha": self.fixture["head_sha"]}}
        if method == "GET" and "/check-runs?" in path:
            return {"check_runs": self.fixture["check_runs"]}
        if method == "GET" and "/git/ref/tags/" in path:
            self.tag_reads += 1
            tag = unquote(path.rsplit("/", 1)[1])
            if tag not in self.fixture["waef_tags"]:
                raise self.not_found(path)
            return {"object": self.fixture["waef_tags"][tag]}
        if method == "GET" and "/git/tags/" in path:
            sha = path.rsplit("/", 1)[1]
            return self.fixture.get("annotated_tags", {})[sha]
        if method == "GET" and "/issues?" in path:
            return self.fixture["issues"]
        if method in {"POST", "PATCH"} and "/issues" in path:
            self.writes.append((method, path, body))
            return {"number": 99, **(body or {})}
        raise AssertionError(f"unexpected request: {method} {path}")


class AuditTests(unittest.TestCase):
    def test_compliant_repository_has_no_findings(self):
        report = audit_organization(
            FakeGitHubClient(load_fixture("compliant-repository.json")),
            [record()],
            TODAY,
        )
        self.assertEqual((), report.findings)
        self.assertEqual(1, report.compliant_repositories)

    def test_drifted_repository_reports_every_required_control(self):
        report = audit_organization(
            FakeGitHubClient(load_fixture("drifted-repository.json")),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        rule_ids = {finding.rule_id for finding in report.findings}
        self.assertTrue(
            {
                "WAEF-AUDIT-AGENTS",
                "WAEF-AUDIT-PROJECT-OWNER",
                "WAEF-AUDIT-WORKFLOW",
                "WAEF-AUDIT-CODEOWNERS",
                "WAEF-AUDIT-CHECK",
                "WAEF-AUDIT-PROVENANCE",
                "WAEF-AUDIT-EXCEPTION-EXPIRED",
            }.issubset(rule_ids)
        )

    def test_missing_lock_and_project_metadata_are_distinct_findings(self):
        fixture = load_fixture("compliant-repository.json")
        del fixture["files"][".waef/waef.lock.yml"]
        del fixture["files"][".waef/project.yml"]
        report = audit_organization(
            FakeGitHubClient(fixture), [record()], TODAY, synchronize_issues=False
        )
        self.assertIn("WAEF-AUDIT-LOCK", {finding.rule_id for finding in report.findings})
        self.assertIn("WAEF-AUDIT-PROJECT", {finding.rule_id for finding in report.findings})

    def test_unregistered_repository_is_an_organization_finding(self):
        fixture = load_fixture("compliant-repository.json")
        repositories = [fixture["repository"], {"name": "surprise", "archived": False}]
        report = audit_organization(
            FakeGitHubClient(fixture, repositories),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        finding = next(
            item for item in report.findings if item.rule_id == "WAEF-AUDIT-UNREGISTERED"
        )
        self.assertEqual(".github", finding.repository)
        self.assertIn("surprise", finding.message)

    def test_archived_repository_gets_one_finding_without_file_cascade(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["repository"]["archived"] = True
        fixture["files"] = {}
        report = audit_organization(
            FakeGitHubClient(fixture), [record()], TODAY, synchronize_issues=False
        )
        self.assertEqual(["WAEF-AUDIT-ARCHIVED"], [item.rule_id for item in report.findings])

    def test_missing_registered_repository_reports_issue_centrally(self):
        fixture = load_fixture("compliant-repository.json")
        read_client = FakeGitHubClient(fixture, [])
        issue_client = FakeGitHubClient(fixture)
        report = audit_organization(
            read_client, [record()], TODAY, issue_client=issue_client
        )
        self.assertEqual(0, report.compliant_repositories)
        self.assertEqual("WAEF-AUDIT-REPOSITORY-MISSING", report.findings[0].rule_id)
        self.assertEqual("/repos/weiandata/.github/issues", issue_client.writes[0][1])

    def test_annotated_tag_is_peeled_before_provenance_comparison(self):
        fixture = load_fixture("compliant-repository.json")
        tag_object = "cccccccccccccccccccccccccccccccccccccccc"
        fixture["waef_tags"]["v4.0"] = {"type": "tag", "sha": tag_object}
        fixture["annotated_tags"] = {
            tag_object: {
                "object": {
                    "type": "commit",
                    "sha": "993ef1e41306146f62881106ab17cae2e23162f5",
                }
            }
        }
        report = audit_organization(
            FakeGitHubClient(fixture), [record()], TODAY, synchronize_issues=False
        )
        self.assertEqual((), report.findings)

    def test_same_waef_tag_is_resolved_only_once_per_audit(self):
        fixture = load_fixture("compliant-repository.json")
        repositories = [
            fixture["repository"],
            {"name": "WFC", "archived": False, "default_branch": "main"},
        ]
        client = FakeGitHubClient(fixture, repositories)
        audit_organization(
            client,
            [record(), record(name="WFC")],
            TODAY,
            synchronize_issues=False,
        )
        self.assertEqual(1, client.tag_reads)

    def test_repeated_finding_updates_existing_issue_by_fingerprint(self):
        fixture = load_fixture("compliant-repository.json")
        del fixture["files"]["AGENTS.md"]
        first_client = FakeGitHubClient(fixture)
        first_report = audit_organization(first_client, [record()], TODAY)
        self.assertEqual(1, len(first_client.writes))
        self.assertEqual("POST", first_client.writes[0][0])
        marker = f"<!-- waef-audit:{first_report.findings[0].fingerprint} -->"
        self.assertIn(marker, first_client.writes[0][2]["body"])

        fixture["issues"] = [{"number": 7, "body": marker, "state": "open"}]
        second_client = FakeGitHubClient(fixture)
        audit_organization(second_client, [record()], TODAY)
        self.assertEqual(1, len(second_client.writes))
        self.assertEqual(("PATCH", "/repos/weiandata/DCC/issues/7"), second_client.writes[0][:2])

    def test_issue_writes_can_use_a_separately_scoped_client(self):
        fixture = load_fixture("compliant-repository.json")
        del fixture["files"]["AGENTS.md"]
        audit_client = FakeGitHubClient(fixture)
        issue_client = FakeGitHubClient(fixture)
        audit_organization(audit_client, [record()], TODAY, issue_client=issue_client)
        self.assertEqual([], audit_client.writes)
        self.assertEqual(1, len(issue_client.writes))

    def test_report_serializes_to_json_and_markdown(self):
        fixture = load_fixture("compliant-repository.json")
        del fixture["files"]["AGENTS.md"]
        report = audit_organization(
            FakeGitHubClient(fixture), [record()], TODAY, synchronize_issues=False
        )
        self.assertEqual(1, len(json.loads(report.to_json())["findings"]))
        self.assertIn("WAEF-AUDIT-AGENTS", report.to_markdown())

    def test_workflow_uses_immutable_actions_and_split_token_scopes(self):
        workflow = (ROOT / ".github" / "workflows" / "waef-audit.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('cron: "17 22 * * *"', workflow)
        self.assertIn(
            "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10", workflow
        )
        self.assertEqual(
            2,
            workflow.count(
                "actions/create-github-app-token@fee1f7d63c2ff003460e3d139729b119787bc349"
            ),
        )
        read_block, issue_block = workflow.split(
            "- name: Create repository-limited Issue token", 1
        )
        self.assertNotIn("repositories: |", read_block)
        self.assertIn("permission-contents: read", read_block)
        self.assertIn("repositories: |", issue_block)
        self.assertIn("permission-issues: write", issue_block)
        self.assertIn("WAEF_ISSUE_TOKEN", workflow)
        self.assertNotIn("upload-artifact", workflow)


if __name__ == "__main__":
    unittest.main()
