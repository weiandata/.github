#!/usr/bin/env python3
"""Validate a staged WAEF ruleset and perform a read-only capability preflight."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
from pathlib import Path
from typing import Any, TextIO

try:
    from .github_client import GitHubClient
except ImportError:  # pragma: no cover - direct script execution
    from github_client import GitHubClient


GITHUB_ACTIONS_INTEGRATION_ID = 15368
SUPPORTED_ORGANIZATION_RULESET_PLANS = frozenset(
    {"team", "business", "business_plus", "enterprise"}
)
EXPECTED_CHECKS = [
    {
        "context": "compliance / WAEF Compliance",
        "integration_id": GITHUB_ACTIONS_INTEGRATION_ID,
    },
    {"context": "Project CI", "integration_id": GITHUB_ACTIONS_INTEGRATION_ID},
]


def _rule(document: dict[str, Any], rule_type: str) -> dict[str, Any] | None:
    rules = document.get("rules")
    if not isinstance(rules, list):
        return None
    matches = [item for item in rules if isinstance(item, dict) and item.get("type") == rule_type]
    return matches[0] if len(matches) == 1 else None


def validate_ruleset(document: Any) -> list[str]:
    """Return deterministic safety errors for the staged organization ruleset."""

    if not isinstance(document, dict):
        return ["ruleset root must be an object"]

    errors: list[str] = []
    if document.get("target") != "branch":
        errors.append("ruleset target must be branch")
    if document.get("enforcement") != "disabled":
        errors.append("enforcement must remain disabled")
    if document.get("bypass_actors") != []:
        errors.append("bypass actors must be empty")

    conditions = document.get("conditions")
    if not isinstance(conditions, dict):
        conditions = {}
    ref_name = conditions.get("ref_name")
    if not isinstance(ref_name, dict) or ref_name.get("include") != ["~DEFAULT_BRANCH"]:
        errors.append("default branch target is required")
    repository_name = conditions.get("repository_name")
    if not isinstance(repository_name, dict) or repository_name.get("include") != ["~ALL"]:
        errors.append("all current and future repositories must be targeted")

    deletion = _rule(document, "deletion")
    if deletion is None:
        errors.append("deletion protection is required")
    force_push = _rule(document, "non_fast_forward")
    if force_push is None:
        errors.append("force-push protection is required")

    pull_request = _rule(document, "pull_request")
    pull_parameters = pull_request.get("parameters", {}) if pull_request else {}
    if pull_parameters.get("required_approving_review_count") != 1:
        errors.append("one approving review is required")
    if pull_parameters.get("require_code_owner_review") is not True:
        errors.append("code-owner review is required")
    if pull_parameters.get("required_review_thread_resolution") is not True:
        errors.append("resolved conversations are required")

    status_rule = _rule(document, "required_status_checks")
    status_parameters = status_rule.get("parameters", {}) if status_rule else {}
    if status_parameters.get("strict_required_status_checks_policy") is not True:
        errors.append("strict status checks are required")
    checks = status_parameters.get("required_status_checks")
    if not isinstance(checks, list):
        checks = []
    if EXPECTED_CHECKS[0] not in checks:
        errors.append("WAEF Compliance must be source-bound to GitHub Actions")
    if EXPECTED_CHECKS[1] not in checks:
        errors.append("Project CI must be source-bound to GitHub Actions")
    if checks != EXPECTED_CHECKS:
        errors.append(
            "required checks must be exactly compliance / WAEF Compliance and Project CI"
        )

    rule_types = [
        item.get("type") for item in document.get("rules", []) if isinstance(item, dict)
    ]
    expected_rule_types = [
        "deletion",
        "non_fast_forward",
        "pull_request",
        "required_status_checks",
    ]
    if sorted(rule_types) != sorted(expected_rule_types):
        errors.append("ruleset must contain only the four reviewed rule types")

    return errors


def load_ruleset(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("ruleset root must be an object")
    return value


def preflight(client: GitHubClient, organization: str, *, output: TextIO = sys.stdout) -> int:
    """Read plan and ruleset capability without changing organization settings."""

    try:
        organization_data = client.request("GET", f"/orgs/{organization}")
    except urllib.error.HTTPError as error:
        if error.code in {401, 403, 404}:
            print(f"organization preflight: unavailable (HTTP {error.code})", file=output)
            print("decision: stop; authorization is insufficient or the organization is unavailable", file=output)
            return 2
        raise

    plan_data = organization_data.get("plan", {}) if isinstance(organization_data, dict) else {}
    plan_name = str(plan_data.get("name", "unknown")).lower()
    private_repository_allowance = plan_data.get("private_repos", "unknown")
    total_private_repositories = (
        organization_data.get("total_private_repos", "unknown")
        if isinstance(organization_data, dict)
        else "unknown"
    )
    print(f"organization: {organization}", file=output)
    print(f"plan: {plan_name}", file=output)
    print(f"plan private-repository allowance: {private_repository_allowance}", file=output)
    print(f"organization private repositories: {total_private_repositories}", file=output)

    if plan_name not in SUPPORTED_ORGANIZATION_RULESET_PLANS:
        print("organization rulesets for private repositories: unsupported", file=output)
        print("decision: stop; keep the reviewed ruleset disabled", file=output)
        return 2

    try:
        rulesets = client.request("GET", f"/orgs/{organization}/rulesets")
    except urllib.error.HTTPError as error:
        if error.code in {401, 403, 404}:
            print(f"organization rulesets: unavailable (HTTP {error.code})", file=output)
            print("decision: stop; authorization or plan capability is insufficient", file=output)
            return 2
        raise

    count = len(rulesets) if isinstance(rulesets, list) else "unknown"
    print("organization rulesets: available", file=output)
    print(f"existing rulesets: {count}", file=output)
    print("mutation performed: no", file=output)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate a disabled ruleset file")
    validate.add_argument("path", type=Path)
    preflight_parser = subparsers.add_parser(
        "preflight", help="read organization plan and ruleset capability"
    )
    preflight_parser.add_argument("--organization", default="weiandata")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        try:
            errors = validate_ruleset(load_ruleset(args.path))
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"ruleset validation failed: {error}", file=sys.stderr)
            return 1
        if errors:
            for error in errors:
                print(f"ruleset validation failed: {error}", file=sys.stderr)
            return 1
        print("ruleset validation passed")
        print("enforcement: disabled")
        return 0

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("preflight requires GH_TOKEN or GITHUB_TOKEN", file=sys.stderr)
        return 2
    return preflight(GitHubClient(token), args.organization)


if __name__ == "__main__":
    raise SystemExit(main())
