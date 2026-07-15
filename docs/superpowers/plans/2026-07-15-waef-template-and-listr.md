# WAEF Template and LISTR Greenfield Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make repository-template generate WAEF-compliant repositories and use LISTR as the first planned statistical-and-engineering-package consumer.

**Architecture:** The template stores a tested initializer and generated WAEF adapter files, not normative framework documents. Initialization writes project metadata, exact WAEF pins, profile-specific licensing, governance templates, and a thin workflow; planned-project mode blocks business development and publication until a language/domain profile is approved.

**Tech Stack:** Python 3.11+ standard library, YAML emitted as deterministic text, Markdown, GitHub Actions, existing template Markdown CI, WAEF 4.0 validator.

## Global Constraints

- Execute only after WAEF 4.0 produces an approved immutable `v4.0` commit.
- Work in repository-template on `feature/waef-project-initializer`; migrate LISTR in a separate `feature/initialize-listr` branch.
- Normative WAEF standards remain in the private WAEF repository; only generated GitHub-facing adapters are stored locally.
- The initializer must be deterministic and idempotent: a second identical run produces no diff.
- Template default state is `planned-project`, `publication: blocked`, with no inferred programming language.
- Generated active projects must choose at least one non-planned profile.
- Never overwrite text outside WAEF markers in an existing AGENTS or CONTRIBUTING file.
- The initializer may modify only the repository passed through `--root`; reject `/`, the home directory, and a dirty Git worktree unless `--allow-dirty` is explicitly provided.
- Do not create a sandbox or remote repository without the named human approval checkpoint.
- For initial adoption, open a draft Pull Request after the first generated adapter commit, capture `PR_URL=$(gh pr view --json url --jq .url)`, rerun the initializer with `--adoption-pr "$PR_URL"`, and require the final commit to pass; no provisional URL may reach the default branch.

---

### Task 1: Add the template's own WAEF 4.0 adoption contract

**Files:**
- Create: `repository-template/AGENTS.md`
- Create: `repository-template/.waef/waef.lock.yml`
- Create: `repository-template/.waef/project.yml`
- Create: `repository-template/.waef/templates/VALIDATION_REPORT.md`
- Create: `repository-template/.waef/templates/DESIGN_DOC.md`
- Create: `repository-template/.waef/templates/ADR.md`
- Create: `repository-template/.waef/templates/RELEASE.md`
- Create: `repository-template/.github/workflows/waef-compliance.yml`
- Modify: `repository-template/.gitignore`
- Modify: `repository-template/CODEOWNERS`
- Modify: `repository-template/CONTRIBUTING.md`
- Modify: `repository-template/.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `repository-template/.github/ISSUE_TEMPLATE/bug.md`
- Modify: `repository-template/.github/ISSUE_TEMPLATE/feature.md`
- Modify: `repository-template/.github/ISSUE_TEMPLATE/documentation.md`

**Interfaces:**
- Consumes: exact WAEF 4.0 commit and reusable workflow path.
- Produces: repository-template itself as a `repository-template` profile consumer.

- [ ] **Step 1: Generate the exact lock values from the release**

Run:

```bash
WAEF_COMMIT=$(git -C WAEF rev-parse 'v4.0^{commit}')
test "$(printf '%s' "$WAEF_COMMIT" | wc -c | tr -d ' ')" = 40
git -C WAEF show -s --format='%D' "$WAEF_COMMIT"
```

Expected: a 40-character commit and decoration containing `tag: v4.0`.

- [ ] **Step 2: Add bootstrap, lock, project metadata, and caller**

Set project metadata to name `repository-template`, owner `WeianData Engineering`, status `active`, risk `moderate`, publication `blocked`, language `language-neutral`, and profile `repository-template`. Render the reusable workflow reference and `waef_commit` input from the same `WAEF_COMMIT` value.

- [ ] **Step 3: Protect and expose human entry points**

Add `.waef/cache/` to `.gitignore`. Require governance owner review for AGENTS, `.waef/`, WAEF workflow, CODEOWNERS, licensing templates, and initializer code. Add WAEF version markers and required evidence fields to local Issue/PR adapters without removing current template-specific fields.

- [ ] **Step 4: Validate repository-template**

Run:

```bash
cd repository-template
python3 ../WAEF/scripts/validate_repository.py .
git diff --check
```

Expected: WAEF Compliance passes locally and no whitespace errors.

- [ ] **Step 5: Commit template adoption**

```bash
git -C repository-template add AGENTS.md .waef .github .gitignore CODEOWNERS CONTRIBUTING.md
git -C repository-template commit -m "feat: adopt WAEF 4.0 governance"
```

### Task 2: Build a deterministic project initializer with TDD

**Files:**
- Create: `repository-template/scripts/initialize_repository.py`
- Create: `repository-template/scripts/render_waef.py`
- Create: `repository-template/tests/test_initialize_repository.py`
- Create: `repository-template/tests/fixtures/planned-template/`
- Create: `repository-template/tests/fixtures/active-r-package/`
- Create: `repository-template/tests/fixtures/active-static-website/`
- Modify: `repository-template/scripts/README.md`
- Modify: `repository-template/README.md`

**Interfaces:**
- Produces CLI: `initialize_repository.py --root PATH --name NAME --owner OWNER --purpose TEXT --status STATUS --risk RISK --publication STATE --language LANGUAGE --profiles PROFILE... --waef-version VERSION --waef-tag TAG --waef-commit SHA --adoption-pr URL`.
- Produces files: AGENTS WAEF block, `.waef/waef.lock.yml`, `.waef/project.yml`, `.waef/templates/VALIDATION_REPORT.md`, `.waef/templates/DESIGN_DOC.md`, `.waef/templates/ADR.md`, `.waef/templates/RELEASE.md`, workflow caller, GitHub Issue/PR adapters, CODEOWNERS rules, CONTRIBUTING block, and selected licensing assets.

- [ ] **Step 1: Write failing initializer tests**

Test deterministic output, second-run no-op, dirty-worktree refusal, invalid SHA, version/tag mismatch, planned-project publication block, active project without domain profile, R-package GPL assets, static-site proprietary assets, WAEF marker preservation, and rejection of paths outside `--root`.

Run: `cd repository-template && python3 -m unittest tests.test_initialize_repository -v`

Expected: FAIL because the initializer does not exist.

- [ ] **Step 2: Implement pure rendering functions**

`render_waef.py` exposes `render_lock(config)`, `render_project(config)`, `render_workflow(config)`, `upsert_marked_block(text, block)`, and `render_codeowners(config)`. Sort keys and profiles deterministically; end every text file with one newline.

- [ ] **Step 3: Implement guarded filesystem application**

Build all output in memory, validate the configuration, print a file-by-file plan, and only then write. Use temporary files plus `Path.replace` for atomic replacement. Return exit 0 on change/no-op, 2 on invalid configuration, and 3 on dirty or unsafe root.

- [ ] **Step 4: Run tests and idempotence proof**

Run:

```bash
cd repository-template
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/initialize_repository.py --help
```

Expected: all tests PASS and help lists every required argument and exit code.

- [ ] **Step 5: Commit initializer**

```bash
git -C repository-template add scripts tests README.md
git -C repository-template commit -m "feat: initialize WAEF-compliant repositories"
```

### Task 3: Generate and validate local WAEF template adapters

**Files:**
- Create: `repository-template/templates/waef/AGENTS.block.md`
- Create: `repository-template/templates/waef/CONTRIBUTING.block.md`
- Create: `repository-template/templates/waef/PULL_REQUEST_TEMPLATE.md`
- Create: `repository-template/templates/waef/ISSUE_TEMPLATE.md`
- Create: `repository-template/templates/waef/VALIDATION_REPORT_TEMPLATE.md`
- Create: `repository-template/templates/waef/DESIGN_DOC_TEMPLATE.md`
- Create: `repository-template/templates/waef/ADR_TEMPLATE.md`
- Create: `repository-template/templates/waef/RELEASE_TEMPLATE.md`
- Create: `repository-template/tests/test_waef_templates.py`
- Create: `repository-template/templates/README.md`

**Interfaces:**
- Consumes: WAEF 4.0 template required-section contract.
- Produces: version-marked, project-extendable adapters used by the initializer.

- [ ] **Step 1: Write failing adapter tests**

Assert version marker, every WAEF required heading, no unresolved angle-bracket prompt in generated active files, and permission for project-specific sections after the required block.

- [ ] **Step 2: Add adapters without copying normative prose**

Keep each adapter limited to fields, checkboxes, and links necessary for GitHub/local rendering. Link to the exact WAEF lock rather than duplicating standards.

- [ ] **Step 3: Run template and initializer tests**

Run: `cd repository-template && python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all tests PASS.

- [ ] **Step 4: Commit generated adapters**

```bash
git -C repository-template add templates tests/test_waef_templates.py
git -C repository-template commit -m "feat: add generated WAEF adapters"
```

### Task 4: Prove greenfield generation in a local sandbox

**Files:**
- Create after execution: `repository-template/tests/generated/planned-project/` (test output, gitignored)
- Create after execution: `repository-template/tests/generated/r-package/` (test output, gitignored)
- Modify: `repository-template/.gitignore`
- Create: `repository-template/docs/waef-initialization-validation.md`

**Interfaces:**
- Produces: local proof that generated planned and R-package repositories pass WAEF without normative document copies.

- [ ] **Step 1: Generate both sandbox types**

Use the exact WAEF release values. Generate one `planned-project` with publication blocked and one active `r-package` with GPL assets.

- [ ] **Step 2: Validate both generated roots**

Run `python3 WAEF/scripts/validate_repository.py` against each root, then rerun the initializer and verify `git diff --no-index` reports no second-run change.

Expected: both validators exit 0 and the second initialization is a no-op.

- [ ] **Step 3: Record evidence and clean generated output**

Write exact commands and results to the validation document. Keep generated directories ignored and remove them after evidence is recorded.

- [ ] **Step 4: Commit local sandbox evidence**

```bash
git -C repository-template add .gitignore docs/waef-initialization-validation.md
git -C repository-template commit -m "test: validate WAEF project initialization"
```

### Task 5: Initialize LISTR as the first planned-project consumer

**Files:**
- Create: `LISTR/AGENTS.md`
- Create: `LISTR/.waef/waef.lock.yml`
- Create: `LISTR/.waef/project.yml`
- Create: `LISTR/.waef/templates/VALIDATION_REPORT.md`
- Create: `LISTR/.waef/templates/DESIGN_DOC.md`
- Create: `LISTR/.waef/templates/ADR.md`
- Create: `LISTR/.waef/templates/RELEASE.md`
- Create: `LISTR/.github/workflows/waef-compliance.yml`
- Modify: `LISTR/.gitignore`
- Modify: `LISTR/CODEOWNERS`
- Modify: `LISTR/CONTRIBUTING.md`
- Modify: `LISTR/README.md`
- Modify: `LISTR/.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `LISTR/.github/ISSUE_TEMPLATE/bug.md`
- Modify: `LISTR/.github/ISSUE_TEMPLATE/feature.md`
- Modify: `LISTR/.github/ISSUE_TEMPLATE/documentation.md`

**Interfaces:**
- Consumes: tested initializer and exact WAEF 4.0 release.
- Produces: LISTR status `planned`, profile `planned-project`, publication blocked, with no business language inferred.

- [ ] **Step 1: Create a dedicated LISTR branch and run the initializer**

Set name `LISTR`, owner `WeianData Engineering`, purpose `Planned statistical and engineering package`, status `planned`, risk `moderate`, publication `blocked`, language `undecided`, and profile `planned-project`.

- [ ] **Step 2: Replace template identity without adding product behavior**

Update README to state the approved purpose, planned status, owner, WAEF governance, and explicit gate: language/domain profile must be approved before business source, dependency manifest, release workflow, or publication is added.

- [ ] **Step 3: Validate LISTR and prove planned-project blocking**

Run:

```bash
python3 WAEF/scripts/validate_repository.py LISTR
test ! -f LISTR/DESCRIPTION
test ! -f LISTR/pyproject.toml
git -C LISTR diff --check
```

Expected: WAEF validation passes, no language manifest exists, and no whitespace errors.

- [ ] **Step 4: Commit LISTR initialization**

```bash
git -C LISTR add AGENTS.md .waef .github .gitignore CODEOWNERS CONTRIBUTING.md README.md
git -C LISTR commit -m "feat: initialize LISTR under WAEF 4.0"
```

### Task 6: Validate GitHub template creation after human approval

**Files:**
- Create: `repository-template/docs/waef-github-template-validation.md`
- Modify only if evidence reveals defects: files already listed in Tasks 1-4.

**Interfaces:**
- Produces: remote proof that GitHub's template operation preserves required files and the private reusable workflow can execute.

- [ ] **Step 1: Human external-state approval checkpoint**

Request approval to create the private `waef-compliance-sandbox` repository from repository-template. Do not create it before approval.

- [ ] **Step 2: Create, initialize, and open a test Pull Request**

Use GitHub's template mechanism, clone the result, run the initializer with a planned-project configuration, and open one PR changing only README status text.

- [ ] **Step 3: Verify remote controls**

Confirm WAEF Compliance and project CI run, protected files request the expected CODEOWNER, the PR cannot merge with a deliberately removed Plan Reference, and no normative WAEF document is committed.

- [ ] **Step 4: Record evidence and request cleanup approval**

Record repository/PR/check URLs and exact conclusions. Ask before deleting the private sandbox; retain the validation report in repository-template.

- [ ] **Step 5: Commit validation report**

```bash
git -C repository-template add docs/waef-github-template-validation.md
git -C repository-template commit -m "test: verify GitHub template WAEF controls"
```
