# WAEF Audit v4.3 Compatibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the eight false-positive WAEF audit findings affecting five compliant repositories while retaining exact workflow provenance, repository binding, and fail-closed version handling.

**Architecture:** Keep the current private reusable-workflow renderer and add one exact renderer for the approved public repository bridge. Select the renderer from trusted repository visibility plus the locked WAEF version. Normalize only the two GitHub-generated check names and two observed workflow-path representations, while continuing to require a successful push run of the exact source workflow at the current default-branch HEAD.

**Tech Stack:** Python 3 standard library, `unittest`, GitHub REST response fixtures, YAML rendered as exact text.

## Global Constraints

- Preserve the existing private reusable caller byte-for-byte.
- Treat repository metadata `private` as authoritative only when it is a Boolean; missing or malformed visibility must fail closed.
- Permit the public bridge for WAEF v4.2 only in `weiandata/.github`.
- Permit the public bridge for all public organization repositories at exactly WAEF v4.3.
- Reject unknown future WAEF versions until their workflow contract is explicitly implemented.
- Bind every accepted public bridge to both `weiandata/<repository>` and the exact 40-character lowercase lock commit.
- Accept check-run names only as `WAEF Compliance` or `compliance / WAEF Compliance`.
- Require at least one successful accepted check run, not exactly one.
- Accept source workflow paths only as `.github/workflows/waef-compliance.yml` or `.github/workflows/waef-compliance.yml@<default-branch>`.
- Continue requiring an exact successful `push` workflow run at the current default-branch HEAD.
- Do not change Issue synchronization or stale-Issue closure in this pull request.
- Do not weaken provenance, CODEOWNERS, lock, project metadata, lifecycle, or exception validation.

---

### Task 1: Add the exact public bridge renderer

**Files:**

- Modify: `operations/waef/render_adapter.py:12-40`
- Modify: `operations/waef/tests/test_render_adapter.py:1-65`

- [x] **Step 1: Create the implementation branch from the approved design**

Run:

```bash
git switch -c fix/waef-audit-v43-compatibility
git status --short --branch
```

Expected: the new branch starts at the approved design and implementation-plan commits with a clean worktree.

- [x] **Step 2: Write failing renderer contract tests**

Add these imports and constants to `operations/waef/tests/test_render_adapter.py`:

```python
from pathlib import Path

from operations.waef.render_adapter import (
    render_public_compliance_workflow,
    replace_waef_block,
    update_generated_version,
)


ROOT = Path(__file__).resolve().parents[3]
PUBLIC_BRIDGE_SOURCE_COMMIT = "3f61a59aace865b162f383a95ecb0372c23880e4"
V43_COMMIT = "bd0eaa761c9ca7b9c4801e0bfcae17e66c03210c"
```

Add these methods to `RenderAdapterTests`:

```python
    def test_renders_exact_repository_bound_public_bridge(self):
        source = (
            ROOT / ".github" / "workflows" / "waef-compliance.yml"
        ).read_text(encoding="utf-8")
        expected = source.replace(
            "weiandata/.github", "weiandata/DCC"
        ).replace(PUBLIC_BRIDGE_SOURCE_COMMIT, V43_COMMIT)

        rendered = render_public_compliance_workflow("DCC", V43_COMMIT)

        self.assertEqual(expected, rendered)

    def test_public_bridge_rejects_non_sha_commit(self):
        with self.assertRaisesRegex(
            ValueError, "full lowercase 40-character SHA"
        ):
            render_public_compliance_workflow("DCC", "main")

    def test_public_bridge_rejects_repository_injection(self):
        with self.assertRaisesRegex(ValueError, "valid GitHub repository name"):
            render_public_compliance_workflow(
                'DCC"\n          run: echo bypass',
                V43_COMMIT,
            )
```

- [x] **Step 3: Run the renderer tests and confirm the new API is absent**

Run:

```bash
python3 -m unittest operations.waef.tests.test_render_adapter -v
```

Expected: FAIL with an import error for `render_public_compliance_workflow`.

- [x] **Step 4: Implement the exact public bridge renderer**

Add the repository-name validator beside `COMMIT_RE` in `operations/waef/render_adapter.py`:

```python
REPOSITORY_RE = re.compile(r"[A-Za-z0-9._-]+")
```

Add this function immediately after `render_compliance_workflow`:

```python
def render_public_compliance_workflow(repository: str, commit: str) -> str:
    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError("repository must be a valid GitHub repository name")
    if not COMMIT_RE.fullmatch(commit):
        raise ValueError("workflow commit must be a full lowercase 40-character SHA")
    return (
        "name: WAEF Compliance\n"
        "on: [pull_request, push]\n"
        "permissions:\n"
        "  contents: read\n"
        "jobs:\n"
        "  compliance:\n"
        "    name: WAEF Compliance\n"
        "    runs-on: ubuntu-latest\n"
        "    timeout-minutes: 15\n"
        "    steps:\n"
        "      - name: Check out consumer repository\n"
        "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10\n"
        "        with:\n"
        "          persist-credentials: false\n"
        "\n"
        "      - name: Restrict public organization bridge\n"
        "        env:\n"
        "          CALLER_REPOSITORY: ${{ github.repository }}\n"
        "        run: |\n"
        "          set -euo pipefail\n"
        f'          test "${{CALLER_REPOSITORY}}" = "weiandata/{repository}"\n'
        "\n"
        "      - name: Create private WAEF read token\n"
        "        id: waef-token\n"
        "        uses: actions/create-github-app-token@f8d387b68d61c58ab83c6c016672934102569859\n"
        "        with:\n"
        "          app-id: ${{ secrets.WAEF_APP_ID }}\n"
        "          private-key: ${{ secrets.WAEF_APP_PRIVATE_KEY }}\n"
        "          owner: weiandata\n"
        "          repositories: WAEF\n"
        "\n"
        "      - name: Check out exact private WAEF source\n"
        "        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10\n"
        "        with:\n"
        "          repository: weiandata/WAEF\n"
        f"          ref: {commit}\n"
        "          token: ${{ steps.waef-token.outputs.token }}\n"
        "          path: .waef/cache\n"
        "          persist-credentials: false\n"
        "          fetch-depth: 0\n"
        "\n"
        "      - name: Verify exact private WAEF source\n"
        "        env:\n"
        "          WAEF_LOCK_PATH: .waef/waef.lock.yml\n"
        '        run: python3 .waef/cache/scripts/verify_framework_checkout.py --lock "$GITHUB_WORKSPACE/$WAEF_LOCK_PATH" --checkout .waef/cache\n'
        "\n"
        "      - name: Install pinned validator requirements\n"
        "        run: python3 -m pip install --disable-pip-version-check --requirement .waef/cache/requirements.txt\n"
        "\n"
        "      - name: Validate consumer repository\n"
        "        env:\n"
        "          WAEF_LOCK_PATH: .waef/waef.lock.yml\n"
        '        run: python3 .waef/cache/scripts/validate_repository.py "$GITHUB_WORKSPACE" --event "$GITHUB_EVENT_PATH" --lock-path "$WAEF_LOCK_PATH"\n'
    )
```

- [x] **Step 5: Run the renderer tests**

Run:

```bash
python3 -m unittest operations.waef.tests.test_render_adapter -v
```

Expected: all renderer adapter tests PASS.

- [x] **Step 6: Commit the renderer**

Run:

```bash
git add operations/waef/render_adapter.py operations/waef/tests/test_render_adapter.py
git commit -m "feat: render exact public WAEF bridge"
```

Expected: one focused commit containing the exact renderer and its contract tests.

---

### Task 2: Select workflow contracts by visibility and locked version

**Files:**

- Modify: `operations/waef/audit.py:12-25`
- Modify: `operations/waef/audit.py:233-251`
- Modify: `operations/waef/audit.py:589-606`
- Modify: `operations/waef/tests/fixtures/compliant-repository.json:2-7`
- Modify: `operations/waef/tests/test_audit.py:12-31`
- Modify: `operations/waef/tests/test_audit.py:278-321`

- [x] **Step 1: Make the legacy compliant fixture explicitly private**

Add `"private": true` to its repository metadata:

```json
  "repository": {
    "name": "DCC",
    "private": true,
    "archived": false,
    "default_branch": "main"
  },
```

This keeps the existing v4.0 private-caller fixture valid without treating absent visibility as private.

- [x] **Step 2: Add an independent public-bridge fixture helper**

Add to `operations/waef/tests/test_audit.py` below the date constant:

```python
PUBLIC_BRIDGE_SOURCE_COMMIT = "3f61a59aace865b162f383a95ecb0372c23880e4"
FIXTURE_COMMIT = "993ef1e41306146f62881106ab17cae2e23162f5"


def public_bridge(repository, commit=FIXTURE_COMMIT):
    source = (
        ROOT / ".github" / "workflows" / "waef-compliance.yml"
    ).read_text(encoding="utf-8")
    return source.replace(
        "weiandata/.github", f"weiandata/{repository}"
    ).replace(PUBLIC_BRIDGE_SOURCE_COMMIT, commit)


def public_fixture(repository, version):
    fixture = load_fixture("compliant-repository.json")
    fixture["repository"]["name"] = repository
    fixture["repository"]["private"] = False
    lock = fixture["files"][".waef/waef.lock.yml"]
    fixture["files"][".waef/waef.lock.yml"] = (
        lock.replace('version: "4.0"', f'version: "{version}"')
        .replace("tag: v4.0", f"tag: v{version}")
        .replace("weiandata/DCC", f"weiandata/{repository}")
    )
    fixture["files"][".github/workflows/waef-compliance.yml"] = public_bridge(
        repository
    )
    fixture["waef_tags"] = {
        f"v{version}": {"type": "commit", "sha": FIXTURE_COMMIT}
    }
    return fixture
```

The helper derives expected test text from the already approved `.github` bridge, not from the new production renderer.

- [x] **Step 3: Write the visibility/version matrix tests**

Add these tests after the commented-caller validation test:

```python
    def test_v43_public_repository_bridge_is_accepted(self):
        fixture = public_fixture("DCC", "4.3")
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertEqual((), report.findings)

    def test_v42_dotgithub_public_bridge_is_accepted(self):
        fixture = public_fixture(".github", "4.2")
        report = audit_organization(
            FakeGitHubClient(fixture),
            [
                record(
                    name=".github",
                    owner="organization-governance",
                    profiles=("governance-framework",),
                )
            ],
            TODAY,
            synchronize_issues=False,
        )
        self.assertNotIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )

    def test_v42_public_bridge_is_rejected_outside_dotgithub(self):
        fixture = public_fixture("DCC", "4.2")
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )

    def test_future_public_bridge_version_fails_closed(self):
        fixture = public_fixture("DCC", "4.4")
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )

    def test_public_bridge_bound_to_another_repository_is_rejected(self):
        fixture = public_fixture("DCC", "4.3")
        fixture["files"][
            ".github/workflows/waef-compliance.yml"
        ] = public_bridge("website")
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )

    def test_public_bridge_bound_to_another_commit_is_rejected(self):
        fixture = public_fixture("DCC", "4.3")
        fixture["files"][
            ".github/workflows/waef-compliance.yml"
        ] = public_bridge("DCC", "a" * 40)
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )

    def test_missing_repository_visibility_fails_closed(self):
        fixture = load_fixture("compliant-repository.json")
        del fixture["repository"]["private"]
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-WORKFLOW",
            {finding.rule_id for finding in report.findings},
        )
```

- [x] **Step 4: Run the audit tests and confirm the matrix fails**

Run:

```bash
python3 -m unittest operations.waef.tests.test_audit -v
```

Expected: the new public bridge acceptance tests FAIL because audit validation still expects only the private reusable caller. The rejection tests should already pass.

- [x] **Step 5: Import the public renderer**

Change the renderer import in `operations/waef/audit.py` to:

```python
from operations.waef.render_adapter import (
    render_compliance_workflow,
    render_public_compliance_workflow,
)
```

- [x] **Step 6: Implement fail-closed dual-mode workflow validation**

Replace `_validate_workflow` with:

```python
def _validate_workflow(
    repository: str,
    text: str | None,
    lock: dict[str, Any] | None,
    repository_private: bool | None,
) -> list[AuditFinding]:
    if text is None:
        return [
            _finding(repository, "WAEF-AUDIT-WORKFLOW", "missing WAEF workflow")
        ]
    if lock is None or not COMMIT_RE.fullmatch(str(lock.get("commit", ""))):
        return [
            _finding(
                repository,
                "WAEF-AUDIT-WORKFLOW",
                "cannot validate workflow without a valid lock commit",
            )
        ]
    if repository_private is None:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-WORKFLOW",
                "cannot validate workflow without Boolean repository visibility",
            )
        ]

    commit = lock["commit"]
    version = str(lock.get("version", ""))
    if repository_private:
        expected = render_compliance_workflow(commit)
    elif version == "4.2" and repository == ".github":
        expected = render_public_compliance_workflow(repository, commit)
    elif version == "4.3":
        expected = render_public_compliance_workflow(repository, commit)
    else:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-WORKFLOW",
                f"public bridge is not authorized for locked WAEF {version or 'unknown'}",
            )
        ]

    if text != expected:
        return [
            _finding(
                repository,
                "WAEF-AUDIT-WORKFLOW",
                "workflow does not exactly match the authorized locked WAEF renderer",
            )
        ]
    return []
```

At the repository audit call site, normalize metadata without guessing:

```python
        raw_private = metadata.get("private")
        repository_private = (
            raw_private if isinstance(raw_private, bool) else None
        )
        findings.extend(
            _validate_workflow(
                record.name,
                workflow,
                lock,
                repository_private,
            )
        )
```

- [x] **Step 7: Run the audit and renderer tests**

Run:

```bash
python3 -m unittest operations.waef.tests.test_audit operations.waef.tests.test_render_adapter -v
```

Expected: all tests PASS, including legacy private v4.0, public `.github` v4.2, public DCC v4.3, repository binding, commit binding, missing visibility, and future-version rejection.

- [x] **Step 8: Commit the workflow selection**

Run:

```bash
git add operations/waef/audit.py operations/waef/tests/test_audit.py operations/waef/tests/fixtures/compliant-repository.json
git commit -m "fix: validate WAEF workflows by visibility"
```

Expected: one focused commit for the renderer selection matrix.

---

### Task 3: Accept canonical GitHub check evidence without weakening provenance

**Files:**

- Modify: `operations/waef/audit.py:380-442`
- Modify: `operations/waef/tests/fixtures/compliant-repository.json:20-27`
- Modify: `operations/waef/tests/test_audit.py:303-370`

- [x] **Step 1: Move the compliant fixture to GitHub's current workflow-path representation**

Change:

```json
"path": ".github/workflows/waef-compliance.yml@main"
```

to:

```json
"path": ".github/workflows/waef-compliance.yml"
```

- [x] **Step 2: Add failing check-name and path compatibility tests**

Add these tests near the existing spoofed-check tests:

```python
    def test_reusable_workflow_check_name_is_accepted(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["check_runs"] = [
            {
                "name": "compliance / WAEF Compliance",
                "conclusion": "success",
                "status": "completed",
            }
        ]
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertEqual((), report.findings)

    def test_multiple_successful_official_check_runs_are_accepted(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["check_runs"] = [
            {
                "name": "compliance / WAEF Compliance",
                "conclusion": "success",
                "status": "completed",
            },
            {
                "name": "compliance / WAEF Compliance",
                "conclusion": "success",
                "status": "completed",
            },
        ]
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertEqual((), report.findings)

    def test_legacy_default_branch_workflow_path_is_accepted(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["workflow_runs"][0]["path"] = (
            ".github/workflows/waef-compliance.yml@main"
        )
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertEqual((), report.findings)

    def test_failed_official_check_is_rejected(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["check_runs"] = [
            {
                "name": "compliance / WAEF Compliance",
                "conclusion": "failure",
                "status": "completed",
            }
        ]
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-CHECK",
            {finding.rule_id for finding in report.findings},
        )

    def test_successful_similarly_named_check_is_rejected(self):
        fixture = load_fixture("compliant-repository.json")
        fixture["check_runs"] = [
            {
                "name": "prefix / WAEF Compliance",
                "conclusion": "success",
                "status": "completed",
            }
        ]
        report = audit_organization(
            FakeGitHubClient(fixture),
            [record()],
            TODAY,
            synchronize_issues=False,
        )
        self.assertIn(
            "WAEF-AUDIT-CHECK",
            {finding.rule_id for finding in report.findings},
        )
```

Keep these existing negative tests unchanged:

- `test_same_name_check_from_another_workflow_is_rejected`
- `test_pull_request_run_is_not_default_branch_evidence`
- `test_workflow_run_from_another_ref_is_rejected`
- `test_workflow_run_query_is_limited_to_default_branch_push_head`

- [x] **Step 3: Run the audit tests and confirm compatibility failures**

Run:

```bash
python3 -m unittest operations.waef.tests.test_audit -v
```

Expected: FAIL for the reusable-workflow check name, duplicate official checks, and current no-suffix source path. The legacy suffixed path and negative provenance tests should pass.

- [x] **Step 4: Accept the two exact check names and at least one success**

Replace the exact-one matching block in `_validate_check` with:

```python
    accepted_check_names = {
        record.expected_waef_check,
        f"compliance / {record.expected_waef_check}",
    }
    matching = [
        run for run in runs if run.get("name") in accepted_check_names
    ]
    successful_checks = [
        run
        for run in matching
        if run.get("status") == "completed"
        and run.get("conclusion") == "success"
    ]
    if not successful_checks:
        return [
            _finding(
                record.name,
                "WAEF-AUDIT-CHECK",
                "current default-branch HEAD lacks a successful official WAEF check",
            )
        ]
```

This permits GitHub's reusable-workflow display name and duplicate successful reruns but does not accept arbitrary prefixes or partial matches.

- [x] **Step 5: Accept only the two observed source-path representations**

Before constructing `source_runs`, add:

```python
    accepted_workflow_paths = {
        WORKFLOW_PATH,
        f"{WORKFLOW_PATH}@{default_branch}",
    }
```

Change the path predicate and cardinality check to:

```python
        if run.get("path") in accepted_workflow_paths
```

and:

```python
    if not source_runs:
```

Keep all other predicates unchanged: exact workflow name, default branch, current HEAD SHA, `push` event, completed status, and successful conclusion.

- [x] **Step 6: Run the focused audit tests**

Run:

```bash
python3 -m unittest operations.waef.tests.test_audit -v
```

Expected: all audit tests PASS. In particular, both path forms and both exact check names pass, while a spoofed workflow, PR-only run, other ref, failed official check, and similarly named check fail.

- [x] **Step 7: Commit the evidence normalization**

Run:

```bash
git add operations/waef/audit.py operations/waef/tests/test_audit.py operations/waef/tests/fixtures/compliant-repository.json
git commit -m "fix: accept canonical GitHub WAEF check evidence"
```

Expected: one focused commit for check evidence compatibility.

---

### Task 4: Verify the complete audit change and prepare review

**Files:**

- Verify: `operations/waef/render_adapter.py`
- Verify: `operations/waef/audit.py`
- Verify: `operations/waef/tests/test_render_adapter.py`
- Verify: `operations/waef/tests/test_audit.py`
- Verify: `operations/waef/tests/fixtures/compliant-repository.json`
- Verify: `docs/superpowers/specs/2026-07-26-waef-audit-v43-compatibility-design.md`
- Verify: `docs/superpowers/plans/2026-07-26-waef-audit-v43-compatibility.md`

- [x] **Step 1: Run the complete Python test suite**

Run:

```bash
python3 -m unittest discover -s operations/waef/tests -p "test_*.py" -v
```

Expected: every WAEF operations test PASS.

- [x] **Step 2: Validate the governance handbook**

Run:

```bash
python3 handbook/tools/validate_handbook.py
```

Expected:

```text
PASS: validated 55 Markdown files, 37 chapters, and 38 stable identifiers
```

If the counts increase because this plan is included by the validator, require `PASS` and record the new exact counts in the pull request.

- [x] **Step 3: Check formatting and unintended changes**

Run:

```bash
git diff --check origin/main...HEAD
git status --short
git log --oneline --decorate origin/main..HEAD
```

Expected: no whitespace errors, a clean worktree, and only the design commit, plan commit, and three focused implementation commits.

- [x] **Step 4: Review the security invariants in the final diff**

Run:

```bash
git diff --stat origin/main...HEAD
git diff origin/main...HEAD -- operations/waef/render_adapter.py operations/waef/audit.py operations/waef/tests
```

Confirm all of the following before publishing:

- Private repositories still require the original exact reusable caller.
- Public v4.2 is accepted only for `.github`.
- Public v4.3 is accepted only through the exact repository-bound bridge.
- Public v4.4 and missing visibility fail closed.
- The bridge action SHAs, repository guard, and locked WAEF ref are exact.
- Only the two approved check names are accepted.
- At least one official check must be completed successfully.
- The exact source workflow must still have a successful default-branch `push` run at the current HEAD.
- No Issue synchronization behavior changed.

- [x] **Step 5: Perform implementation review before publishing**

Use the `requesting-code-review` skill to review the branch against the approved design and this plan. Resolve any correctness or security findings, rerun Steps 1-4, and commit fixes with a narrowly scoped message.

- [x] **Step 6: Publish only after explicit user authorization**

After the user approves the reviewed implementation, use the `github:yeet` skill to push `fix/waef-audit-v43-compatibility` and open a pull request. The pull request description must report:

- five affected repositories and eight removed compatibility false positives;
- the visibility/version workflow matrix;
- the two accepted check names and two accepted path forms;
- the retained source-run provenance requirements;
- the exact test and handbook validation commands and results;
- stale-Issue closure is intentionally deferred to a separate pull request.
