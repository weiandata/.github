# WAEF Organization Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a least-privilege organization inventory, daily WAEF audit, reviewed upgrade-Pull-Request automation, and staged ruleset controls to `weiandata/.github`.

**Architecture:** A Python standard-library GitHub client and deterministic audit/upgrade modules consume a checked-in JSON repository inventory. GitHub Actions obtain short-lived installation tokens from a dedicated GitHub App; audit is read-mostly, while upgrade automation creates branches, commits, Issues, and Pull Requests without merging.

**Tech Stack:** Python 3.11+, `unittest`, JSON, GitHub REST API, GitHub Actions, GitHub App installation tokens, Engineering Handbook validator.

## Global Constraints

- Work in `.github` on a `feature/waef-organization-automation` branch based on the approved design commit.
- Consume the exact WAEF 4.0 release commit produced by the WAEF framework plan.
- GitHub App secrets are named `WAEF_APP_ID` and `WAEF_APP_PRIVATE_KEY`.
- No personal access token, mutable action reference, auto-merge, force-push, or automatic ruleset activation.
- Pin checkout v6 to `df4cb1c069e1874edd31b4311f1884172cec0e10` and create-github-app-token v2 to `fee1f7d63c2ff003460e3d139729b119787bc349`.
- Inventory is the reviewed registration authority; discovering an unregistered repository creates a failure, not an automatic silent addition.
- API clients must redact authorization values and never serialize private keys.
- Ruleset application is an explicit final human-approved operation after an 11/11 green audit.

---

### Task 1: Define the organization inventory and GitHub client

**Files:**
- Create: `.github/operations/waef/repositories.json`
- Create: `.github/operations/waef/github_client.py`
- Create: `.github/operations/waef/models.py`
- Create: `.github/operations/waef/tests/test_inventory.py`
- Create: `.github/operations/waef/tests/test_github_client.py`
- Create: `.github/operations/waef/tests/fixtures/organization-repositories.json`

**Interfaces:**
- Produces: `RepositoryRecord`, `AuditFinding`, `GitHubClient.request(method, path, body=None)`, and `load_inventory(path) -> list[RepositoryRecord]`.

- [ ] **Step 1: Write failing inventory tests**

Require exactly these eleven names: `.github`, `DCC`, `IRTC`, `LISTR`, `WAEF`, `WFC`, `mergecalib`, `ratecalib`, `repository-template`, `website`, and `website-global-preview`. Require owner, lifecycle, profiles, expected WAEF check, and migration wave; reject duplicates and unknown fields.

Run: `cd .github && python3 -m unittest operations.waef.tests.test_inventory -v`

Expected: FAIL because the operations package does not exist.

- [ ] **Step 2: Write the initial inventory**

Assign R-package profile to the five developed R packages; static-website to both websites; governance-framework to `.github` and WAEF; repository-template to repository-template; planned-project to LISTR. Record migration waves 1-3 from the approved design.

- [ ] **Step 3: Implement a redacting REST client**

Use `urllib.request`, `Authorization: Bearer`, `Accept: application/vnd.github+json`, and API version `2022-11-28`. Retry HTTP 429, 502, 503, and 504 at most three times using `Retry-After` or exponential delays 1, 2, and 4 seconds; do not retry 401, 403, 404, or validation errors.

- [ ] **Step 4: Run tests**

Run: `cd .github && python3 -m unittest operations.waef.tests.test_inventory operations.waef.tests.test_github_client -v`

Expected: all tests PASS with no token in captured logs.

- [ ] **Step 5: Commit inventory foundation**

```bash
git -C .github add operations/waef
git -C .github commit -m "feat: add WAEF repository inventory"
```

### Task 2: Implement the daily compliance audit

**Files:**
- Create: `.github/operations/waef/audit.py`
- Create: `.github/operations/waef/tests/test_audit.py`
- Create: `.github/operations/waef/tests/fixtures/compliant-repository.json`
- Create: `.github/operations/waef/tests/fixtures/drifted-repository.json`
- Create: `.github/.github/workflows/waef-audit.yml`
- Create: `.github/operations/waef/AUDIT.md`

**Interfaces:**
- Consumes: inventory and `GitHubClient` from Task 1.
- Produces: `audit_organization(client, inventory, today) -> AuditReport`; CLI JSON and Markdown reports; exit 0 when compliant and 1 when findings exist.

- [ ] **Step 1: Write failing audit tests**

Cover missing `AGENTS.md`, lock, project metadata, workflow caller, CODEOWNERS coverage, expected status check, owner, mismatched WAEF tag/SHA, expired exception, unregistered repository, archived repository handling, and issue deduplication.

- [ ] **Step 2: Implement repository and organization audit**

Read default-branch files through the contents API and check recent commit
status/check-runs. Bind audit evidence to a successful `push` workflow run at
the exact default-branch HEAD and the qualified governed workflow path. Compare
GitHub organization repository enumeration to the inventory. Produce stable
finding fingerprints from repository, rule ID, and path so repeated daily
failures update one Issue instead of creating duplicates.

- [ ] **Step 3: Implement daily workflow**

Trigger at `17 22 * * *` UTC (06:00 Asia/Kuala_Lumpur) and `workflow_dispatch`. Use immutable action SHAs, mint an installation token limited to the eleven repositories, run tests before the live audit, upload no secret-bearing artifact, and write the Markdown summary to `GITHUB_STEP_SUMMARY`.

- [ ] **Step 4: Run audit tests and Handbook validation**

Run:

```bash
cd .github
python3 -m unittest discover -s operations/waef/tests -p 'test_*.py' -v
python3 handbook/tools/validate_handbook.py
```

Expected: all automation tests PASS and Handbook validator exits 0.

- [ ] **Step 5: Commit daily audit**

```bash
git -C .github add operations/waef .github/workflows/waef-audit.yml
git -C .github commit -m "feat: audit WAEF compliance daily"
```

### Task 3: Implement reviewed WAEF upgrade Pull Requests

**Files:**
- Create: `.github/operations/waef/upgrade.py`
- Create: `.github/operations/waef/render_adapter.py`
- Create: `.github/operations/waef/tests/test_upgrade.py`
- Create: `.github/operations/waef/tests/test_render_adapter.py`
- Create: `.github/.github/workflows/waef-upgrade.yml`
- Create: `.github/operations/waef/UPGRADES.md`

**Interfaces:**
- Produces: `build_upgrade(repo: RepositoryRecord, version: str, tag: str, commit: str, migration_url: str, changed_rules: str, migration_steps: str) -> UpgradeChange`; `render_lock(version: str, tag: str, commit: str, profiles: Sequence[str], updated_by: str) -> str`; `render_workflow(commit: str) -> str`; branch name computed as `f"automation/waef-{version}"`; one Pull Request per inventory repository.

- [ ] **Step 1: Write failing upgrade tests**

Assert exact lock version/tag/commit, exact reusable workflow SHA, preservation of profiles and project-local AGENTS content, generated template version markers, one logical change, migration link, no auto-merge field, existing-PR reuse, and refusal of non-40-hex commits or a tag not equal to `"v" + version`.

- [ ] **Step 2: Implement deterministic adapter rendering**

Render only WAEF-owned blocks between markers `<!-- WAEF:START -->` and `<!-- WAEF:END -->`; fail if either marker is missing or duplicated. Never rewrite text outside those blocks.

- [ ] **Step 3: Implement upgrade branch and PR operations**

Use Git data and Pull Request APIs to create or update `f"automation/waef-{version}"`, commit with `f"chore: upgrade WAEF to {version}"`, and open a PR whose body lists old/new pins, changed MUST rules, migration URL, repository validation results, approval requirements, and rollback command. Never call a merge endpoint.

- [ ] **Step 4: Implement release-dispatch workflow**

Accept `workflow_dispatch` inputs `version`, `tag`, `commit`, `migration_url`,
`changed_rules`, and `migration_steps`. Pass them to shell commands only through
quoted environment variables. Before creating any remote branch, run unit tests
and call `git ls-remote` for both the direct and peeled tag refs; require the
peeled commit (or direct commit for a lightweight tag) to equal the `commit`
input.

- [ ] **Step 5: Run upgrade tests**

Run: `cd .github && python3 -m unittest operations.waef.tests.test_upgrade operations.waef.tests.test_render_adapter -v`

Expected: all tests PASS and mocked request history contains no merge or force-update request.

- [ ] **Step 6: Commit upgrade automation**

```bash
git -C .github add operations/waef .github/workflows/waef-upgrade.yml
git -C .github commit -m "feat: open reviewed WAEF upgrade PRs"
```

### Task 4: Document and configure the GitHub App safely

**Files:**
- Create: `.github/operations/waef/GITHUB_APP.md`
- Create: `.github/operations/waef/INCIDENTS.md`
- Modify: `.github/SECURITY.md`
- Modify: `.github/CODEOWNERS`

**Interfaces:**
- Produces: approved App permissions, secret distribution, rotation, revocation, incident, and recovery runbooks.

- [ ] **Step 1: Document separate validation and automation permissions**

Validation requires metadata read, contents read, checks read, and Actions read
to bind a successful check to the governed workflow path. Issue reporting uses
a separate repository-limited write token. Upgrade automation additionally
requires contents write, pull-requests write, issues write, and workflows write.
Prefer separate App installations or tokens when GitHub permission boundaries
allow it.

- [ ] **Step 2: Protect automation and secret-bearing configuration**

Add `operations/waef/`, `.github/workflows/waef-*.yml`, CODEOWNERS, SECURITY, and future ruleset definitions to governance ownership. Document annual key rotation and immediate revocation after suspected disclosure.

- [ ] **Step 3: Human external-state approval checkpoint**

Present the App name, repository selection, permissions, secret names, rotation owner, and incident contacts. Do not create the GitHub App or organization secrets until an Organization Owner explicitly approves.

- [ ] **Step 4: After approval, configure and verify without printing secrets**

Use GitHub settings to create the App and organization secrets with explicit repository access. Run only `gh secret list --org weiandata` to verify names; never run a command that outputs secret values.

- [ ] **Step 5: Commit runbooks**

```bash
git -C .github add operations/waef/GITHUB_APP.md operations/waef/INCIDENTS.md SECURITY.md CODEOWNERS
git -C .github commit -m "docs: define WAEF automation operations"
```

### Task 5: Define and stage the organization ruleset

**Files:**
- Create: `.github/operations/waef/ruleset.json`
- Create: `.github/operations/waef/apply_ruleset.py`
- Create: `.github/operations/waef/tests/test_ruleset.py`
- Create: `.github/operations/waef/RULESET.md`
- Modify: `.github/handbook/chapters/23-repository-governance.md`
- Modify: `.github/handbook/chapters/30-pull-request-standard.md`
- Modify: `.github/handbook/handbook-manifest.json`
- Modify: `.github/handbook/rule-registry.json`

**Interfaces:**
- Produces: a disabled/staged ruleset requiring WAEF Compliance, project CI, Pull Request review, code-owner review, resolved conversations, and no force pushes or deletions on default branches.

- [ ] **Step 1: Write failing ruleset tests**

Assert target branch `~DEFAULT_BRANCH`, required WAEF check source, strict required checks, minimum one approval, code-owner review, conversation resolution, blocked force pushes/deletions, no bypass actor, and initial enforcement `disabled`.

- [ ] **Step 2: Implement plan preflight**

`apply_ruleset.py preflight` calls the organization endpoint and reports the GitHub plan/features without mutating settings. If private-repository organization rulesets are unsupported, exit 2 and stop for an accountable platform decision.

- [ ] **Step 3: Add Handbook links and machine registry entries**

Make the Handbook point to WAEF as lifecycle enforcement without duplicating validator rules. Add stable Handbook rule identifiers for exact WAEF adoption and required compliance checks.

- [ ] **Step 4: Validate the staged ruleset and Handbook**

Run:

```bash
cd .github
python3 -m unittest discover -s operations/waef/tests -p 'test_*.py' -v
python3 handbook/tools/validate_handbook.py
python3 operations/waef/apply_ruleset.py validate operations/waef/ruleset.json
```

Expected: tests and Handbook validator pass; ruleset validation reports `enforcement: disabled`.

- [ ] **Step 5: Commit staged enforcement**

```bash
git -C .github add operations/waef handbook
git -C .github commit -m "feat: stage organization WAEF ruleset"
```

### Task 6: Prove automation in a private sandbox

**Files:**
- Create: `.github/operations/waef/SANDBOX-VALIDATION.md`
- Modify only if tests reveal a defect: files already listed in Tasks 1-5.

**Interfaces:**
- Produces: primary evidence that private reusable workflows, App tokens, audit, upgrade PRs, and fail-closed checks behave as designed.

- [ ] **Step 1: Human approval checkpoint for sandbox mutation**

Request approval to create a temporary private repository named `waef-compliance-sandbox` in `weiandata`. Do not create it without approval.

- [ ] **Step 2: Run positive and destructive scenarios**

Create the sandbox from repository-template after the template plan is ready. Prove one clean PR passes, then separate PRs with a wrong SHA, removed plan evidence, expired exception, deleted workflow, and red project check remain unmergeable.

- [ ] **Step 3: Test upgrade and audit behavior**

Dispatch an upgrade PR against the sandbox, confirm it remains unmerged, and confirm audit findings open/update one Issue per fingerprint.

- [ ] **Step 4: Record and review evidence**

Record workflow URLs, check conclusions, PR URLs, Issue deduplication, App installation scope, and credential-log inspection. Delete the sandbox only after explicit approval and after retaining the validation report.

- [ ] **Step 5: Commit the validation report**

```bash
git -C .github add operations/waef/SANDBOX-VALIDATION.md
git -C .github commit -m "test: validate WAEF automation sandbox"
```
