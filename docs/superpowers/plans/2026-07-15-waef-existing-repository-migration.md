# WAEF Existing Repository Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate every developed WeianData repository to the exact WAEF 4.0 contract, preserve project-specific knowledge, and enable organization-wide required checks only after an 11/11 green baseline.

**Architecture:** A tested adapter renderer inserts WAEF-owned blocks and generates exact locks/workflow callers per repository. Migration proceeds by pilot and profile waves; each repository retains its own CI and receives an independent Pull Request, validation report, approval, and rollback path.

**Tech Stack:** Git, WAEF 4.0 validator, Python 3, GitHub Actions, R/R CMD check, repository website validators, Handbook validator.

## Global Constraints

- Execute after the WAEF framework, organization automation, and template/LISTR plans pass their acceptance gates.
- Use one branch and Pull Request per repository; never combine repositories in one Git history.
- Exact profile map: DCC/IRTC/WFC/mergecalib/ratecalib=`r-package`; website/website-global-preview=`static-website`; WAEF/.github=`governance-framework`; repository-template=`repository-template`; LISTR=`planned-project`.
- Preserve all project-specific AGENTS rules; insert or replace only the WAEF-marked block.
- Pin WAEF workflow to the exact WAEF 4.0 commit.
- Pin existing external Actions to these immutable SHAs when their workflow files are touched:
  - actions/checkout v6: `df4cb1c069e1874edd31b4311f1884172cec0e10`
  - actions/checkout v4: `34e114876b0b11c390a56381ad16ebd13914f8d5`
  - actions/deploy-pages v4: `d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e`
  - actions/upload-artifact v4: `ea165f8d65b6e75b540449e92b4886f43607fa02`
  - actions/upload-pages-artifact v4: `7b1f4a764d45c48632c6b24a0339c27f5614fb0b`
  - markdownlint-cli2-action v23: `1628d9b2c73e580b4cb9b6b34303457a72478c5e`
  - lychee-action v2: `e7477775783ea5526144ba13e8db5eec57747ce8`
  - r-lib/actions v2: `d3c5be51b12e724e68f33216ca3c148b66d5f0b6`
- Preserve the readable version tag as a trailing YAML comment beside each action SHA.
- Do not change product APIs, algorithms, website business copy, statistical behavior, deployment targets, or release versions.
- Generated build/check output stays untracked and is removed after evidence is recorded.
- WAEF self-adoption occurs after the `v4.0` tag: the release commit cannot contain a lock pointing to its own hash, so a later normal Pull Request pins that immutable release.
- For every initial adoption, open a draft Pull Request after the first adapter commit, read its URL with `gh pr view --json url --jq .url`, rerender `updated_by` with that URL, and require the final commit to pass. Never leave a provisional value on the default branch.
- Do not enable an organization-wide ruleset until Task 7's audit passes 11/11.

---

### Task 1: Adopt released WAEF 4.0 in WAEF itself

**Files:**
- Modify: `WAEF/AGENTS.md`
- Create: `WAEF/.waef/waef.lock.yml`
- Create: `WAEF/.waef/project.yml`
- Create: `WAEF/.waef/templates/VALIDATION_REPORT.md`
- Create: `WAEF/.waef/templates/DESIGN_DOC.md`
- Create: `WAEF/.waef/templates/ADR.md`
- Create: `WAEF/.waef/templates/RELEASE.md`
- Create: `WAEF/.github/workflows/waef-compliance.yml`
- Create: `WAEF/.github/PULL_REQUEST_TEMPLATE.md`
- Create: `WAEF/.github/ISSUE_TEMPLATE/bug.md`
- Create: `WAEF/.github/ISSUE_TEMPLATE/feature.md`
- Create: `WAEF/.github/ISSUE_TEMPLATE/documentation.md`
- Create: `WAEF/CONTRIBUTING.md`
- Modify: `WAEF/CODEOWNERS`
- Create: `WAEF/.gitignore`

**Interfaces:**
- Consumes: immutable `v4.0` release commit from the framework plan.
- Produces: WAEF default branch governed by the last released WAEF version without a recursive Git hash.

- [ ] **Step 1: Create `feature/adopt-waef-4` after tagging v4.0**

Set project name WAEF, owner WeianData Engineering, status active, risk controlled, publication blocked, language Markdown/Python, and profile governance-framework. Pin the lock and reusable workflow to `git rev-parse 'v4.0^{commit}'`, not the post-release adoption commit.

- [ ] **Step 2: Open a draft adoption PR and finalize `updated_by`**

Commit the adapters, push the branch, open a draft PR, capture `PR_URL=$(gh pr view --json url --jq .url)`, rerender the lock with that URL, and commit the final lock. The draft may be red before the final URL commit; the final commit must be green.

- [ ] **Step 3: Run WAEF self and consumer validation**

Run:

```bash
cd WAEF
PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v
PYTHONPATH=validator python3 scripts/validate_waef.py
PYTHONPATH=validator python3 scripts/validate_repository.py .
git diff --check
```

Expected: framework tests, self-check, consumer compliance, and diff check all pass.

- [ ] **Step 4: Commit final WAEF adoption state**

```bash
git -C WAEF add AGENTS.md .waef .github .gitignore CODEOWNERS CONTRIBUTING.md
git -C WAEF commit -m "feat: adopt released WAEF 4.0"
```

### Task 2: Adopt WAEF in the DCC R-package pilot

**Files:**
- Modify: `DCC/AGENTS.md`
- Create: `DCC/.waef/waef.lock.yml`
- Create: `DCC/.waef/project.yml`
- Create: `DCC/.waef/templates/VALIDATION_REPORT.md`
- Create: `DCC/.waef/templates/DESIGN_DOC.md`
- Create: `DCC/.waef/templates/ADR.md`
- Create: `DCC/.waef/templates/RELEASE.md`
- Create: `DCC/.github/workflows/waef-compliance.yml`
- Modify: `DCC/.gitignore`
- Modify: `DCC/CODEOWNERS`
- Modify: `DCC/CONTRIBUTING.md`
- Modify: `DCC/.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `DCC/.github/ISSUE_TEMPLATE/bug.md`
- Modify: `DCC/.github/ISSUE_TEMPLATE/feature.md`
- Modify: `DCC/.github/ISSUE_TEMPLATE/documentation.md`
- Modify: `DCC/.github/workflows/ci.yml`
- Modify: `DCC/.github/workflows/r-check.yml`
- Modify: `DCC/.github/workflows/r-bench.yml`

**Interfaces:**
- Produces: first developed R-package adoption and feedback for the R-package profile.

- [ ] **Step 1: Create `feature/adopt-waef-4` and render adapters**

Set project name DCC, owner WeianData Engineering, status active, risk high, publication allowed, language R, and profile r-package. Insert the WAEF block above the existing DCC-specific AGENTS text.

- [ ] **Step 2: Protect governance and pin touched actions**

Add governance paths to CODEOWNERS, cache ignore, generated Issue/PR adapters, and immutable action SHAs. Do not alter R test matrices or benchmark commands.

- [ ] **Step 3: Run DCC validation**

Run:

```bash
python3 WAEF/scripts/validate_repository.py DCC
R CMD build DCC
DCC_VERSION=$(sed -n 's/^Version:[[:space:]]*//p' DCC/DESCRIPTION)
R CMD check --no-manual "DCC_${DCC_VERSION}.tar.gz"
git -C DCC diff --check
```

Expected: WAEF passes; build exits 0; check reports 0 ERROR and 0 WARNING or any pre-existing NOTE is recorded exactly; diff check passes.

- [ ] **Step 4: Commit DCC pilot**

```bash
git -C DCC add AGENTS.md .waef .github .gitignore CODEOWNERS CONTRIBUTING.md
git -C DCC commit -m "feat: adopt WAEF 4.0 governance"
```

### Task 3: Adopt WAEF in the website static-site pilot

**Files:**
- Create: `website/AGENTS.md`
- Create: `website/.waef/waef.lock.yml`
- Create: `website/.waef/project.yml`
- Create: `website/.waef/templates/VALIDATION_REPORT.md`
- Create: `website/.waef/templates/DESIGN_DOC.md`
- Create: `website/.waef/templates/ADR.md`
- Create: `website/.waef/templates/RELEASE.md`
- Create: `website/.github/workflows/waef-compliance.yml`
- Modify: `website/.gitignore`
- Modify: `website/CODEOWNERS`
- Modify: `website/CONTRIBUTING.md`
- Modify: `website/.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `website/.github/ISSUE_TEMPLATE/bug.md`
- Modify: `website/.github/ISSUE_TEMPLATE/feature.md`
- Modify: `website/.github/ISSUE_TEMPLATE/documentation.md`
- Modify: `website/.github/workflows/ci.yml`

**Interfaces:**
- Produces: first static-website adoption and proof that WAEF does not modify frozen business content.

- [ ] **Step 1: Create `feature/adopt-waef-4` and render static-site adapters**

Set owner WeianData, status active, risk high, publication allowed, language static HTML/JavaScript/Python validation, and profile static-website. Mark `articles/`, `articles-en/`, public legal text, production domain, and deployment configuration as protected/frozen unless the Issue explicitly scopes them.

- [ ] **Step 2: Pin actions without changing website behavior**

Replace action tags with the approved immutable SHAs and retain comments naming their readable versions. Do not change validator commands, production domain, HTML, article text, or deployment behavior.

- [ ] **Step 3: Run website validation**

Run:

```bash
python3 WAEF/scripts/validate_repository.py website
python3 website/scripts/validate_site.py
python3 website/scripts/validate_site.py --production
git -C website diff --check
```

Expected: WAEF and both website modes pass with no business-content diff.

- [ ] **Step 4: Commit website pilot**

```bash
git -C website add AGENTS.md .waef .github .gitignore CODEOWNERS CONTRIBUTING.md
git -C website commit -m "feat: adopt WAEF 4.0 governance"
```

### Task 4: Review pilot evidence before broad migration

**Files:**
- Create: `.github/operations/waef/PILOT-VALIDATION.md`
- Modify if required by a confirmed root cause: WAEF 4.0 or adapter files through their owning plans.

**Interfaces:**
- Consumes: WAEF, repository-template, DCC, and website pilot checks.
- Produces: explicit approval to start Wave 2.

- [ ] **Step 1: Compare all four pilot contracts**

Verify exact lock equality, workflow reference equality, profile behavior, CODEOWNERS, generated templates, project CI, and no copied normative documents.

- [ ] **Step 2: Run organization audit in pilot mode**

Run the audit with inventory filtered to WAEF, repository-template, DCC, and website.

Expected: 4/4 compliant and no expired exception.

- [ ] **Step 3: Root-cause any failure**

Fix a framework defect in WAEF, a generation defect in repository-template, an automation defect in `.github`, or a project adapter defect in the affected repository. Re-run all four pilots after any shared-layer fix.

- [ ] **Step 4: Human Wave 2 approval checkpoint**

Present pilot PR/check URLs and validation report. Do not migrate the remaining repositories until the WAEF Maintainer and Organization Governance owner approve Wave 2.

### Task 5: Migrate IRTC, WFC, mergecalib, and ratecalib independently

**Files per repository:**
- Modify: `IRTC/AGENTS.md`, `WFC/AGENTS.md`, `ratecalib/AGENTS.md`
- Create: `mergecalib/AGENTS.md`
- Create in each of IRTC, WFC, mergecalib, and ratecalib: `.waef/waef.lock.yml`, `.waef/project.yml`, and `.github/workflows/waef-compliance.yml`
- Create in each of IRTC, WFC, mergecalib, and ratecalib: `.waef/templates/VALIDATION_REPORT.md`, `.waef/templates/DESIGN_DOC.md`, `.waef/templates/ADR.md`, and `.waef/templates/RELEASE.md`
- Modify in each of IRTC, WFC, mergecalib, and ratecalib: `.gitignore`, `CODEOWNERS`, `CONTRIBUTING.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/bug.md`, `.github/ISSUE_TEMPLATE/feature.md`, and `.github/ISSUE_TEMPLATE/documentation.md`
- Modify: `IRTC/.github/workflows/ci.yml`, `IRTC/.github/workflows/r-check.yml`
- Modify: `WFC/.github/workflows/ci.yml`, `WFC/.github/workflows/R-CMD-check.yaml`, `WFC/.github/workflows/test-coverage.yaml`
- Modify: `mergecalib/.github/workflows/ci.yml`, `mergecalib/.github/workflows/R-CMD-check.yaml`, `mergecalib/.github/workflows/pkgdown.yaml`
- Modify: `ratecalib/.github/workflows/ci.yml`, `ratecalib/.github/workflows/R-CMD-check.yaml`

**Interfaces:**
- Produces: four separately reviewable R-package consumers.

- [ ] **Step 1: Migrate IRTC and validate**

Preserve current AGENTS text. Run:

```bash
python3 WAEF/scripts/validate_repository.py IRTC
R CMD build IRTC
IRTC_VERSION=$(sed -n 's/^Version:[[:space:]]*//p' IRTC/DESCRIPTION)
R CMD check --no-manual "IRTC_${IRTC_VERSION}.tar.gz"
git -C IRTC diff --check
```

Commit `feat: adopt WAEF 4.0 governance` only after fresh evidence.

- [ ] **Step 2: Migrate WFC and validate**

Preserve ownership, project authority, language, data, development, and Git policies in WFC/AGENTS.md. Run:

```bash
python3 WAEF/scripts/validate_repository.py WFC
R CMD build WFC
WFC_VERSION=$(sed -n 's/^Version:[[:space:]]*//p' WFC/DESCRIPTION)
R CMD check --no-manual "WFC_${WFC_VERSION}.tar.gz"
git -C WFC diff --check
```

- [ ] **Step 3: Migrate mergecalib and validate**

Create AGENTS from the WAEF bootstrap plus repository discovery facts; do not invent product rules. Run:

```bash
python3 WAEF/scripts/validate_repository.py mergecalib
R CMD build mergecalib
MERGECALIB_VERSION=$(sed -n 's/^Version:[[:space:]]*//p' mergecalib/DESCRIPTION)
R CMD check --no-manual "mergecalib_${MERGECALIB_VERSION}.tar.gz"
git -C mergecalib diff --check
```

- [ ] **Step 4: Migrate ratecalib and validate**

Preserve the full current AGENTS handoff document and insert only the WAEF block. Run:

```bash
python3 WAEF/scripts/validate_repository.py ratecalib
R CMD build ratecalib/package
RATECALIB_VERSION=$(sed -n 's/^Version:[[:space:]]*//p' ratecalib/package/DESCRIPTION)
R CMD check --no-manual "ratecalib_${RATECALIB_VERSION}.tar.gz"
git -C ratecalib diff --check
```

Expected: each repository passes WAEF, its R checks, and its existing CI; any package NOTE is recorded exactly and not mislabeled as PASS without review.

- [ ] **Step 5: Review four independent Pull Requests**

Require one PR, validation report, CODEOWNER review, and rollback statement per repository. Do not merge one repository merely because another passed.

### Task 6: Migrate website-global-preview and organization `.github`

**Files for website-global-preview:**
- Create: `website-global-preview/AGENTS.md`
- Create: `website-global-preview/.waef/waef.lock.yml`
- Create: `website-global-preview/.waef/project.yml`
- Create: `website-global-preview/.waef/templates/VALIDATION_REPORT.md`
- Create: `website-global-preview/.waef/templates/DESIGN_DOC.md`
- Create: `website-global-preview/.waef/templates/ADR.md`
- Create: `website-global-preview/.waef/templates/RELEASE.md`
- Create: `website-global-preview/.github/workflows/waef-compliance.yml`
- Create: `website-global-preview/.github/workflows/ci.yml`
- Modify: `website-global-preview/.gitignore`
- Modify: `website-global-preview/CODEOWNERS`
- Modify: `website-global-preview/CONTRIBUTING.md`
- Create: `website-global-preview/.github/PULL_REQUEST_TEMPLATE.md`
- Create: `website-global-preview/.github/ISSUE_TEMPLATE/bug.md`
- Create: `website-global-preview/.github/ISSUE_TEMPLATE/feature.md`
- Create: `website-global-preview/.github/ISSUE_TEMPLATE/documentation.md`

**Files for `.github`:**
- Create: `.github/AGENTS.md`
- Create: `.github/.waef/waef.lock.yml`
- Create: `.github/.waef/project.yml`
- Create: `.github/.waef/templates/VALIDATION_REPORT.md`
- Create: `.github/.waef/templates/DESIGN_DOC.md`
- Create: `.github/.waef/templates/ADR.md`
- Create: `.github/.waef/templates/RELEASE.md`
- Create: `.github/.github/workflows/waef-compliance.yml`
- Modify: `.github/.gitignore`
- Modify: `.github/CODEOWNERS`
- Modify: `.github/CONTRIBUTING.md`
- Create: `.github/.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/.github/ISSUE_TEMPLATE/bug.md`
- Create: `.github/.github/ISSUE_TEMPLATE/feature.md`
- Modify: `.github/.github/workflows/validate-handbook.yml`

**Interfaces:**
- Produces: remaining developed static site and governance repository consumers.

- [ ] **Step 1: Migrate website-global-preview**

Use static-website profile, protect both language article trees and deployment files, create a CI workflow that runs `python3 scripts/validate_site.py` plus existing Markdown/link checks, and pin all actions.

- [ ] **Step 2: Validate website-global-preview**

Run WAEF validator, `python3 website-global-preview/scripts/validate_site.py`, and diff check. Confirm no production content or Cloudflare configuration changed.

- [ ] **Step 3: Migrate `.github` as governance-framework**

Protect Handbook, rule registry, manifest, operations/waef, workflows, SECURITY, legal identity, and CODEOWNERS. Pin actions in validate-handbook without changing the command.

- [ ] **Step 4: Validate `.github`**

Run:

```bash
python3 WAEF/scripts/validate_repository.py .github
python3 .github/handbook/tools/validate_handbook.py
python3 -m unittest discover -s .github/operations/waef/tests -p 'test_*.py' -v
git -C .github diff --check
```

Expected: WAEF, Handbook, organization automation, and diff checks pass.

- [ ] **Step 5: Commit and review each repository independently**

Use `feat: adopt WAEF 4.0 governance` in website-global-preview and `.github`; attach separate validation reports.

### Task 7: Run the 11/11 baseline audit and activate the ruleset

**Files:**
- Create: `.github/operations/waef/BASELINE-2026-07-15.md`
- Modify after approval: live GitHub organization ruleset state through `operations/waef/apply_ruleset.py`; no repository file is silently rewritten.

**Interfaces:**
- Consumes: all ten developed migrations plus LISTR planned-project initialization.
- Produces: complete baseline evidence and active organization merge protection.

- [ ] **Step 1: Verify every default branch after merges**

Run daily audit logic against all inventory entries. Require 11/11 registered, owned, exactly pinned, profiled, CODEOWNERS-protected, and green on WAEF Compliance. Require zero expired exceptions and zero missing/renamed checks.

- [ ] **Step 2: Run deliberate negative checks in the approved sandbox**

Confirm wrong lock, missing plan, red project CI, expired exception, and deleted WAEF workflow each block merging. Confirm the upgrade bot opens but does not merge.

- [ ] **Step 3: Write the baseline report**

Record repository, profile/lifecycle, exact WAEF SHA, default-branch commit, WAEF check URL, project CI URL, CODEOWNER approval, exceptions, and verdict for all eleven repositories.

- [ ] **Step 4: Human organization-enforcement approval checkpoint**

Present baseline, ruleset JSON, plan preflight, negative-test evidence, rollback procedure, and GitHub App permissions. Do not activate without an Organization Owner's explicit approval.

- [ ] **Step 5: Activate and immediately re-audit**

Run `python3 operations/waef/apply_ruleset.py apply operations/waef/ruleset.json --enforcement active` from `.github`, then rerun the full audit.

Expected: the ruleset is active on all eleven default branches and the immediate audit remains 11/11 green.

- [ ] **Step 6: Commit final baseline evidence**

```bash
git -C .github add operations/waef/BASELINE-2026-07-15.md
git -C .github commit -m "docs: record WAEF 4 rollout baseline"
```

### Task 8: Exercise and document rollback

**Files:**
- Create: `.github/operations/waef/ROLLBACK-VALIDATION.md`

**Interfaces:**
- Produces: tested evidence that a consumer can restore its previous exact WAEF SHA through a normal Pull Request.

- [ ] **Step 1: Open a sandbox upgrade PR**

Move the approved sandbox from its current exact WAEF SHA to another signed test release through the upgrade bot. Require normal checks and human approval.

- [ ] **Step 2: Open a normal rollback PR**

Restore version, tag, commit, workflow reference, and generated template marker to the previous lock. Do not rewrite history or force-push.

- [ ] **Step 3: Verify rollback evidence**

Confirm WAEF Compliance and project CI pass, both PRs remain in history, audit reports the restored pin, and no exception was used.

- [ ] **Step 4: Commit rollback report**

```bash
git -C .github add operations/waef/ROLLBACK-VALIDATION.md
git -C .github commit -m "test: validate WAEF rollback workflow"
```
