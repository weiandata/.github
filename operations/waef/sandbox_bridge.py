"""Isolated audit bridge for the single reviewed WAEF candidate sandbox."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
from typing import Any, Sequence
from zoneinfo import ZoneInfo

from operations.waef.audit import (
    AuditReport,
    _finding,
    _read_file,
    _validate_agents,
    _validate_check,
    _validate_codeowners,
    _validate_exceptions,
    _validate_lock,
    _validate_project,
    _write_report,
    synchronize_findings,
)
from operations.waef.github_client import GitHubClient
from operations.waef.models import AuditFinding, RepositoryRecord


SANDBOX_REPOSITORY = "waef-compliance-sandbox"
CANDIDATE_COMMIT = "da22b444005e834e12d114651f354277e0e3a10d"
WORKFLOW_PATH = ".github/workflows/waef-compliance.yml"
SANDBOX_RECORD = RepositoryRecord(
    name=SANDBOX_REPOSITORY,
    owner="sandbox-validation",
    lifecycle="planned",
    profiles=("planned-project",),
    expected_waef_check="WAEF Compliance",
    migration_wave=1,
)


def render_candidate_workflow() -> str:
    """Render the only workflow caller accepted by the candidate bridge."""

    return f"""name: WAEF Compliance
on: [pull_request, push]
permissions:
  contents: read
jobs:
  compliance:
    uses: weiandata/WAEF/.github/workflows/candidate-compliance.yml@{CANDIDATE_COMMIT}
    with:
      waef_commit: {CANDIDATE_COMMIT}
      lock_path: .waef/waef.lock.yml
    secrets:
      WAEF_APP_ID: ${{{{ secrets.WAEF_APP_ID }}}}
      WAEF_APP_PRIVATE_KEY: ${{{{ secrets.WAEF_APP_PRIVATE_KEY }}}}
"""


def _validate_candidate_commit(
    lock: dict[str, Any] | None,
) -> list[AuditFinding]:
    if lock is None or not isinstance(lock.get("commit"), str):
        return []
    if lock["commit"] == CANDIDATE_COMMIT:
        return []
    return [
        _finding(
            SANDBOX_REPOSITORY,
            "WAEF-BRIDGE-CANDIDATE",
            ".waef/waef.lock.yml",
            f"sandbox lock must use reviewed candidate commit {CANDIDATE_COMMIT}",
        )
    ]


def _validate_candidate_workflow(text: str | None) -> list[AuditFinding]:
    if text is None:
        return [
            _finding(
                SANDBOX_REPOSITORY,
                "WAEF-AUDIT-WORKFLOW",
                WORKFLOW_PATH,
                "WAEF candidate workflow caller is missing",
            )
        ]
    if text == render_candidate_workflow():
        return []
    return [
        _finding(
            SANDBOX_REPOSITORY,
            "WAEF-AUDIT-WORKFLOW",
            WORKFLOW_PATH,
            "workflow caller does not exactly use the reviewed WAEF candidate commit",
        )
    ]


def audit_candidate_sandbox(
    read_client: GitHubClient,
    issue_client: GitHubClient | None,
    today: dt.date,
    ref: str = "main",
    *,
    synchronize_issues: bool = True,
) -> AuditReport:
    """Audit only the hard-coded sandbox at the hard-coded candidate commit."""

    if not ref:
        raise ValueError("sandbox audit ref must not be empty")

    agents = _read_file(read_client, SANDBOX_REPOSITORY, ref, "AGENTS.md")
    lock_text = _read_file(
        read_client, SANDBOX_REPOSITORY, ref, ".waef/waef.lock.yml"
    )
    project = _read_file(read_client, SANDBOX_REPOSITORY, ref, ".waef/project.yml")
    workflow = _read_file(read_client, SANDBOX_REPOSITORY, ref, WORKFLOW_PATH)
    codeowners = _read_file(read_client, SANDBOX_REPOSITORY, ref, "CODEOWNERS")
    exceptions = _read_file(
        read_client, SANDBOX_REPOSITORY, ref, ".waef/exceptions.yml"
    )

    findings: list[AuditFinding] = []
    findings.extend(
        _validate_agents(SANDBOX_REPOSITORY, agents, SANDBOX_RECORD.profiles)
    )
    lock, lock_findings = _validate_lock(
        SANDBOX_REPOSITORY, lock_text, SANDBOX_RECORD.profiles
    )
    findings.extend(lock_findings)
    findings.extend(
        _validate_project(
            SANDBOX_REPOSITORY,
            project,
            SANDBOX_RECORD.owner,
            SANDBOX_RECORD.lifecycle,
        )
    )
    findings.extend(_validate_candidate_commit(lock))
    findings.extend(_validate_candidate_workflow(workflow))
    findings.extend(_validate_codeowners(SANDBOX_REPOSITORY, codeowners))
    findings.extend(_validate_exceptions(SANDBOX_REPOSITORY, exceptions, today))
    findings.extend(_validate_check(read_client, SANDBOX_RECORD, ref))

    findings.sort(
        key=lambda item: (
            item.repository.casefold(),
            item.rule_id,
            item.path,
            item.message,
        )
    )
    findings = list({finding.fingerprint: finding for finding in findings}.values())
    report = AuditReport(
        date=today,
        registered_repositories=1,
        compliant_repositories=0 if findings else 1,
        findings=tuple(findings),
    )
    if synchronize_issues and findings:
        if issue_client is None:
            raise ValueError("issue_client is required to synchronize sandbox findings")
        synchronize_findings(issue_client, findings, today)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit_parser = subparsers.add_parser("audit", help="audit the fixed WAEF sandbox")
    audit_parser.add_argument("--ref", default="main")
    audit_parser.add_argument(
        "--today",
        type=dt.date.fromisoformat,
        default=dt.datetime.now(ZoneInfo("Asia/Kuala_Lumpur")).date(),
    )
    audit_parser.add_argument("--json-output")
    audit_parser.add_argument("--markdown-output")
    audit_parser.add_argument("--no-sync-issues", action="store_true")
    args = parser.parse_args(argv)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        audit_parser.error("GH_TOKEN or GITHUB_TOKEN is required")
    synchronize_issues = not args.no_sync_issues
    issue_token = os.environ.get("WAEF_ISSUE_TOKEN")
    if synchronize_issues and not issue_token:
        audit_parser.error("WAEF_ISSUE_TOKEN is required unless --no-sync-issues is used")

    report = audit_candidate_sandbox(
        GitHubClient(token),
        GitHubClient(issue_token) if issue_token else None,
        args.today,
        ref=args.ref,
        synchronize_issues=synchronize_issues,
    )
    json_report = report.to_json()
    markdown_report = report.to_markdown()
    _write_report(args.json_output, json_report)
    _write_report(args.markdown_output, markdown_report)
    print(json_report, end="")
    return 1 if report.findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
