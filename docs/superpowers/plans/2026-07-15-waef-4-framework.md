# WAEF 4.0 Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn WAEF 3.0 into a tested WAEF 4.0 framework that governs human and AI engineering work and can validate exact-version repository adoption.

**Architecture:** A small Python package loads YAML locks and project metadata, emits stable findings, applies machine-readable profile checks, and validates PR/release evidence. Markdown remains normative; a private reusable workflow checks out the caller and the exact WAEF release, then invokes the same validator used locally.

**Tech Stack:** Python 3.11+, PyYAML 6.0.3, `unittest`, JSON Schema documents, Markdown, GitHub Actions.

## Global Constraints

- Work in the `WAEF` repository on a `feature/waef-4-framework` branch.
- Preserve BT-001 through BT-011 and never reuse their identifiers.
- New mandatory scope requires MAJOR version `4.0`, changelog entry, and `docs/governance/WAEF-4.0-migration.md`.
- Stable validator output uses `Finding(rule_id, severity, message, path)` and severities `error`, `warning`, and `info`; compliance fails on any `error`.
- Lock SHA is authoritative; version, tag, workflow reference, and fetched metadata must agree with it.
- Use `yaml.safe_load`; never use unsafe YAML object construction.
- Pin PyYAML to `6.0.3`.
- Pin GitHub Actions by immutable commit. Use checkout v6 SHA `df4cb1c069e1874edd31b4311f1884172cec0e10` and create-github-app-token v2 SHA `fee1f7d63c2ff003460e3d139729b119787bc349`.
- No release tag, GitHub settings mutation, or push occurs without a human approval checkpoint.

---

### Task 1: Establish the validator package and lock contract

**Files:**
- Create: `WAEF/requirements.txt`
- Create: `WAEF/schemas/waef-lock.schema.json`
- Create: `WAEF/schemas/project.schema.json`
- Create: `WAEF/validator/waef_validator/__init__.py`
- Create: `WAEF/validator/waef_validator/models.py`
- Create: `WAEF/validator/waef_validator/lockfile.py`
- Create: `WAEF/tests/python/test_lockfile.py`
- Create: `WAEF/tests/fixtures/lock/valid/.waef/waef.lock.yml`
- Create: `WAEF/tests/fixtures/lock/mutable-ref/.waef/waef.lock.yml`
- Create: `WAEF/tests/fixtures/lock/mismatched-tag/.waef/waef.lock.yml`

**Interfaces:**
- Produces: `Lock`, `Project`, and `Finding` dataclasses; `load_lock(path: Path) -> Lock`; `validate_lock(lock: Lock, workflow_text: str) -> list[Finding]`.

- [ ] **Step 1: Write failing lock tests**

Cover a valid exact lock, missing 40-character SHA, `main`/`latest`, mismatched `version` and `tag`, duplicate profiles, missing `updated_by`, and a workflow reference that differs from `commit`.

Run: `cd WAEF && PYTHONPATH=validator python3 -m unittest tests.python.test_lockfile -v`

Expected: FAIL because `waef_validator.lockfile` does not exist.

- [ ] **Step 2: Add pinned YAML dependency and immutable models**

Write `requirements.txt` as:

```text
PyYAML==6.0.3
```

Define frozen dataclasses with exact fields from the design; reject unknown top-level lock keys so typos cannot silently pass.

- [ ] **Step 3: Implement strict lock loading and validation**

Require `schema`, `framework`, `version`, `repository`, `tag`, `commit`, `profiles`, and `updated_by`. Accept only `framework: WAEF`, `repository: weiandata/WAEF`, tag equal to `"v" + lock.version`, a lowercase 40-hex SHA, HTTPS GitHub PR URL for `updated_by`, and unique profile identifiers.

- [ ] **Step 4: Run lock tests**

Run: `cd WAEF && python3 -m pip install -r requirements.txt && PYTHONPATH=validator python3 -m unittest tests.python.test_lockfile -v`

Expected: all lock tests PASS.

- [ ] **Step 5: Commit the lock contract**

```bash
git -C WAEF add requirements.txt schemas validator tests/python/test_lockfile.py tests/fixtures/lock
git -C WAEF commit -m "feat: add exact WAEF lock validation"
```

### Task 2: Add project lifecycle and machine-readable profiles

**Files:**
- Create: `WAEF/profiles/manifest.yml`
- Create: `WAEF/validator/waef_validator/project.py`
- Create: `WAEF/validator/waef_validator/profiles.py`
- Create: `WAEF/tests/python/test_profiles.py`
- Create: `WAEF/tests/fixtures/profiles/r-package-pass/`
- Create: `WAEF/tests/fixtures/profiles/r-package-fail/`
- Create: `WAEF/tests/fixtures/profiles/static-website-pass/`
- Create: `WAEF/tests/fixtures/profiles/governance-framework-pass/`
- Create: `WAEF/tests/fixtures/profiles/repository-template-pass/`
- Create: `WAEF/tests/fixtures/profiles/planned-project-pass/`
- Modify: `WAEF/docs/project-profiles/README.md`
- Modify: `WAEF/docs/project-profiles/api-service.md`
- Modify: `WAEF/docs/project-profiles/cli-tool.md`
- Modify: `WAEF/docs/project-profiles/dataset.md`
- Modify: `WAEF/docs/project-profiles/python-library.md`
- Modify: `WAEF/docs/project-profiles/r-package.md`
- Modify: `WAEF/docs/project-profiles/research-repository.md`
- Modify: `WAEF/docs/project-profiles/static-website.md`
- Create: `WAEF/docs/project-profiles/governance-framework.md`
- Create: `WAEF/docs/project-profiles/repository-template.md`
- Create: `WAEF/docs/project-profiles/planned-project.md`

**Interfaces:**
- Consumes: `Finding` and lock profiles from Task 1.
- Produces: `load_project(path: Path) -> Project`; `validate_profiles(root: Path, project: Project, lock: Lock) -> list[Finding]`.

- [ ] **Step 1: Write failing profile tests**

Test R package GPL metadata and `inst/COPYRIGHTS`; static website proprietary notice and validator; governance framework owner/policy files; repository template initializer assets; and planned-project blocking of publication, release workflows, or business manifests.

Run: `cd WAEF && PYTHONPATH=validator python3 -m unittest tests.python.test_profiles -v`

Expected: FAIL because profile validation is absent.

- [ ] **Step 2: Define project metadata**

Require `.waef/project.yml` fields `name`, `owner`, `status`, `purpose`, `risk`, `publication`, and `language`. Allowed status values are `planned`, `active`, `maintenance`, `retired`, and `archived`; allowed risk values are `low`, `moderate`, `high`, and `controlled`.

- [ ] **Step 3: Define all profile checks in one manifest**

List the existing seven profiles plus `governance-framework`, `repository-template`, and `planned-project`. The manifest maps each profile to required paths, forbidden paths, content assertions, and profile-specific validation commands. Keep normative explanations in Markdown and machine predicates in `profiles/manifest.yml`.

- [ ] **Step 4: Implement profile validation**

Apply every selected profile and let the stricter result win. Permit `planned-project` only with `status: planned`, `publication: blocked`, no release/deploy workflow, and no language manifest or business source directory. Require a domain profile before status changes to `active`.

- [ ] **Step 5: Run profile tests and all Task 1 tests**

Run: `cd WAEF && PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v`

Expected: all tests PASS.

- [ ] **Step 6: Commit profiles**

```bash
git -C WAEF add profiles validator docs/project-profiles tests/python tests/fixtures/profiles
git -C WAEF commit -m "feat: add executable repository profiles"
```

### Task 3: Validate repository bootstrap, evidence, templates, and exceptions

**Files:**
- Create: `WAEF/validator/waef_validator/repository.py`
- Create: `WAEF/validator/waef_validator/evidence.py`
- Create: `WAEF/validator/waef_validator/exceptions.py`
- Create: `WAEF/validator/waef_validator/cli.py`
- Create: `WAEF/scripts/validate_repository.py`
- Create: `WAEF/tests/python/test_repository.py`
- Create: `WAEF/tests/python/test_evidence.py`
- Create: `WAEF/tests/python/test_exceptions.py`
- Create: `WAEF/tests/fixtures/repository/complete/`
- Create: `WAEF/tests/fixtures/repository/missing-plan/`
- Create: `WAEF/tests/fixtures/repository/expired-exception/`
- Modify: `WAEF/templates/ISSUE_TEMPLATE.md`
- Modify: `WAEF/templates/PULL_REQUEST_TEMPLATE.md`
- Modify: `WAEF/templates/VALIDATION_REPORT_TEMPLATE.md`
- Modify: `WAEF/templates/RELEASE_TEMPLATE.md`

**Interfaces:**
- Produces: `validate_repository(root: Path, event: dict | None, today: date) -> list[Finding]` and CLI exit 0 with no errors, exit 1 with compliance errors, exit 2 for invocation/configuration failure.

- [ ] **Step 1: Write failing repository tests**

Test required `AGENTS.md`, lock, project metadata, CONTRIBUTING WAEF reference, generated template version markers, workflow caller, CODEOWNERS protection, gitignored cache, PR Issue closure, branch prefix, required PR sections, validation results, exception approvals, and expiration.

- [ ] **Step 2: Implement repository and evidence validation**

Parse `GITHUB_EVENT_PATH` when present. Require PR sections `Related Issue`, `Scope`, `Plan Reference`, `Validation Report`, `Risks & Rollback`, and `AI Contribution`; accept `Closes`, `Fixes`, or `Resolves` followed by a GitHub Issue reference. Validate branch prefixes from WAEF Git Standard.

- [ ] **Step 3: Implement exception validation**

Require rule ID, rationale, Issue/ADR URL, Project Owner approval, WAEF Maintainer approval, creation date, and future expiration date. Reject wildcard rule IDs, missing approvals, and exceptions for secrets, confidential publication, direct default-branch pushes, or required-check removal.

- [ ] **Step 4: Add CLI and run all tests**

Run: `cd WAEF && PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v`

Expected: all tests PASS, and `python3 scripts/validate_repository.py tests/fixtures/repository/missing-plan` exits 1 with the stable missing-plan rule ID.

- [ ] **Step 5: Commit repository enforcement**

```bash
git -C WAEF add validator scripts templates tests
git -C WAEF commit -m "feat: validate WAEF repository evidence"
```

### Task 4: Expand WAEF standards from agents to the complete lifecycle

**Files:**
- Modify: `WAEF/AGENTS.md`
- Modify: `WAEF/README.md`
- Modify: `WAEF/docs/DEVELOPMENT_STANDARD.md`
- Modify: `WAEF/docs/GIT_STANDARD.md`
- Modify: `WAEF/docs/REVIEW_STANDARD.md`
- Modify: `WAEF/docs/TESTING_STANDARD.md`
- Modify: `WAEF/docs/SECURITY_STANDARD.md`
- Modify: `WAEF/docs/COPYRIGHT_LICENSING_STANDARD.md`
- Modify: `WAEF/skills/README.md`
- Modify: `WAEF/skills/code-review.md`
- Modify: `WAEF/skills/debugging.md`
- Modify: `WAEF/skills/implementation.md`
- Modify: `WAEF/skills/planning.md`
- Modify: `WAEF/skills/release-preparation.md`
- Modify: `WAEF/skills/repository-discovery.md`
- Modify: `WAEF/skills/requirement-analysis.md`
- Modify: `WAEF/skills/verification.md`
- Modify: `WAEF/templates/README.md`
- Modify: `WAEF/docs/governance/governance-model.md`

**Interfaces:**
- Consumes: stable validator rule IDs from Tasks 1-3.
- Produces: normative human+AI obligations that correspond one-to-one with executable checks where automation is possible.

- [ ] **Step 1: Update terminology and accountable roles**

Define WAEF Maintainer, Organization Governance, Project Owner, Contributor, AI Agent, and Reviewer. State explicitly that green CI is necessary but not sufficient and that human judgment remains responsible for business intent, root cause, architecture, security, statistics, and irreversible actions.

- [ ] **Step 2: Add exact lock, local bootstrap, exception, and upgrade rules**

Require repository bootstrap files, fail-closed behavior, exact pins, generated template adapters, protected governance ownership, and review-only upgrade Pull Requests.

- [ ] **Step 3: Reconcile branch categories**

Make WAEF Git Standard match the approved company categories already used by repository-template: `feature`, `fix`, `docs`, `refactor`, `test`, `release`, and `hotfix`. Record this breaking normalization in the migration guide.

- [ ] **Step 4: Review every MUST against validation coverage**

For automatable rules, record the validator rule ID. For judgment rules, record required evidence and reviewer role. Remove no security, evidence, or licensing obligation from 3.0.

- [ ] **Step 5: Commit the normative scope change**

```bash
git -C WAEF add AGENTS.md README.md docs skills templates
git -C WAEF commit -m "docs: expand WAEF to the engineering lifecycle"
```

### Task 5: Add WAEF 4.0 behavioral and self-validation tests

**Files:**
- Create: `WAEF/tests/scenarios/BT-012-version-drift.md`
- Create: `WAEF/tests/scenarios/BT-013-expired-exception.md`
- Create: `WAEF/tests/scenarios/BT-014-required-check-bypass.md`
- Create: `WAEF/tests/scenarios/BT-015-missing-human-approval.md`
- Create: `WAEF/tests/scenarios/BT-016-unsafe-framework-upgrade.md`
- Modify: `WAEF/tests/README.md`
- Create: `WAEF/scripts/validate_waef.py`
- Create: `WAEF/tests/python/test_validate_waef.py`

**Interfaces:**
- Produces: `validate_waef.py` self-check used by the release workflow and WAEF's own adoption.

- [ ] **Step 1: Write failing self-check tests**

Require version agreement across README/changelog/migration, valid internal links, all skills with Trigger/Inputs/Outputs/Mandatory Steps/Failure Conditions/Deliverables, all scenarios with Category/Setup/Task/Expected/Violations/References, unique BT IDs, and every profile in both documentation and machine manifest.

- [ ] **Step 2: Add BT-012 through BT-016**

Each scenario must name observable pass and failure behavior. BT-014 must reject deletion, renaming, or warning-only conversion of WAEF Compliance; BT-016 must reject automatic merging or mutable-ref upgrades.

- [ ] **Step 3: Implement and run the self-check**

Run: `cd WAEF && PYTHONPATH=validator python3 scripts/validate_waef.py`

Expected: exit 0, 16 structurally complete behavioral scenarios, all profiles indexed, and no broken internal path.

- [ ] **Step 4: Commit behavioral coverage**

```bash
git -C WAEF add tests scripts/validate_waef.py
git -C WAEF commit -m "test: cover WAEF 4 governance failures"
```

### Task 6: Add the private reusable compliance workflow

**Files:**
- Create: `WAEF/.github/workflows/compliance.yml`
- Create: `WAEF/.github/workflows/self-check.yml`
- Create: `WAEF/docs/governance/private-workflow-access.md`
- Create: `WAEF/tests/python/test_workflows.py`

**Interfaces:**
- Consumes: `scripts/validate_repository.py` and the exact lock commit.
- Produces: reusable job named `WAEF Compliance` and a self-check required on WAEF changes.

- [ ] **Step 1: Write workflow contract tests**

Parse both YAML files and assert least-privilege permissions, immutable action SHAs, pull-request and push coverage, timeout, exact input names, no `pull_request_target`, and no shell interpolation of untrusted PR body text.

- [ ] **Step 2: Implement reusable workflow**

Inputs are `waef_commit` and `lock_path` (default `.waef/waef.lock.yml`). Secrets are `WAEF_APP_ID` and `WAEF_APP_PRIVATE_KEY`. The job checks out the caller, creates a scoped App token, checks out `weiandata/WAEF` at `waef_commit` into `.waef/cache`, installs `requirements.txt`, and runs the repository validator with `GITHUB_EVENT_PATH`.

- [ ] **Step 3: Implement WAEF self-check workflow**

Use immutable checkout v6, Python 3, pinned requirements, unit tests, `validate_waef.py`, and `git diff --check`. Name the required job `WAEF Self Check`.

- [ ] **Step 4: Run workflow and unit validation**

Run: `cd WAEF && PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v && PYTHONPATH=validator python3 scripts/validate_waef.py`

Expected: all tests PASS and self-check exits 0.

- [ ] **Step 5: Commit workflows**

```bash
git -C WAEF add .github docs/governance/private-workflow-access.md tests/python/test_workflows.py
git -C WAEF commit -m "ci: add reusable WAEF compliance workflow"
```

### Task 7: Prepare and approve the WAEF 4.0 release

**Files:**
- Create: `WAEF/docs/governance/WAEF-4.0-migration.md`
- Create: `WAEF/docs/governance/WAEF-4.0-validation-report.md`
- Modify: `WAEF/CHANGELOG.md`
- Modify: `WAEF/README.md`

**Interfaces:**
- Produces after human approval: exact tag `v4.0` and immutable release commit used by every later plan.

- [ ] **Step 1: Write migration and validation reports**

Explain the human+AI scope, new bootstrap contract, branch-category normalization, new profiles, exact pins, exception process, reusable workflow, and migration from WAEF 3.0. Record every fresh command and result.

- [ ] **Step 2: Run final release verification**

Run:

```bash
cd WAEF
python3 -m pip install -r requirements.txt
PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v
PYTHONPATH=validator python3 scripts/validate_waef.py
git diff --check
git status --short
```

Expected: all tests pass, self-check exits 0, no whitespace errors, and status contains only planned release files.

- [ ] **Step 3: Human release approval checkpoint**

Present the full diff, migration guide, validation report, and proposed tag. Do not tag, push, or publish until the WAEF Maintainer explicitly approves.

- [ ] **Step 4: Tag only after approval**

Run: `git -C WAEF tag -a v4.0 -m "WAEF 4.0"`

Expected: `git -C WAEF rev-parse 'v4.0^{commit}'` prints the exact release commit later recorded in all locks.
