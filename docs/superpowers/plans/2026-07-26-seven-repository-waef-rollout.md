# Seven-Repository WAEF v4.3 Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adopt the complete WAEF v4.3 consumer contract in seven registered repositories without changing product code, dependencies, business CI, deployment, release behavior, or licensing.

**Architecture:** Each repository receives an isolated worktree, branch, draft Pull Request, complete governance adapter, and independent validation evidence. Public repositories use the exact repository-bound bridge; private repositories use the exact reusable caller. Every Pull Request stops at Ready until separately authorized for merge.

**Tech Stack:** Git worktrees, GitHub CLI, GitHub Actions, Markdown, YAML, Python 3, WAEF v4.3, R, npm, pnpm, Next.js, and repository-native validators.

## Global Constraints

- Pin WAEF `v4.3` to `bd0eaa76490fd4e79f8ecb28a75dd0fdda6623e7`.
- Use only the 13 consumer-contract paths defined below; IRTC, LISTC, and WFC may additionally modify `.Rbuildignore`.
- Preserve project-owned content outside inserted WAEF blocks.
- Keep LISTC `active + r-package`; lifecycle redesign is separate.
- Do not use exceptions to suppress missing baseline governance.
- Do not commit `.waef/cache/`.
- Do not run auto-fixing product commands.
- Keep a Pull Request Draft when product validation is blocked or failing.
- Do not merge without a new explicit authorization naming the target PR.
- Design authority:
  `docs/superpowers/specs/2026-07-26-seven-repository-waef-rollout-design.md`.

## Complete Consumer-Contract Paths

Every target may create or modify:

1. `AGENTS.md`
2. `CODEOWNERS`
3. `.gitignore`
4. `CONTRIBUTING.md`
5. `.waef/waef.lock.yml`
6. `.waef/project.yml`
7. `.github/workflows/waef-compliance.yml`
8. `.github/ISSUE_TEMPLATE/waef-change.md`
9. `.github/pull_request_template.md`
10. `.waef/templates/VALIDATION_REPORT_TEMPLATE.md`
11. `.waef/templates/DESIGN_DOC_TEMPLATE.md`
12. `.waef/templates/ADR_TEMPLATE.md`
13. `.waef/templates/RELEASE_TEMPLATE.md`

For IRTC, LISTC, and WFC, path 14 is `.Rbuildignore`.

An existing `.github/PULL_REQUEST_TEMPLATE.md` is moved with `apply_patch` to
the canonical lowercase path before the WAEF block is appended. Existing bug,
feature, and documentation Issue templates remain unchanged.

## Exact Shared Adapter Content

Use the following exact bootstrap for `planned-project`:

```markdown
<!-- WAEF:START -->
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
<!-- markdownlint-disable-file MD041 -->
Read `.waef/waef.lock.yml` and use only its exact WAEF commit. Stop if
`.waef/cache/` is missing or does not match the lock.
Apply locked profile(s): planned-project. Project rules may strengthen but must not weaken
WAEF.
<!-- WAEF:END -->
```

Use the same text with the profile line exactly
`Apply locked profile(s): static-website. Project rules may strengthen but must not weaken`
for both static websites, exactly
`Apply locked profile(s): r-package. Project rules may strengthen but must not weaken`
for the three R packages, and exactly
`Apply locked profile(s): web-application. Project rules may strengthen but must not weaken`
for wechat-md-edit. The following `WAEF.` line remains unchanged.

Append this ownership block when the licensing declaration is
`PROPRIETARY.md`:

```text

# WAEF governance ownership
/AGENTS.md @weiandata/waef-maintainers
/.waef/ @weiandata/waef-maintainers
/.github/workflows/waef-compliance.yml @weiandata/waef-maintainers
/.github/workflows/ @weiandata/organization-governance
/CODEOWNERS @weiandata/organization-governance
/PROPRIETARY.md @weiandata/organization-governance
```

For R packages the final line is
`/DESCRIPTION @weiandata/organization-governance`. For wechat-md-edit it is
`/LICENSE @weiandata/organization-governance`. All preceding lines remain
identical.

Every lock uses schema `1`, framework `WAEF`, version `4.3`, repository
`weiandata/WAEF`, tag `v4.3`, and commit
`bd0eaa76490fd4e79f8ecb28a75dd0fdda6623e7`. Its one-item `profiles` array is
the literal profile named by the applicable repository task. Its `updated_by`
is the exact repository-local adoption PR URL returned by GitHub in Task 2.
Both dynamic values are applied together with `apply_patch`; the lock schema
and provenance check are the acceptance gate.

Append this block to each `.gitignore`:

```text

# WAEF local cache
.waef/cache/
```

Append this block to each `CONTRIBUTING.md`:

```markdown

<!-- WAEF:START -->
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
<!-- markdownlint-disable-file MD041 -->
Read `.waef/waef.lock.yml`, then follow the Issue, approved plan, categorized
branch, Pull Request, validation, accountable review, and release sequence.
<!-- WAEF:END -->
```

Create `.github/ISSUE_TEMPLATE/waef-change.md`:

```markdown
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# Issue: [one-line title]

## Problem

<!-- What is wrong or missing. -->

## Expected

<!-- What correct behavior looks like. -->

## Scope

<!-- In scope and out of scope. -->

## Acceptance Criteria

- [ ]

## Context

<!-- Related issues, documents, standards, and selected profile. -->
```

Append this block to a preserved Pull Request template, or use it as the whole
file when no template exists:

```markdown
<!-- WAEF:START -->
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# WAEF Review Evidence

## Related Issue

<!-- Use Closes, Fixes, or Resolves followed by a GitHub Issue reference. -->

## Scope

<!-- State the one logical change and explicit non-changes. -->

## Plan Reference

<!-- Link the approved implementation plan. -->

## Validation Report

<!-- Include fresh commands, exit codes, and acceptance-criterion evidence. -->

## Risks & Rollback

<!-- Describe known risks, migration, and recovery. -->

## AI Contribution

<!-- State whether AI contributed and what accountable human review remains. -->
<!-- WAEF:END -->
```

Create `.waef/templates/VALIDATION_REPORT_TEMPLATE.md`:

```markdown
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# Validation Report

## Commands & Results

| Command     | Exit code | Result   |
|-------------|-----------|----------|
| `<command>` | 0         | [result] |

## Acceptance Criteria

| Criterion   | Verdict     | Evidence   |
|-------------|-------------|------------|
| [criterion] | PASS / FAIL | [evidence] |

## Not Verified

<!-- Anything unverified and why. -->

## Verdict

<!-- Complete or Incomplete. -->
```

Create `.waef/templates/DESIGN_DOC_TEMPLATE.md`:

```markdown
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# Design: <feature/change title>

## Goal

## Non-Goals

## Current State

## Proposed Design

## Risks & Mitigations

## Validation Plan

## Rollout & Rollback
```

Create `.waef/templates/ADR_TEMPLATE.md`:

```markdown
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# ADR-[number]: [decision title]

## Context

## Decision

## Alternatives Considered

## Consequences
```

Create `.waef/templates/RELEASE_TEMPLATE.md`:

```markdown
<!-- WAEF-TEMPLATE-VERSION: 4.3 -->
# Release: v[version]

## Summary

## Changes

## Compatibility

## Verification

- [ ] CI green on the default branch
- [ ] Fresh release-candidate evidence is linked
- [ ] Human tag and publication approval is recorded

## Post-Release

- [ ] Published artifact is verified
- [ ] Rollback remains available
```

The public workflow must equal
`operations.waef.render_adapter.render_public_compliance_workflow()` from the
reviewed `.github` branch for the literal repository name and locked commit.
The private workflow must equal
`operations.waef.render_adapter.render_compliance_workflow()` for the locked
commit. Render to stdout, inspect it, and use `apply_patch`; do not redirect a
script into repository files.

---

### Task 1: Revise and Publish the Rollout Documentation

**Files:**

- Modify:
  `docs/superpowers/specs/2026-07-26-seven-repository-waef-rollout-design.md`
- Create:
  `docs/superpowers/plans/2026-07-26-seven-repository-waef-rollout.md`

**Interfaces:**

- Consumes: approved design commit `c8107d9` and the approved complete-contract
  scope.
- Produces: one `.github` documentation PR URL used as the exact plan reference
  in Tasks 2-8.

- [ ] Run `python3 handbook/tools/validate_handbook.py`; require `PASS`.
- [ ] Run `git diff origin/main...HEAD --check`; require exit 0.
- [ ] Confirm only the design and plan documents differ.
- [ ] Commit with `docs: complete seven-repository WAEF rollout plan`.
- [ ] Push `docs/seven-repo-waef-rollout` and open a draft `.github` PR.
- [ ] Put the handbook command, exit 0, and literal `Verdict: PASS` in the PR.
- [ ] Watch WAEF checks and mark Ready only when green.
- [ ] Record the exact documentation PR URL; do not merge without authorization.

### Task 2: Create the Seven Reservation Pull Requests

**Files:**

- No target repository files change in the reservation commits.

**Interfaces:**

- Consumes: current `origin/main` for each target.
- Produces: seven exact adoption PR URLs required by the lock schema.

- [ ] For each target, verify `git status -sb` is clean and fetch `origin/main`.
- [ ] Create branch `chore/adopt-waef-v4-3` in a repository-specific worktree:
  `data-reporting-ai-waef-v4-3`, `website-global-preview-waef-v4-3`,
  `website-AI-preview-waef-v4-3`, `IRTC-waef-v4-3`, `LISTC-waef-v4-3`,
  `WFC-waef-v4-3`, and `wechat-md-edit-waef-v4-3`.
- [ ] Commit `chore: reserve WAEF v4.3 rollout` with `--allow-empty`.
- [ ] Push each branch and open a draft PR titled
  `chore: adopt WAEF v4.3 governance`.
- [ ] For wechat-md-edit, explicitly use `--repo weiandata/wechat-md-edit`
  because the local checkout retains upstream `doocs/md` metadata.
- [ ] Record every exact PR URL. Do not predict PR numbers.

### Task 3: Adopt WAEF in data-reporting-ai

**Files:** the 13 complete consumer-contract paths.

**Interfaces:**

- Profile: `planned-project`
- Visibility: private
- Owner/status: `analytics-engineering` / `planned`
- Issues: data-reporting-ai `#1` through `#6`

- [ ] Run the external v4.3 validator before editing; require a non-zero red
  baseline containing the missing bootstrap contracts.
- [ ] Create the WAEF bootstrap with profile `planned-project`.
- [ ] Preserve `* @makunxiang-weiandata` and append governance CODEOWNERS for
  `/AGENTS.md`, `/.waef/`, the WAEF workflow, all workflows, `/CODEOWNERS`, and
  `/PROPRIETARY.md`.
- [ ] Add the exact shared cache, contribution, Issue, PR, and four `.waef`
  template adapters.
- [ ] Create the lock using the recorded data-reporting-ai adoption PR URL.
- [ ] Create project metadata:

```yaml
name: "data-reporting-ai"
owner: "analytics-engineering"
status: "planned"
purpose: "Hold the approved boundary for a planned data-reporting AI project"
risk: "low"
publication: "blocked"
language: "undecided"
```

- [ ] Apply the exact private workflow renderer output.
- [ ] Clone/check out the exact WAEF commit into ignored `.waef/cache`.
- [ ] Run checkout provenance, repository validation, Markdown validation, and
  `git diff --check`; require exit 0.
- [ ] Confirm only the 13 allowed paths differ.
- [ ] Commit `chore: adopt WAEF v4.3 governance`, push, and update the PR with
  closure lines for `#1` through `#6`, exact commands, exit 0, and
  `Verdict: PASS`.
- [ ] Watch Repository checks and WAEF; mark Ready only when green.

### Task 4: Adopt WAEF in website-global-preview

**Files:** the 13 complete consumer-contract paths.

**Interfaces:**

- Profile: `static-website`
- Visibility: public
- Owner/status: `web-engineering` / `active`
- Issues: website-global-preview `#1` through `#6`

- [ ] Capture the red v4.3 validation baseline.
- [ ] Add the complete shared adapters with bootstrap profile
  `static-website` and licensing ownership `/PROPRIETARY.md`.
- [ ] Create the lock using the recorded website-global-preview PR URL.
- [ ] Create project metadata:

```yaml
name: "website-global-preview"
owner: "web-engineering"
status: "active"
purpose: "Operate the bilingual WeianData static global website"
risk: "moderate"
publication: "allowed"
language: "Static HTML/JavaScript/Python"
```

- [ ] Apply public renderer output for literal repository
  `website-global-preview`.
- [ ] Run provenance validation, WAEF repository validation,
  `python3 scripts/validate_site.py`, and `git diff --check`.
- [ ] Require exit 0 and exactly the 13 allowed paths.
- [ ] Commit, push, add closure lines for `#1` through `#6`, publish PASS
  evidence, watch checks, and mark Ready only when green.

### Task 5: Adopt WAEF in website-AI-preview

**Files:** the 13 complete consumer-contract paths, including a case-only move
from `.github/PULL_REQUEST_TEMPLATE.md` to the canonical lowercase path.

**Interfaces:**

- Profile: `static-website`
- Visibility: public
- Owner/status: `web-engineering` / `active`
- Issues: website-AI-preview `#1` through `#6`

- [ ] Capture the red v4.3 validation baseline.
- [ ] Add the complete shared adapters with bootstrap profile
  `static-website` and licensing ownership `/PROPRIETARY.md`.
- [ ] Preserve the existing PR template, move it to lowercase with
  `apply_patch`, and append the exact WAEF review block.
- [ ] Create the lock using the recorded website-AI-preview PR URL.
- [ ] Create project metadata:

```yaml
name: "website-AI-preview"
owner: "web-engineering"
status: "active"
purpose: "Operate the bilingual WeianData AI Skills website"
risk: "controlled"
publication: "allowed"
language: "TypeScript/Next.js"
```

- [ ] Apply public renderer output for `website-AI-preview`.
- [ ] Run provenance and WAEF validation, then `npm ci`, `npm test`,
  `npm run lint`, `npm run typecheck`, `npm run build`, and
  `npm run test:static-output`.
- [ ] Require exit 0, no tracked npm changes, and only the 13 allowed paths.
- [ ] Commit, push, close `#1` through `#6`, publish PASS evidence, watch
  checks, and mark Ready only when green.

### Task 6: Adopt WAEF in IRTC

**Files:** the 13 complete paths plus `.Rbuildignore`.

**Interfaces:**

- Profile: `r-package`
- Visibility: public
- Owner/status: `package-maintainers` / `active`
- Issues: IRTC `#1` through `#6`

- [ ] Capture the red v4.3 validation baseline.
- [ ] Prepend the `r-package` bootstrap while preserving the full existing
  agent handoff.
- [ ] Add governance ownership with licensing path `/DESCRIPTION`.
- [ ] Add all shared adapters and `^\.waef$` to `.Rbuildignore`.
- [ ] Preserve and lowercase the existing PR template before appending WAEF.
- [ ] Create the lock from the recorded IRTC PR URL.
- [ ] Create project metadata:

```yaml
name: "IRTC"
owner: "package-maintainers"
status: "active"
purpose: "Provide item-response-theory analysis and reviewable reporting"
risk: "high"
publication: "allowed"
language: "R"
```

- [ ] Apply public renderer output for `IRTC`.
- [ ] Run provenance and WAEF validation, then
  `Rscript scripts/verify-release-1.1.R` and `git diff --check`.
- [ ] Require exit 0 and only the 14 allowed paths.
- [ ] Commit, push, close `#1` through `#6`, publish PASS evidence, watch all
  R and WAEF checks, and mark Ready only when green.

### Task 7: Adopt WAEF in LISTC

**Files:** the 13 complete paths plus `.Rbuildignore`.

**Interfaces:**

- Profile: `r-package`
- Visibility: public
- Owner/status: `statistics-engineering` / `active`
- Issues: LISTC `#1` through `#12`

- [ ] Capture the red v4.3 validation baseline.
- [ ] Create the `r-package` bootstrap.
- [ ] Add governance ownership with licensing path `/DESCRIPTION`.
- [ ] Add all shared adapters and both `^AGENTS\.md$` and `^\.waef$` to
  `.Rbuildignore`.
- [ ] Preserve and lowercase the existing PR template before appending WAEF.
- [ ] Create the lock from the recorded LISTC PR URL.
- [ ] Create project metadata:

```yaml
name: "LISTC"
owner: "statistics-engineering"
status: "active"
purpose: "Produce design-aware statistical pivot tables for assessment and survey data"
risk: "high"
publication: "allowed"
language: "R"
```

- [ ] Apply public renderer output for `LISTC`.
- [ ] Run provenance and WAEF validation,
  `Rscript -e 'devtools::test(stop_on_failure = TRUE)'`,
  `Rscript scripts/coverage.R`, and `git diff --check`.
- [ ] Require exit 0 and only the 14 allowed paths.
- [ ] Commit, push, close `#1` through `#12`, publish PASS evidence, watch all
  checks, and mark Ready only when green.

### Task 8: Adopt WAEF in WFC

**Files:** the 13 complete paths plus `.Rbuildignore`.

**Interfaces:**

- Profile: `r-package`
- Visibility: public
- Owner/status: `package-maintainers` / `active`
- Issues: WFC `#10` through `#15`

- [ ] Capture the red v4.3 validation baseline.
- [ ] Prepend the `r-package` bootstrap while preserving all ownership,
  authority, language, data, development, and Git policies.
- [ ] Add governance ownership with licensing path `/DESCRIPTION`.
- [ ] Add all shared adapters and `^\.waef$` to `.Rbuildignore`.
- [ ] Preserve and lowercase the existing PR template before appending WAEF.
- [ ] Create the lock from the recorded WFC PR URL.
- [ ] Create project metadata:

```yaml
name: "WFC"
owner: "package-maintainers"
status: "active"
purpose: "Provide controlled and reviewable survey weighting workflows"
risk: "controlled"
publication: "allowed"
language: "R"
```

- [ ] Apply public renderer output for `WFC`.
- [ ] Run provenance and WAEF validation,
  `Rscript -e 'devtools::test(stop_on_failure = TRUE)'`, and
  `git diff --check`.
- [ ] Require exit 0 and only the 14 allowed paths.
- [ ] Commit, push, close `#10` through `#15`, publish PASS evidence, watch all
  checks, and mark Ready only when green.

### Task 9: Adopt WAEF in wechat-md-edit

**Files:** the 13 complete consumer-contract paths.

**Interfaces:**

- Profile: `web-application`
- Visibility: private
- Owner/status: `web-engineering` / `active`
- Centrally routed Issues: `.github` `#21` through `#26`

- [ ] Capture the red v4.3 baseline against exactly
  `weiandata/wechat-md-edit`.
- [ ] Prepend the `web-application` bootstrap while preserving all existing
  Chinese monorepo instructions.
- [ ] Create `CODEOWNERS` with wildcard `@makunxiang-weiandata`, the five
  governance paths, and licensing ownership `/LICENSE`.
- [ ] Add all shared cache, contribution, Issue, PR, and `.waef` templates.
- [ ] Create the lock from the recorded wechat-md-edit PR URL.
- [ ] Create project metadata:

```yaml
name: "wechat-md-edit"
owner: "web-engineering"
status: "active"
purpose: "Maintain the web-based Markdown editor and its supported clients"
risk: "controlled"
publication: "allowed"
language: "TypeScript/Vue"
```

- [ ] Apply the exact private workflow renderer output.
- [ ] Run provenance and WAEF validation, `pnpm install --frozen-lockfile`,
  `pnpm exec eslint .`, `pnpm run type-check`, `pnpm test`, `pnpm web build`,
  and `git diff --check`.
- [ ] Require exit 0, no auto-fixed files, and only the 13 allowed paths.
- [ ] Commit and push explicitly to `weiandata/wechat-md-edit`.
- [ ] Put cross-repository closure lines for `.github#21` through
  `.github#26` in the PR, publish PASS evidence, watch checks, and mark Ready
  only when green.

### Task 10: Verify Ready State and Stop for Merge Authorization

**Files:** no changes.

**Interfaces:**

- Consumes: seven adoption PR URLs and exact HEAD SHAs.
- Produces: a final readiness table.

- [ ] Query each PR for URL, Draft state, mergeability, review decision, HEAD,
  and every check conclusion.
- [ ] Query each PR file list and require only its 13 or 14 allowed paths.
- [ ] Report any product-validation limitation explicitly.
- [ ] Stop and request merge authorization; do not infer ordinary merge or
  administrator bypass permission.

### Task 11: Merge Authorized Targets and Re-Audit

**Files:** no planned changes.

**Interfaces:**

- Consumes: explicit per-PR merge authorization.
- Produces: verified merge commits and a fresh organization baseline.

- [ ] Merge only named targets with `--match-head-commit`; use `--admin` only
  when explicitly authorized for that named PR.
- [ ] Verify each merged PR and its default-branch WAEF `push` run.
- [ ] After all seven are merged, dispatch `.github` workflow `313679449` on
  main and monitor it.
- [ ] Require 12 registered repositories, 12 compliant repositories, zero
  findings, and exit 0.
- [ ] Verify audit Issues close only after their finding is absent; report
  stale Issue state without mutating it unless separately authorized.
