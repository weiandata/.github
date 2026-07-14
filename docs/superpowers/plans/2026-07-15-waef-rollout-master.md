# WAEF Organization Rollout Master Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Release WAEF 4.0 and enforce its exact, review-controlled adoption across all existing and future WeianData repositories.

**Architecture:** WAEF owns standards, profiles, validators, and the reusable compliance workflow. The organization `.github` repository owns inventory, audit, upgrade automation, GitHub App operations, and rulesets; repository-template owns greenfield initialization; consuming repositories retain only a bootstrap, exact lock, generated adapters, and project-specific rules.

**Tech Stack:** Markdown, Python 3.11+, PyYAML 6.0.3, JSON, GitHub Actions, GitHub Apps, GitHub CLI/API, Git, R package checks, existing website and Handbook validators.

## Global Constraints

- Approved design: `.github/handbook/SPECIFICATION/2026-07-15-waef-organization-rollout-design.md`.
- Initial consumer version: exact WAEF `4.0`, tag `v4.0`, and the full immutable release commit SHA.
- WAEF is private and remains the only normative framework source.
- No consumer may reference `main`, `latest`, or a mutable WAEF tag without also verifying the immutable release SHA.
- WAEF upgrades open Pull Requests and never auto-merge.
- Repository-local rules may strengthen but may not silently weaken Handbook or WAEF MUST requirements.
- Authentication uses a least-privilege GitHub App, not a personal access token.
- Required checks fail closed; no implementation task may delete, skip, rename, or downgrade them to warnings.
- Existing project-specific AGENTS content must be preserved.
- LISTR is a planned statistical and engineering package; it uses the planned-project lifecycle until its language profile is approved.
- Do not publish, deploy, enable an organization-wide ruleset, or create external repositories without the explicit approval gate named in the relevant sub-plan.
- Do not use CodeGraph for this documentation- and configuration-led rollout.

---

## Plan Suite and Dependency Order

### Task 1: Build and release WAEF 4.0

**Plan:** `docs/superpowers/plans/2026-07-15-waef-4-framework.md`

**Produces:** lock/project schemas, validators, machine profiles, human+AI standards, behavioral scenarios, private reusable compliance workflow, and the immutable `v4.0` release commit.

- [ ] Execute the WAEF 4.0 plan through its release-readiness checkpoint.
- [ ] Record the full `v4.0` commit with `git -C WAEF rev-parse 'v4.0^{commit}'`.
- [ ] Confirm the release validator and all WAEF tests pass before any consumer adoption.

### Task 2: Build organization automation

**Plan:** `docs/superpowers/plans/2026-07-15-waef-organization-automation.md`

**Consumes:** WAEF validator interfaces and release metadata from Task 1.

**Produces:** repository inventory, daily audit, upgrade-PR automation, GitHub App runbook, sandbox integration evidence, and a staged ruleset definition.

- [ ] Implement and test automation locally against fixture GitHub responses.
- [ ] Verify the organization plan supports private-repository rulesets before applying any rule.
- [ ] Create the GitHub App and organization secrets only after the documented human approval checkpoint.

### Task 3: Make future projects compliant by construction

**Plan:** `docs/superpowers/plans/2026-07-15-waef-template-and-listr.md`

**Consumes:** exact WAEF 4.0 release SHA and organization workflow contract.

**Produces:** repository-template bootstrap, initializer, generated WAEF adapters, a sandbox proof, and LISTR as the first planned-project consumer.

- [ ] Make repository-template pass WAEF 4.0 before using it for any sandbox.
- [ ] Prove a generated sandbox becomes compliant without copying normative WAEF documents.
- [ ] Initialize LISTR with status `planned`; do not add business code or infer its eventual language.

### Task 4: Migrate existing repositories and activate enforcement

**Plan:** `docs/superpowers/plans/2026-07-15-waef-existing-repository-migration.md`

**Consumes:** tested WAEF 4.0, organization automation, repository adapters, and exact action pins from Tasks 1-3.

**Produces:** ten developed repositories pinned to WAEF 4.0, LISTR initialized, an 11/11 audit baseline, and an organization required-check ruleset.

- [ ] Pilot WAEF, repository-template, DCC, and website before broad migration.
- [ ] Migrate the remaining R packages, website-global-preview, and `.github` in separate reviewable Pull Requests.
- [ ] Run repository-specific tests and WAEF compliance in every repository.
- [ ] Enable the organization ruleset only after the baseline audit reports 11/11 compliant repositories.

## Cross-Plan Acceptance Gate

- [ ] `WAEF Compliance` is green and required on all eleven repositories.
- [ ] All locks identify WAEF `4.0`, `v4.0`, and the same verified release commit.
- [ ] Every developed repository has an approved domain profile; LISTR is explicitly `planned-project` until its language decision.
- [ ] Incorrect locks, missing evidence, red project CI, expired exceptions, and modified governance workflows block a sandbox Pull Request.
- [ ] The upgrade bot opens but does not merge a simulated WAEF upgrade Pull Request.
- [ ] The daily audit detects an added unregistered repository and a deliberately expired exception fixture.
- [ ] A rollback Pull Request restores the previous WAEF SHA without rewriting history.
- [ ] Final evidence lists every command, exit code, GitHub check URL, approval, and remaining environmental limitation.

## Execution Checkpoints

After each sub-plan:

1. run that plan's complete validation suite;
2. request a focused review of only that subsystem;
3. commit one logical change in the owning repository;
4. do not start the dependent plan until the produced interfaces and evidence are approved;
5. update this master checklist with the commit and validation report links.
