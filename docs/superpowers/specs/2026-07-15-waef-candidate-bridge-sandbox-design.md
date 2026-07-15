# WAEF 4.0 Candidate Bridge Sandbox Design

| Field | Value |
|---|---|
| Status | Approved |
| Owner | WeianData Engineering |
| Approval date | 2026-07-15 |
| Sandbox | `weiandata/waef-compliance-sandbox` (private, temporary) |
| Candidate commit | `da22b444005e834e12d114651f354277e0e3a10d` |

## 1. Purpose

Break the rollout plan's circular dependency without weakening the WAEF 4.0
release gate. WAEF Pull Request #2 requires independent organization controls
and private-sandbox evidence before release, while the template plan requires an
approved immutable `v4.0` release before `repository-template` may adopt WAEF
4.0 or create its own template-derived sandbox.

The bridge sandbox validates only the unreleased candidate's integration with
the organization-owned audit and review-only upgrade automation. It does not
claim that `repository-template` is ready and does not substitute for the later
template-derived sandbox proof.

## 2. Authority boundary

The human approval authorizes creation of one private temporary repository
named `weiandata/waef-compliance-sandbox` and the test mutations listed below.
It does not authorize:

- merging WAEF Pull Request #2 or any sandbox Pull Request;
- creating or publishing the `v4.0` tag or a release;
- enabling an organization-wide ruleset or production scheduled audit;
- migrating a production consumer;
- adding business code, deployment credentials, or production data; or
- deleting the sandbox without a separate human approval after evidence is
  retained.

The previously reviewed candidate commit
`993ef1e41306146f62881106ab17cae2e23162f5` cannot produce a green consumer
run before `v4.0` exists because the production reusable workflow correctly
requires release-tag provenance. WAEF Pull Request #2 therefore adds a separate
sandbox-only candidate workflow. That change passed 58 tests, 16 behavioral
scenarios, the hosted `WAEF Self Check`, and independent review with no remaining
findings. Its full commit SHA
`da22b444005e834e12d114651f354277e0e3a10d` is the only accepted bridge
candidate identity. No mutable branch, `main`, `latest`, or provisional value is
accepted.

## 3. Sandbox construction

Create a private, non-template repository with Issues and Actions enabled. Add
only a minimal planned-project consumer contract and test fixtures required to
exercise WAEF and organization automation. The repository contains no copied
normative WAEF documents; it references the private WAEF candidate workflow by
the exact reviewed commit and uses generated, project-facing adapters only.

The candidate workflow is a separate reusable workflow in WAEF Pull Request #2.
It accepts calls only from `weiandata/waef-compliance-sandbox`, verifies the
exact checked-out candidate SHA, verifies WAEF 4.0 metadata, and runs the full
repository validator. It defers only the final `v4.0` tag-to-commit proof. It
cannot be selected through the production `compliance.yml`, does not weaken the
production workflow, and is covered by workflow-contract tests.

The sandbox is registered temporarily in a sandbox-only inventory or supplied
through an explicitly scoped validation input. Production inventory and
production schedule remain unchanged. GitHub App repository access and secrets
are granted only as required by the already documented split-permission model:
the Read App remains read-only, and any Automation App write access is limited
to this sandbox for the validation window.

## 4. Validation scenarios

The bridge records a clean baseline and then uses separate unmerged Pull
Requests or reversible branches to prove fail-closed behavior:

1. a clean candidate-pinned consumer produces successful WAEF evidence;
2. a wrong WAEF SHA is rejected;
3. required plan or validation evidence removal is rejected;
4. an expired exception is rejected;
5. deleting, renaming, trigger-removing, or adding `if: false` to the local WAEF
   caller cannot produce acceptable organization audit evidence;
6. a red project check remains red and does not become WAEF-compliant by name
   spoofing;
7. audit findings use stable fingerprints and repeated observations update one
   Issue instead of creating duplicates; and
8. a reviewed upgrade dispatch may open or update a Draft Pull Request but does
   not merge it, enable auto-merge, or write the default branch directly.

Every destructive scenario is isolated from the clean baseline. No test PR is
merged.

## 5. Evidence and credential safety

Record repository, branch, Pull Request, check-run, workflow-run, and Issue URLs;
exact candidate SHA; check conclusions; App installation scope; and whether log
inspection found credential material. Record secret names and update timestamps
only—never secret values, installation tokens, private keys, or authorization
headers. Do not upload a secret-bearing artifact.

Evidence is written to
`operations/waef/SANDBOX-VALIDATION.md` in `weiandata/.github` and reviewed in
Draft Pull Request #1. Any implementation defect discovered during validation
is fixed with a regression test before the scenario is repeated.

## 6. Acceptance and continuation

The bridge is successful only when all eight scenarios have attributable
evidence, credential inspection is clean, the upgrade Pull Request remains
unmerged, and no production rule or schedule changed. Candidate evidence does
not claim final tag provenance. A successful bridge may satisfy the pre-release
integration blocker in WAEF Pull Request #2, but WAEF Maintainer approval and a
successful production-workflow proof remain required before publication.

After an approved immutable `v4.0` tag exists, `repository-template` is adopted
against that exact release and its separate template-derived sandbox proof is
performed. The bridge repository is deleted only after its durable evidence has
been reviewed and a human explicitly approves cleanup.

## 7. Rollback and stop conditions

Stop immediately if the candidate SHA changes after it is frozen and recorded,
a required permission exceeds the documented boundary, GitHub cannot keep the
repository private, a workflow would expose a credential, or a test requires
merging. Revoke any sandbox-only Automation App access, close unmerged test Pull
Requests, and preserve evidence of the stop condition. Repository deletion is
not part of automatic rollback because it has its own approval checkpoint.
