# WAEF 4.0 Candidate Bridge Sandbox Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a sandbox-only WAEF candidate workflow, freeze its reviewed commit, and use one temporary private repository to prove organization controls fail closed before the final `v4.0` tag exists.

**Architecture:** WAEF keeps its production `compliance.yml` and tag-provenance requirement unchanged. A separate `candidate-compliance.yml` is guarded to the exact sandbox repository, verifies exact candidate HEAD and 4.0 metadata, and runs the full repository validator; the validator accepts that caller only when project name is exactly `waef-compliance-sandbox`. Organization code gains a separate one-repository bridge audit path, while production inventory, production schedules, merge behavior, and release behavior remain unchanged.

**Tech Stack:** Python 3.11, PyYAML 6.0.3, GitHub Actions, GitHub CLI/API, Git, and the existing private Read and Automation GitHub Apps.

## Global Constraints

- Candidate workflow access is limited to caller context `weiandata/waef-compliance-sandbox`; GitHub documents that a called reusable workflow's `github` context is associated with its caller.
- The exact candidate commit is frozen only after WAEF tests, self-validation, hosted `WAEF Self Check`, and independent review pass.
- Production `.github/workflows/compliance.yml` continues to require `v4.0` tag-to-commit provenance.
- Production consumer callers and the sandbox candidate caller both cover `pull_request` and `push`; `pull_request_target`, `if: false`, renamed checks, and extra caller keys are forbidden.
- The sandbox is exactly `weiandata/waef-compliance-sandbox`, private, temporary, and non-template.
- Do not merge WAEF Pull Request #2 or any sandbox Pull Request.
- Do not create or publish `v4.0`, a GitHub Release, an organization ruleset, or a production schedule.
- Do not modify `operations/waef/repositories.json` or its eleven-repository production allowlist.
- Never expose secret values, private keys, installation tokens, authorization headers, or PEM content.
- Temporary additional App keys are stored only as encrypted sandbox secrets, deleted from disk immediately after entry, and revoked after evidence is retained.
- Sandbox deletion requires a separate human approval.

---

### Task 1: Add the sandbox-only WAEF candidate contract with TDD

**Files:**
- Create: `WAEF/.github/workflows/candidate-compliance.yml`
- Create: `WAEF/scripts/verify_candidate_checkout.py`
- Modify: `WAEF/validator/waef_validator/provenance.py`
- Modify: `WAEF/validator/waef_validator/repository.py`
- Modify: `WAEF/tests/python/test_workflows.py`
- Modify: `WAEF/tests/python/test_provenance.py`
- Modify: `WAEF/tests/python/test_repository.py`
- Modify: `WAEF/tests/fixtures/repository/complete/.github/workflows/waef-compliance.yml`
- Create: `WAEF/tests/fixtures/repository/candidate-sandbox/` from the complete fixture with project name `waef-compliance-sandbox` and candidate caller path.
- Modify: `WAEF/docs/governance/WAEF-4.0-validation-report.md`

**Interfaces:**
- Produces `validate_candidate_checkout(lock: Lock, checkout: Path) -> list[Finding]`.
- Produces reusable workflow `.github/workflows/candidate-compliance.yml` with the same two inputs and two secrets as production compliance.
- Changes repository caller validation so all normal projects require `compliance.yml@LOCK_COMMIT`, while only project name `waef-compliance-sandbox` may require `candidate-compliance.yml@LOCK_COMMIT`.

- [ ] **Step 1: Write failing workflow-contract tests**

Add assertions that `candidate-compliance.yml`:

```python
def test_candidate_workflow_is_sandbox_only_and_tag_independent(self) -> None:
    workflow, text = load("candidate-compliance.yml")
    call = workflow["on"]["workflow_call"]
    self.assertEqual({"lock_path", "waef_commit"}, set(call["inputs"]))
    self.assertEqual({"WAEF_APP_ID", "WAEF_APP_PRIVATE_KEY"}, set(call["secrets"]))
    self.assertEqual({"contents": "read"}, workflow["permissions"])
    steps = workflow["jobs"]["compliance"]["steps"]
    self.assertEqual("Restrict candidate workflow to the bridge sandbox", steps[0]["name"])
    self.assertIn('weiandata/waef-compliance-sandbox', steps[0]["run"])
    self.assertLess(text.index("Restrict candidate workflow"), text.index("create-github-app-token"))
    self.assertIn("verify_candidate_checkout.py", text)
    self.assertNotIn("verify_framework_checkout.py", text)
    self.assertImmutableActions(workflow)
```

Extend the shell-interpolation safety loop to include
`candidate-compliance.yml`.

- [ ] **Step 2: Write failing provenance and repository tests**

Add:

```python
def test_candidate_checkout_requires_head_and_metadata_but_not_release_tag(self):
    findings = validate_candidate_checkout(self.lock, self.checkout)
    self.assertEqual([], findings)

def test_only_exact_sandbox_project_accepts_candidate_caller(self):
    findings = validate_repository(FIXTURES / "candidate-sandbox", None, TODAY)
    self.assertEqual([], findings)

def test_normal_project_rejects_candidate_caller(self):
    # Copy the candidate fixture and change project.name to any other value.
    self.assertIn("WAEF-WORKFLOW-CALLER", {item.rule_id for item in findings})

def test_caller_requires_pull_request_and_push(self):
    # Remove push from the complete fixture caller.
    self.assertIn("WAEF-WORKFLOW-THIN-CALLER", {item.rule_id for item in findings})
```

- [ ] **Step 3: Run focused tests and confirm RED**

```bash
PYTHONPATH=validator python3 -m unittest \
  tests.python.test_workflows \
  tests.python.test_provenance \
  tests.python.test_repository -v
```

Expected: failures because the candidate workflow/function/fixture do not yet
exist and production caller validation still accepts pull-request-only.

- [ ] **Step 4: Implement candidate provenance**

Add to `provenance.py`:

```python
def validate_candidate_checkout(lock: Lock, checkout: Path) -> list[Finding]:
    findings: list[Finding] = []
    head = _git(checkout, "rev-parse", "HEAD")
    if head != lock.commit:
        findings.append(Finding("WAEF-CANDIDATE-HEAD", "error", "fetched candidate HEAD must equal lock commit", str(checkout)))
    readme = checkout / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    match = re.search(r"\*\*Version:\s*([0-9]+\.[0-9]+)", text)
    if match is None or match.group(1) != lock.version:
        findings.append(Finding("WAEF-CANDIDATE-METADATA", "error", "candidate metadata must equal lock version", str(readme)))
    return findings
```

`verify_candidate_checkout.py` mirrors `verify_framework_checkout.py` but calls
this function and never resolves a tag.

- [ ] **Step 5: Implement the guarded reusable workflow**

The first step runs with `CALLER_REPOSITORY: ${{ github.repository }}` and:

```bash
set -euo pipefail
test "${CALLER_REPOSITORY}" = "weiandata/waef-compliance-sandbox"
```

Only after the guard succeeds may the workflow create the Read App token,
checkout the caller, checkout exact WAEF source to `.waef/cache`, run
`verify_candidate_checkout.py`, install pinned requirements, and run
`validate_repository.py`. Job name remains `WAEF Compliance`, timeout is 15
minutes, and no artifact is uploaded.

- [ ] **Step 6: Align exact caller validation**

Change `_validate_workflow` to accept the loaded `Project` and compute:

```python
workflow_file = (
    "candidate-compliance.yml"
    if project.name == "waef-compliance-sandbox"
    else "compliance.yml"
)
expected_use = f"weiandata/WAEF/.github/workflows/{workflow_file}@{lock.commit}"
trigger_valid = trigger == ["pull_request", "push"] or trigger == {
    "pull_request": "",
    "push": "",
}
```

Keep the exact root keys, one `compliance` job, exact inputs/secrets, read-only
permissions, and no extra job keys. Pass `project` into `_validate_workflow` only
after both lock and project load successfully.

- [ ] **Step 7: Run full WAEF verification**

```bash
python3 -m pip install -r requirements.txt
PYTHONPATH=validator python3 -m unittest discover -s tests/python -p 'test_*.py' -v
PYTHONPATH=validator python3 scripts/validate_waef.py
git diff --check
```

Expected: all tests pass, 16 behavioral scenarios pass, ten profiles validate,
and no whitespace errors remain.

- [ ] **Step 8: Commit and push WAEF candidate change**

```bash
git add .github/workflows/candidate-compliance.yml scripts/verify_candidate_checkout.py \
  validator/waef_validator tests docs/governance/WAEF-4.0-validation-report.md
git commit -m "ci: add sandbox-only WAEF candidate validation"
git push origin feature/waef-4-framework
```

---

### Task 2: Review and freeze the new candidate SHA

**Files:**
- Modify: `.github/docs/superpowers/specs/2026-07-15-waef-candidate-bridge-sandbox-design.md`
- Modify: WAEF Pull Request #2 body.

**Interfaces:**
- Consumes: Task 1 commit and hosted checks.
- Produces: one reviewed immutable `CANDIDATE_COMMIT` used everywhere below.

- [ ] **Step 1: Verify hosted WAEF check and exact PR head**

```bash
gh pr checks 2 --repo weiandata/WAEF
CANDIDATE_COMMIT=$(gh pr view 2 --repo weiandata/WAEF --json headRefOid --jq .headRefOid)
test "$(printf '%s' "$CANDIDATE_COMMIT" | wc -c | tr -d ' ')" = 40
```

Expected: `WAEF Self Check` is successful and the SHA is 40 lowercase hex
characters.

- [ ] **Step 2: Run independent whole-branch review**

Review the complete WAEF PR #2 diff, emphasizing candidate caller isolation,
guard-before-token ordering, normal-project rejection, PR+push coverage, and
unchanged production tag provenance. Fix Critical or Important findings with
focused regression tests and repeat review.

- [ ] **Step 3: Freeze the reviewed SHA in durable records**

Replace the design's generated-candidate wording with the exact reviewed
`CANDIDATE_COMMIT`, update WAEF PR #2 validation evidence, and commit:

```bash
git add docs/superpowers/specs/2026-07-15-waef-candidate-bridge-sandbox-design.md
git commit -m "docs: freeze reviewed WAEF bridge candidate"
git push origin feature/waef-organization-automation
```

---

### Task 3: Add an isolated organization candidate-audit harness with TDD

**Files:**
- Create: `.github/operations/waef/sandbox_bridge.py`
- Create: `.github/operations/waef/tests/test_sandbox_bridge.py`
- Modify: `.github/operations/waef/GITHUB_APP.md`

**Interfaces:**
- Produces `audit_candidate_sandbox(read_client, issue_client, today, ref="main") -> AuditReport`.
- Reuses existing file, CODEOWNERS, exception, source-bound check, fingerprint, and Issue synchronization logic.
- Rejects any repository name other than `waef-compliance-sandbox` and any lock commit other than frozen `CANDIDATE_COMMIT`.

- [ ] **Step 1: Write failing isolation tests**

Tests must prove: production allowlist remains exactly eleven; only the sandbox
record is audited; another lock SHA yields `WAEF-BRIDGE-CANDIDATE`; a clean
candidate push run yields zero findings; branch refs can be audited for negative
scenarios; repeated identical findings create once and update once; and no tag
endpoint is called.

- [ ] **Step 2: Run focused test and confirm RED**

```bash
python3 -m unittest operations.waef.tests.test_sandbox_bridge -v
```

Expected: import failure because the module does not exist.

- [ ] **Step 3: Implement the sandbox-only module**

Hard-code the sandbox name and frozen candidate SHA. Fetch only the requested
sandbox ref, reuse existing validators, compare the lock SHA to the frozen
candidate, validate the exact candidate workflow caller, and reuse
`synchronize_findings()` only for sandbox findings. CLI subcommand `audit`
accepts `--ref`, `--today`, `--json-output`, `--markdown-output`, and
`--no-sync-issues`; it accepts no repository or SHA override.

- [ ] **Step 4: Verify and commit**

```bash
python3 -m unittest discover -s operations/waef/tests -p 'test_*.py' -v
python3 handbook/tools/validate_handbook.py
git diff --check
git add operations/waef/sandbox_bridge.py operations/waef/tests/test_sandbox_bridge.py operations/waef/GITHUB_APP.md
git commit -m "test: add WAEF candidate sandbox audit"
git push origin feature/waef-organization-automation
```

---

### Task 4: Create, credential, and seed the private sandbox

**Files:**
- Create in sandbox: minimal planned-project bootstrap, candidate caller, project CI, manual bridge audit/upgrade workflows, and generated adapters.

**Interfaces:**
- Consumes: frozen WAEF candidate SHA and exact `.github` bridge-harness commit.
- Produces: private repository with one clean source-bound default-branch push run.

- [ ] **Step 1: Create and verify the repository**

```bash
gh repo create weiandata/waef-compliance-sandbox --private \
  --description "Temporary WAEF 4.0 candidate bridge validation; no production data"
gh repo view weiandata/waef-compliance-sandbox \
  --json nameWithOwner,visibility,isTemplate,url
```

Expected: exact name, `PRIVATE`, and `isTemplate: false`.

- [ ] **Step 2: Apply the temporary App boundary**

Keep the Read App on all repositories; add only the sandbox to the Automation
App installation; generate one additional key for each existing App; set only
`WAEF_APP_ID`, `WAEF_APP_PRIVATE_KEY`, `WAEF_AUTOMATION_APP_ID`, and
`WAEF_AUTOMATION_APP_PRIVATE_KEY` as sandbox secrets; delete both PEM downloads
immediately; verify names only with `gh secret list`.

- [ ] **Step 3: Seed the exact candidate consumer**

Create project name `waef-compliance-sandbox`, owner `sandbox-validation`, status
`planned`, purpose `Validate the reviewed WAEF 4.0 candidate against organization
controls`, risk `controlled`, publication `blocked`, language `undecided`, and
profile `planned-project`. Lock and candidate caller both use frozen
`CANDIDATE_COMMIT`; the caller triggers on `pull_request` and `push` and invokes
`candidate-compliance.yml@CANDIDATE_COMMIT`. Add deterministic green project CI
and manual bridge workflows pinned to the exact Task 3 governance commit.

- [ ] **Step 4: Validate and push clean main**

```bash
python3 /Users/makunxiang/Developer/WeianData/.worktrees/WAEF-waef-4/scripts/validate_repository.py .
git diff --check
if rg -n 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|github_pat_|ghs_' .; then exit 1; fi
git add .
git commit -m "test: seed WAEF candidate bridge sandbox"
git push -u origin main
gh run list --repo weiandata/waef-compliance-sandbox --branch main --limit 10
```

Expected: local validation passes, credential scan is empty, and both WAEF
candidate compliance and project CI are successful at exact main HEAD.

---

### Task 5: Run negative scenarios, audit deduplication, and Draft upgrade

**Files:**
- Modify only on separate unmerged sandbox branches.

**Interfaces:**
- Produces attributable PR/check/run/Issue evidence for all eight approved scenarios.

- [ ] **Step 1: Open separate negative Pull Requests**

Use branches `sandbox/wrong-waef-sha`, `sandbox/missing-plan-evidence`,
`sandbox/expired-exception`, `sandbox/deleted-caller`,
`sandbox/renamed-caller`, `sandbox/removed-push-trigger`, `sandbox/if-false`, and
`sandbox/red-project-check`. Each branch changes only its named control and each
PR remains unmerged.

- [ ] **Step 2: Verify exact failure and unmerged state**

```bash
gh pr checks --repo weiandata/waef-compliance-sandbox "$PR_URL"
gh pr view --repo weiandata/waef-compliance-sandbox "$PR_URL" \
  --json url,state,isDraft,mergeStateStatus,headRefOid
```

Expected: the named rule/check fails, head SHA is recorded, and state is not merged.

- [ ] **Step 3: Prove fingerprint create/update behavior**

Run the manual bridge audit twice against the same deleted-caller ref with Issue
synchronization enabled. Expected: one Issue is created then updated with the
same 20-character fingerprint.

- [ ] **Step 4: Prove Draft-only upgrade behavior**

Use the sandbox-only manual workflow to call existing `upgrade_repository()`
directly for synthetic `4.1`/`v4.1` at the frozen candidate SHA, explicitly
labelled candidate-only and without production tag preflight. Expected: one
Draft PR, no merge, no auto-merge, no default-branch write, and blocked
provenance/version evidence.

- [ ] **Step 5: Inspect masked logs**

Inspect run logs without downloading artifacts. Expected: no PEM header, GitHub
token prefix, private key, or authorization header appears unmasked.

---

### Task 6: Record evidence and revoke temporary access

**Files:**
- Create: `.github/operations/waef/SANDBOX-VALIDATION.md`
- Modify: `.github/docs/superpowers/specs/2026-07-15-waef-candidate-bridge-sandbox-design.md`
- Modify: WAEF PR #2 and `.github` Draft PR #1 bodies.

**Interfaces:**
- Produces durable evidence while leaving sandbox deletion, final tag, merge, publication, production dispatch, and ruleset activation pending.

- [ ] **Step 1: Record exact evidence and limitations**

Record commands, exit codes, SHAs, URLs, conclusions, fingerprint behavior, App
scope, secret names, credential-log result, all unmerged states, and that final
`v4.0` tag provenance remains unverified.

- [ ] **Step 2: Revoke the validation credential boundary**

Delete four sandbox secrets, revoke both temporary App keys, and remove the
sandbox from the Automation App installation. Verify the Read App remains
read-only on all repositories. Do not delete the sandbox.

- [ ] **Step 3: Run final verification**

```bash
python3 -m unittest discover -s operations/waef/tests -p 'test_*.py' -v
python3 handbook/tools/validate_handbook.py
git diff --check
if rg -n --hidden --glob '!.git/**' 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|github_pat_|ghs_' .; then exit 1; fi
```

Expected: all tests and validators pass and no credential marker is found.

- [ ] **Step 4: Commit, push, and update Draft PRs**

```bash
git add operations/waef/SANDBOX-VALIDATION.md docs/superpowers/specs/2026-07-15-waef-candidate-bridge-sandbox-design.md
git commit -m "test: validate WAEF candidate bridge sandbox"
git push origin feature/waef-organization-automation
```

Mark only candidate bridge validation complete. Keep final tag provenance,
template-derived sandbox proof, WAEF Maintainer approval, merges, release,
production audit dispatch, ruleset activation, and sandbox deletion pending.
