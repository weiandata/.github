# Seven-Repository WAEF v4.3 Rollout Design

## Goal

Adopt the exact WAEF v4.3 governance contract in the seven registered
repositories that remain non-compliant after organization audit run
[`30206524474`](https://github.com/weiandata/.github/actions/runs/30206524474),
without changing product code, dependencies, builds, deployments, release
behavior, licensing terms, or existing project-specific instructions.

## Approved Baseline

The post-merge audit registered 12 repositories, reported five compliant
repositories, and emitted 42 findings. The five compliant repositories are
`.github`, DCC, WAEF, repository-template, and website.

Each remaining repository has exactly one finding in each of six rule
families:

- `WAEF-AUDIT-AGENTS`;
- `WAEF-AUDIT-CHECK`;
- `WAEF-AUDIT-CODEOWNERS`;
- `WAEF-AUDIT-LOCK`;
- `WAEF-AUDIT-PROJECT`; and
- `WAEF-AUDIT-WORKFLOW`.

The remaining repositories are IRTC, LISTC, WFC, data-reporting-ai,
website-AI-preview, website-global-preview, and wechat-md-edit. The audit
infrastructure, GitHub App tokens, repository access, unit tests, and Issue
synchronization all succeeded. The workflow failed only because real
repository findings remain.

## Non-Goals

- Do not modify application, package, website, statistical, content, test, or
  deployment source.
- Do not alter existing business CI or release workflows.
- Do not add dependencies, install scripts, runtime services, or generated
  build artifacts.
- Do not change repository visibility, GitHub archival state, branch
  protection, licensing, or ownership.
- Do not use WAEF exceptions to suppress missing baseline governance.
- Do not change the reviewed organization inventory in this rollout.
- Do not reinterpret LISTC's completed-project state in this rollout. The
  current reviewed inventory remains `active + r-package`; lifecycle model
  changes require a separate design and Pull Request.
- Do not merge rollout Pull Requests without separate explicit authorization.

## Considered Approaches

### Approach A: Complete Bounded Consumer Contract

Create one independently reviewable Pull Request per repository. Add or
minimally extend the complete repository-consumer contract enforced by the
locked WAEF v4.3 validator. Render the workflow from the exact WAEF v4.3
contract for the repository's real visibility.

This approach is approved because it isolates rollback, preserves project
integrity, produces repository-local evidence, and avoids unrelated template
expansion.

### Approach B: Audit-Only Five-File Envelope

Add only `AGENTS.md`, `CODEOWNERS`, the lock, project metadata, and the
compliance workflow because those are the files inspected by the central
organization audit.

This was rejected after implementation-plan self-review because the
repository-local WAEF v4.3 validator additionally requires cache exclusion,
contribution lifecycle language, and versioned review templates. An audit-only
envelope would reduce central findings while every new repository WAEF check
would fail.

### Approach C: Central Exceptions

Add temporary audit exceptions for missing governance files.

This was rejected because the findings are accurate, the repositories are
accessible, and suppressing the findings would weaken rather than implement
the approved governance baseline.

## Repository Contract Matrix

All repositories use WAEF tag `v4.3` at immutable commit
`bd0eaa76490fd4e79f8ecb28a75dd0fdda6623e7`.

| Repository | Visibility | Owner | Status | Profile | Workflow mode |
| --- | --- | --- | --- | --- | --- |
| IRTC | public | package-maintainers | active | r-package | guarded public bridge |
| LISTC | public | statistics-engineering | active | r-package | guarded public bridge |
| WFC | public | package-maintainers | active | r-package | guarded public bridge |
| data-reporting-ai | private | analytics-engineering | planned | planned-project | private reusable caller |
| website-AI-preview | public | web-engineering | active | static-website | guarded public bridge |
| website-global-preview | public | web-engineering | active | static-website | guarded public bridge |
| wechat-md-edit | private | web-engineering | active | web-application | private reusable caller |

The `.waef/project.yml` values are:

| Repository | Purpose | Risk | Publication | Language |
| --- | --- | --- | --- | --- |
| IRTC | Provide item-response-theory analysis and reviewable reporting | high | allowed | R |
| LISTC | Produce design-aware statistical pivot tables for assessment and survey data | high | allowed | R |
| WFC | Provide controlled and reviewable survey weighting workflows | controlled | allowed | R |
| data-reporting-ai | Hold the approved boundary for a planned data-reporting AI project | low | blocked | undecided |
| website-AI-preview | Operate the bilingual WeianData AI Skills website | controlled | allowed | TypeScript/Next.js |
| website-global-preview | Operate the bilingual WeianData static global website | moderate | allowed | Static HTML/JavaScript/Python |
| wechat-md-edit | Maintain the web-based Markdown editor and its supported clients | controlled | allowed | TypeScript/Vue |

## Governance File Design

### Complete Bounded File Set

Every repository changes or creates only these governance surfaces:

- `AGENTS.md`;
- `CODEOWNERS`;
- `.gitignore`;
- `CONTRIBUTING.md`;
- `.waef/waef.lock.yml`;
- `.waef/project.yml`;
- `.github/workflows/waef-compliance.yml`;
- `.github/ISSUE_TEMPLATE/waef-change.md`;
- `.github/pull_request_template.md`;
- `.waef/templates/VALIDATION_REPORT_TEMPLATE.md`;
- `.waef/templates/DESIGN_DOC_TEMPLATE.md`;
- `.waef/templates/ADR_TEMPLATE.md`; and
- `.waef/templates/RELEASE_TEMPLATE.md`.

IRTC, LISTC, and WFC also update `.Rbuildignore` so `.waef/` and any newly
introduced root governance entry point remain outside the R package source
bundle. This is a build-exclusion safeguard, not a change to package code or
runtime behavior.

Existing uppercase `.github/PULL_REQUEST_TEMPLATE.md` files are moved to the
validator's canonical lowercase path and retain their project-owned content.
The WAEF review block is appended rather than replacing the existing template.
Existing bug, feature, and documentation Issue templates remain unchanged.

### WAEF Lock

Each repository receives `.waef/waef.lock.yml` with schema 1, framework
`WAEF`, version `4.3`, tag `v4.3`, the immutable commit above, and exactly one
profile from the matrix. `updated_by` must be the exact repository-local
rollout Pull Request URL.

Because the lock schema requires an existing Pull Request number, each rollout
branch first receives an empty reservation commit. The branch is pushed and a
draft Pull Request is opened before governance files are written. The lock
then records that real Pull Request URL. No placeholder URL is committed.

### Project Metadata

Each repository receives `.waef/project.yml` using the exact owner, status,
purpose, risk, publication, and language values in the matrix. These values
describe the repository but do not affect runtime behavior.

### Agent Instructions

The exact WAEF v4.3 locked bootstrap block is added at the start of
`AGENTS.md`. It requires agents to:

- read `.waef/waef.lock.yml`;
- use only its exact WAEF commit;
- stop if `.waef/cache/` is absent or mismatched;
- apply the locked profile; and
- allow project rules to strengthen but never weaken WAEF.

IRTC, WFC, and wechat-md-edit retain all existing instructions byte-for-byte
after the inserted block. Repositories without `AGENTS.md` receive only the
locked bootstrap block; this rollout does not invent project-development
rules.

### Cache and Package Exclusion

Each `.gitignore` receives exactly `.waef/cache/` under a WAEF local-cache
comment. The cache remains untracked and exists only to validate the immutable
framework checkout.

Each R package receives `^\.waef$` in `.Rbuildignore`. LISTC also receives
`^AGENTS\.md$` because its new root instruction file does not yet have a build
exclusion. Existing exclusions remain unchanged.

### Contribution and Review Adapters

Each `CONTRIBUTING.md` retains its project guidance and receives the exact WAEF
v4.3 lifecycle block requiring an Issue, approved plan, categorized branch,
Pull Request, validation, accountable review, and release sequence.

The repository receives the six versioned v4.3 review adapters required by the
locked validator:

- one WAEF change Issue template;
- one canonical lowercase Pull Request template containing the required WAEF
  review block;
- a validation-report template;
- a design-document template;
- an ADR template; and
- a release template.

These are contributor-facing Markdown files. They do not install software,
change existing business workflows, or alter runtime behavior.

### Governance Ownership

Existing wildcard ownership remains unchanged. A deterministic governance
block is appended to `CODEOWNERS`:

- `/AGENTS.md` and `/.waef/` belong to
  `@weiandata/waef-maintainers`;
- `/.github/workflows/waef-compliance.yml` belongs to
  `@weiandata/waef-maintainers`;
- `/.github/workflows/` and `/CODEOWNERS` belong to
  `@weiandata/organization-governance`; and
- one existing license or copyright declaration belongs to
  `@weiandata/organization-governance`.

The protected declaration is `/DESCRIPTION` for the R packages,
`/PROPRIETARY.md` for data-reporting-ai and both static websites, and
`/LICENSE` for wechat-md-edit. wechat-md-edit receives a new root
`CODEOWNERS` whose wildcard owner remains `@makunxiang-weiandata`.

### Compliance Workflow

Public repositories receive the complete repository-bound WAEF v4.3 bridge,
rendered for the exact `weiandata/<repository>` identity. The bridge:

- uses read-only repository permissions;
- checks out the consumer without persisted credentials;
- refuses any caller repository other than its exact identity;
- creates a GitHub App token limited to `weiandata/WAEF`;
- checks out the immutable WAEF commit into `.waef/cache`;
- verifies the checkout against the lock;
- installs only the pinned WAEF validator requirements; and
- runs the locked validator against the consumer.

Private repositories receive the compact reusable workflow caller pinned to
the same immutable WAEF commit and pass only the lock path plus the two
repository secrets required by the existing WAEF contract.

Neither workflow edits, replaces, or calls existing business CI. It runs only
on `pull_request` and `push`.

## Pull Request Isolation

Each repository uses its own worktree, branch, draft Pull Request, validation
report, and commit history. No cross-repository aggregate branch is permitted.

The rollout order is:

1. data-reporting-ai, the planned private repository with no runtime;
2. website-global-preview and website-AI-preview, the two static websites;
3. IRTC, LISTC, and WFC, the three public R packages; and
4. wechat-md-edit, the private web application with the largest existing
   instruction surface.

This order proves both workflow modes on low-runtime-risk repositories before
moving to statistical packages and the web monorepo. Failure in one
repository does not block review of an already validated repository, but no
later rollout may copy an unverified workflow result.

## Validation

Every repository must pass all of the following before its draft Pull Request
can become Ready for review:

1. Confirm the diff touches only the 13 complete consumer-contract paths
   listed above, plus `.Rbuildignore` for IRTC, LISTC, and WFC. An uppercase
   Pull Request template may appear as a rename to the canonical lowercase
   path.
2. Populate `.waef/cache` from the immutable WAEF commit without tracking the
   cache.
3. Run `verify_framework_checkout.py` against the lock.
4. Run WAEF `validate_repository.py` against the repository.
5. Run `git diff --check`.
6. Run the existing repository-native validation that does not mutate product
   source:
   - existing template/Markdown checks for data-reporting-ai;
   - existing site validator or documented test/build commands for the static
     websites;
   - the repository's release verification or R package test/check gate for
     IRTC, LISTC, and WFC; and
   - lint, type-check, test, and production build for wechat-md-edit when its
     existing dependency installation is available.
7. Record commands, exit status 0, and literal `Verdict: PASS` in the Pull
   Request validation report.
8. Confirm all GitHub Actions checks complete successfully.

If a repository-native validation cannot run because an existing external
dependency or environment is unavailable, the Pull Request remains Draft and
reports the exact blocked command. WAEF success alone does not justify a claim
that the product remains buildable.

## Organization-Level Acceptance

After all approved repository Pull Requests are separately reviewed and
merged:

1. wait for each default-branch WAEF `push` run to succeed;
2. rerun `WAEF Organization Audit` from `.github` main;
3. require 12 registered repositories, 12 compliant repositories, and zero
   findings; and
4. verify that resolved audit Issues follow the separately approved Issue
   lifecycle policy.

The expected zero-finding result is an acceptance target, not permission to
weaken the audit if a genuine new finding appears.

## Failure Handling and Rollback

- A workflow rendering mismatch stops only that repository's rollout.
- A failed product validation stops the Pull Request and triggers diagnosis;
  it does not authorize product-code changes in the governance PR.
- A visibility mismatch stops the rollout before push.
- A changed WAEF tag or commit requires a new reviewed design; mutable refs are
  never substituted.
- Rollback is repository-local: revert the unmerged branch or revert the
  single merged governance Pull Request. Existing business files remain
  untouched.
