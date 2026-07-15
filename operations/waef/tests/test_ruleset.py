import copy
import io
import json
import unittest
from pathlib import Path

from operations.waef.apply_ruleset import preflight, validate_ruleset


RULESET = Path(__file__).resolve().parents[1] / "ruleset.json"
GITHUB_ACTIONS_INTEGRATION_ID = 15368


class RecordingClient:
    def __init__(self, responses):
        self.responses = responses
        self.requests = []

    def request(self, method, path, body=None):
        self.requests.append((method, path, body))
        return self.responses[path]


def load_ruleset():
    return json.loads(RULESET.read_text(encoding="utf-8"))


def rule(document, rule_type):
    return next(item for item in document["rules"] if item["type"] == rule_type)


class RulesetDefinitionTests(unittest.TestCase):
    def test_staged_ruleset_has_complete_default_branch_controls(self):
        document = load_ruleset()

        self.assertEqual([], validate_ruleset(document))
        self.assertEqual("branch", document["target"])
        self.assertEqual("disabled", document["enforcement"])
        self.assertEqual([], document["bypass_actors"])
        self.assertEqual(
            ["~DEFAULT_BRANCH"], document["conditions"]["ref_name"]["include"]
        )
        self.assertEqual(["~ALL"], document["conditions"]["repository_name"]["include"])

        pull_request = rule(document, "pull_request")["parameters"]
        self.assertEqual(1, pull_request["required_approving_review_count"])
        self.assertTrue(pull_request["require_code_owner_review"])
        self.assertTrue(pull_request["required_review_thread_resolution"])

        status_checks = rule(document, "required_status_checks")["parameters"]
        self.assertTrue(status_checks["strict_required_status_checks_policy"])
        self.assertEqual(
            [
                {
                    "context": "compliance / WAEF Compliance",
                    "integration_id": GITHUB_ACTIONS_INTEGRATION_ID,
                },
                {
                    "context": "Project CI",
                    "integration_id": GITHUB_ACTIONS_INTEGRATION_ID,
                },
            ],
            status_checks["required_status_checks"],
        )
        self.assertIsNotNone(rule(document, "deletion"))
        self.assertIsNotNone(rule(document, "non_fast_forward"))

    def test_validator_rejects_unsafe_or_incomplete_variants(self):
        mutations = {
            "enforcement must remain disabled": lambda value: value.update(
                enforcement="active"
            ),
            "bypass actors must be empty": lambda value: value["bypass_actors"].append(
                {"actor_id": 1, "actor_type": "Team", "bypass_mode": "always"}
            ),
            "default branch target is required": lambda value: value["conditions"][
                "ref_name"
            ].update(include=["refs/heads/main"]),
            "strict status checks are required": lambda value: rule(
                value, "required_status_checks"
            )["parameters"].update(strict_required_status_checks_policy=False),
            "WAEF Compliance must be source-bound to GitHub Actions": lambda value: rule(
                value, "required_status_checks"
            )["parameters"]["required_status_checks"][0].pop("integration_id"),
            "one approving review is required": lambda value: rule(
                value, "pull_request"
            )["parameters"].update(required_approving_review_count=0),
            "code-owner review is required": lambda value: rule(value, "pull_request")[
                "parameters"
            ].update(require_code_owner_review=False),
            "resolved conversations are required": lambda value: rule(
                value, "pull_request"
            )["parameters"].update(required_review_thread_resolution=False),
            "deletion protection is required": lambda value: value.update(
                rules=[item for item in value["rules"] if item["type"] != "deletion"]
            ),
            "force-push protection is required": lambda value: value.update(
                rules=[
                    item for item in value["rules"] if item["type"] != "non_fast_forward"
                ]
            ),
        }

        for expected, mutate in mutations.items():
            with self.subTest(expected=expected):
                document = copy.deepcopy(load_ruleset())
                mutate(document)
                self.assertIn(expected, validate_ruleset(document))


class RulesetPreflightTests(unittest.TestCase):
    def test_free_plan_private_repositories_stop_without_ruleset_request(self):
        client = RecordingClient(
            {
                "/orgs/weiandata": {
                    "login": "weiandata",
                    "plan": {"name": "free", "private_repos": 10000},
                    "total_private_repos": 7,
                }
            }
        )
        output = io.StringIO()

        result = preflight(client, "weiandata", output=output)

        self.assertEqual(2, result)
        self.assertEqual([("GET", "/orgs/weiandata", None)], client.requests)
        self.assertIn("plan: free", output.getvalue())
        self.assertIn("organization private repositories: 7", output.getvalue())
        self.assertIn("unsupported", output.getvalue())

    def test_team_plan_checks_ruleset_endpoint_without_mutation(self):
        client = RecordingClient(
            {
                "/orgs/weiandata": {
                    "login": "weiandata",
                    "plan": {"name": "team", "private_repos": 10000},
                    "total_private_repos": 11,
                },
                "/orgs/weiandata/rulesets": [],
            }
        )
        output = io.StringIO()

        result = preflight(client, "weiandata", output=output)

        self.assertEqual(0, result)
        self.assertEqual(
            [
                ("GET", "/orgs/weiandata", None),
                ("GET", "/orgs/weiandata/rulesets", None),
            ],
            client.requests,
        )
        self.assertTrue(all(method == "GET" and body is None for method, _, body in client.requests))
        self.assertIn("organization rulesets: available", output.getvalue())


if __name__ == "__main__":
    unittest.main()
