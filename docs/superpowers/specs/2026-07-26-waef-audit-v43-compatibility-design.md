# WAEF Audit v4.3 Compatibility Design

## Goal

Make the independent organization audit recognize the exact WAEF v4.2 and
v4.3 workflow contracts that already pass repository-local WAEF validation,
without weakening repository binding, immutable pinning, source-workflow
evidence, or fail-closed behavior.

## Non-Goals

- Do not change product code, repository visibility, deployment behavior, or
  licensing.
- Do not change the reviewed repository inventory or LISTC's
  `active + r-package` classification.
- Do not make WAEF public or replace full commit pins with mutable refs.
- Do not close historical audit Issues in this change. Resolved-finding Issue
  lifecycle will be handled in a second, independently reviewed Pull Request.
- Do not onboard repositories that currently lack WAEF governance files in
  this change.

## Current State

The organization audit has completed successfully at the infrastructure layer:
the organization-wide read token, repository-limited Issue token, audit test
suite, repository enumeration, and disabled-Issues central routing all work.
The latest audit reports 50 findings and exits with status 1.

Eight findings across five repositories are compatibility false positives:

- `.github`, DCC, and website use exact guarded inline bridges accepted by
  their locked WAEF validators, but the central audit accepts only the legacy
  reusable caller.
- WAEF and repository-template use the reusable workflow successfully, but
  their GitHub check-run names are `compliance / WAEF Compliance`.
- GitHub's current Actions API returns workflow run paths as
  `.github/workflows/waef-compliance.yml`, while the audit fixture and
  implementation require an `@main` suffix.

The remaining findings describe repositories that have not yet adopted the
required WAEF governance files or checks. Those repositories must be handled
only after compatibility false positives are removed.

## Proposed Design

### Dual-Mode Exact Workflow Rendering

`operations/waef/render_adapter.py` will provide two deterministic renderers:

1. The existing private reusable workflow caller.
2. The guarded inline public bridge defined by WAEF v4.2 and generalized by
   WAEF v4.3.

The public renderer will bind the complete workflow to:

- the exact `weiandata/<repository>` identity;
- the exact commit in `.waef/waef.lock.yml`;
- immutable approved SHAs for `actions/checkout` and
  `actions/create-github-app-token`;
- read-only workflow permissions;
- an App token scoped only to `weiandata/WAEF`;
- the exact lock path, checkout path, provenance command, dependency
  installation command, and repository validation command.

The audit will compare the complete workflow text with the selected renderer.
It will not accept a workflow based only on string anchors or partial semantic
checks.

### Visibility and Version Selection

`audit_organization()` already receives GitHub repository metadata. It will
pass the repository's public/private state into workflow validation.

- Private repositories must use the exact reusable caller.
- Public repositories locked to WAEF v4.3 must use the exact
  repository-bound public bridge.
- The public `.github` repository locked to WAEF v4.2 may use the exact bridge
  introduced specifically for that repository.
- Any other public repository locked below v4.3 will fail closed because its
  locked WAEF contract does not authorize the generalized bridge.
- Any unrecognized future WAEF version will fail closed until a reviewed
  central-audit compatibility update defines its exact workflow contract.

The validator will not infer visibility mode from workflow structure.

### Default-Branch Evidence

The audit will continue to bind evidence to the repository's current default
branch HEAD.

A successful source workflow run must match all of:

- workflow path `.github/workflows/waef-compliance.yml`, accepting GitHub's
  current path representation and the prior `@<default-branch>`
  representation;
- default branch;
- current HEAD SHA;
- `push` event;
- completed status;
- successful conclusion;
- workflow name `WAEF Compliance`.

Check-run evidence will accept the two GitHub-generated official contexts:

- `WAEF Compliance` for the inline public bridge;
- `compliance / WAEF Compliance` for the reusable workflow job.

At least one accepted check run must be successful. Multiple accepted check
runs may exist at the same HEAD. The exact source-workflow requirement remains
mandatory, so a same-name check from another workflow cannot satisfy the
audit.

## Data Flow

1. Enumerate organization repositories and retain the returned visibility
   metadata.
2. Read each registered repository's default-branch WAEF lock, project
   metadata, workflow, CODEOWNERS, AGENTS instructions, and exceptions.
3. Verify lock schema, reviewed profile, and tag provenance.
4. Select the exact workflow renderer from repository visibility, lock
   version, and repository identity.
5. Compare the complete repository workflow with the rendered contract.
6. Query check runs for the current default-branch HEAD.
7. Query runs from the exact WAEF workflow file and bind them to branch, HEAD,
   event, status, conclusion, and workflow name.
8. Produce findings and synchronize them using the existing repository-local
   or centralized Issue destination.

## Failure Behavior

The audit remains fail closed.

It will emit `WAEF-AUDIT-WORKFLOW` when:

- the workflow is missing;
- the repository uses the wrong visibility mode;
- a public bridge is not authorized by the locked WAEF version;
- repository identity, lock SHA, action SHA, permissions, scope, command,
  ordering, or any other generated workflow byte differs from the contract.

It will emit `WAEF-AUDIT-CHECK` when:

- no accepted check run succeeds at the default-branch HEAD;
- no successful run originates from the exact WAEF workflow;
- the run belongs to another branch, commit, event, workflow, or state.

API errors, missing metadata, and provenance failures continue to produce
findings or hard failures according to existing behavior.

## Testing

Test-driven implementation will add regressions for:

- exact WAEF v4.2 `.github` public bridge acceptance;
- exact WAEF v4.3 public consumer bridge acceptance;
- rejection of a bridge bound to another repository;
- rejection of a bridge with the wrong WAEF or action SHA;
- rejection of a generalized public bridge below WAEF v4.3;
- acceptance of GitHub's workflow path without `@main`;
- backward-compatible acceptance of the prior path representation;
- acceptance of `compliance / WAEF Compliance` for reusable workflows;
- acceptance of multiple official check runs when at least one succeeds;
- continued rejection of a same-name check from another workflow.

The complete `operations/waef/tests` suite must pass, and `git diff --check`
must report no errors.

## Rollout and Verification

1. Implement the compatibility change in one focused branch and Pull Request.
2. Require a successful WAEF Compliance check on the Pull Request.
3. Merge only after human authorization under the existing governance policy.
4. Verify WAEF Compliance on the resulting `main` commit.
5. Run the organization audit from `main`.
6. Confirm that the compatibility findings for `.github`, DCC, website, WAEF,
   and repository-template disappear.
7. Use the reduced finding set to plan repository onboarding waves without
   changing project-owned functionality.
8. Design and implement resolved-finding Issue closure in a separate Pull
   Request.

## Risks and Mitigations

- **Renderer drift:** The central renderer could diverge from WAEF. Mitigation:
  copy the exact v4.3 contract, test every security-critical field, and update
  central audit compatibility in reviewed WAEF release migrations.
- **Over-broad check-name matching:** Suffix matching could accept a spoofed
  check. Mitigation: accept only the two explicit names and independently
  require a successful run from the exact workflow file at the exact HEAD.
- **Visibility misclassification:** A workflow could be evaluated in the
  wrong mode. Mitigation: use GitHub repository metadata, never workflow
  self-identification.
- **Scope expansion:** Compatibility work could mix with repository adoption
  or stale-Issue cleanup. Mitigation: keep both out of this Pull Request and
  verify the changed-file set before publishing.
