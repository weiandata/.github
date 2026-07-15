# Staged WAEF Organization Ruleset

`ruleset.json` is the reviewed, machine-readable definition for default-branch
governance across all current and future WeianData repositories. It is checked
in with `enforcement: disabled` and no bypass actors. This repository does not
contain an activation command.

## Staged controls

The ruleset targets `~DEFAULT_BRANCH` in `~ALL` repositories and stages these
controls:

- changes enter through a Pull Request with at least one approval;
- code-owner review is required when owned paths change;
- review conversations must be resolved;
- `compliance / WAEF Compliance` and `Project CI` are strict required checks;
- both check contexts are bound to the GitHub Actions App integration;
- default branches cannot be deleted or force-pushed; and
- no person, team, App, or deploy key is configured to bypass the rules.

The WAEF context is the actual reusable-workflow check-run name observed in the
private sandbox; `WAEF Compliance` alone is the workflow-run name and is not a
valid required-check context. Both checks use the verified GitHub Actions App
integration ID `15368`.

GitHub required-check source binding identifies the App that produced a check,
not the reusable workflow path. The independent daily audit therefore remains
required: it binds successful WAEF evidence to the governed caller path, the
default-branch head SHA, and the exact WAEF release pin.

## Local validation

Run the deterministic validator before review:

```bash
python3 operations/waef/apply_ruleset.py validate operations/waef/ruleset.json
```

The command succeeds only when the reviewed controls are present and
`enforcement` remains `disabled`.

## Read-only capability preflight

The preflight accepts a token only through `GH_TOKEN` or `GITHUB_TOKEN`:

```bash
GH_TOKEN="<short-lived-token>" python3 operations/waef/apply_ruleset.py preflight --organization weiandata
```

It performs only `GET` requests. It reads the organization plan first. On an
unsupported plan it exits `2` without requesting the organization rulesets
endpoint. On a supported plan it reads the endpoint to confirm availability;
an authorization or feature error also exits `2`. It never creates, updates,
enables, or deletes a ruleset.

GitHub currently documents organization rulesets for customers on GitHub Team
or GitHub Enterprise plans. The 2026-07-15 preflight observed the `weiandata`
organization on the Free plan with private repositories, so activation is not
available under the current plan. See [Creating rulesets for repositories in
your organization](https://docs.github.com/en/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization)
and [REST API endpoints for rules](https://docs.github.com/en/rest/orgs/rules).

## Activation gate

Activation is a separate organization mutation and remains prohibited until:

1. all eleven registered repositories pass the baseline audit;
2. the WAEF release and exact pins are approved and published;
3. the final JSON and preflight evidence receive governance review;
4. plan capability and least-privilege authorization are available;
5. rollback and incident ownership are confirmed; and
6. an Organization Owner explicitly approves activation.

If any condition is absent, retain the disabled file and continue using the
audit as detection evidence. A later activation implementation must be a new,
reviewed change; it must not weaken the validator or add a bypass actor.
