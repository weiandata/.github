# WAEF 4.0 candidate bridge sandbox validation

## Verdict

PASS for the pre-release candidate bridge only. The exact WAEF candidate ran
successfully in a private consumer, all approved negative scenarios produced
attributable evidence, audit fingerprints were stable, and the reviewed upgrade
automation created an unmerged Draft Pull Request. This report does not prove
final `v4.0` tag provenance or authorize a merge, release, production audit,
ruleset activation, migration, or sandbox deletion.

## Identities and boundary

| Item | Evidence |
|---|---|
| Sandbox | [`weiandata/waef-compliance-sandbox`](https://github.com/weiandata/waef-compliance-sandbox), private, non-template |
| WAEF candidate | `da22b444005e834e12d114651f354277e0e3a10d` |
| Candidate review | [WAEF Draft PR #2](https://github.com/weiandata/WAEF/pull/2), open, unmerged, exact head unchanged |
| Final sandbox baseline | `54a9b8de2e9bb8bdbd4d4144fff32409e0f37770` |
| Frozen organization harness | `042f089ae64c0bac342ecff44be7f50851721526` in [.github Draft PR #1](https://github.com/weiandata/.github/pull/1) |
| WAEF workflow sharing | `access_level: organization`; changed from `none` after explicit approval |
| Production inventory/schedule | Unchanged; sandbox is not in `operations/waef/repositories.json` and no production audit was dispatched |

The planned `sandbox/...` test branch prefix was changed to
`test/sandbox-*` because the frozen candidate accepts only categorized WAEF
branch prefixes. This avoided an unrelated `WAEF-GIT-BRANCH` failure in every
scenario while preserving the scenario names and isolation.

## Clean baseline

The first caller attempt failed before job creation because private WAEF
reusable-workflow access was `none` ([run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380247860)).
After the explicitly approved change to organization access, the exact candidate
completed every guarded step at `25bc0ec91924270aae1c33b869833e166fa27ccb`:

- [WAEF Compliance](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380395714): success;
- [Project CI](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380395469): success.

After recording the reviewed source and pinning the repaired audit harness, the
final clean `main` head remained green:

- [WAEF Compliance](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381150216): success;
- [Project CI](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381150036): success.

The successful WAEF job restricted the caller to the exact sandbox, created a
read token, checked out the exact private candidate, verified candidate identity,
installed pinned requirements, and validated the repository.

## Isolated negative Pull Requests

All Pull Requests below are open and unmerged. Each file mutation is isolated
from clean `main`.

| Scenario | PR / head | Hosted evidence | Conclusion |
|---|---|---|---|
| Wrong locked WAEF SHA | [#1](https://github.com/weiandata/waef-compliance-sandbox/pull/1) / `a8dc5c019172c034bac1cfd3d49869818aadecd7` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380607635) | `WAEF-CANDIDATE-HEAD`; Project CI succeeded |
| Missing plan evidence | [#2](https://github.com/weiandata/waef-compliance-sandbox/pull/2) / `4404a2697e10895266f8a637dd9a23592b0bdb0e` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380639297) | `WAEF-EVIDENCE-PLAN`; Project CI succeeded |
| Expired exception | [#3](https://github.com/weiandata/waef-compliance-sandbox/pull/3) / `6b0e684e48410ad9f71f2d903d97f48d2b598989` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380677475) | `WAEF-EXCEPTION-EXPIRED`; Project CI succeeded |
| Deleted caller | [#4](https://github.com/weiandata/waef-compliance-sandbox/pull/4) / `9b3e2459fbd5ecded2075f64b046a6eead5c50f5` | [Project CI](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380726998), audit below | No WAEF run exists; independent audit reports missing caller and missing source-bound check |
| Renamed caller | [#5](https://github.com/weiandata/waef-compliance-sandbox/pull/5) / `a7d22a8d6b41ae728affa87ffb994d559edbabd1` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380773519) | `WAEF-BOOTSTRAP-WORKFLOW`; Project CI succeeded |
| Removed push trigger | [#6](https://github.com/weiandata/waef-compliance-sandbox/pull/6) / `7eaf871acd70280466d6ec2e0913c10c966e5410` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380812930) | `WAEF-WORKFLOW-THIN-CALLER`; Project CI succeeded |
| Caller `if: false` | [#7](https://github.com/weiandata/waef-compliance-sandbox/pull/7) / `d61796ef67214acf0fb80660aa66e7b7c8c2ee01` | [WAEF run](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380861733) | Compliance job was `SKIPPED`; Project CI succeeded; exact-caller audit rejects the mutation |
| Red project check with WAEF name spoof | [#8](https://github.com/weiandata/waef-compliance-sandbox/pull/8) / `65e673863b8368172c1e6ed824ace9bd892de2f0` | [real WAEF success](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380900754), [spoofed Project CI failure](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380900529) | A same-name failing project check remained visibly red and did not replace source-bound WAEF evidence |

Because production ruleset activation is intentionally still pending, GitHub
reported the deleted and skipped-caller PRs as `CLEAN`; they nevertheless remain
open and unmerged and fail the independent audit contract. This is evidence for,
not a substitute for, the later reviewed ruleset activation.

## Audit implementation and fingerprint behavior

The first live audit exposed GitHub Contents API line-wrapped Base64 handling:
[run 29380963615](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29380963615)
failed before findings were synchronized. Regression tests reproduced the exact
boundary for both audit and upgrade reads. Commit
`042f089ae64c0bac342ecff44be7f50851721526` normalizes whitespace before strict
Base64/UTF-8 validation; the focused tests and the complete 56-test organization
suite passed.

Two independent audits of `test/sandbox-deleted-caller` then completed their
finding and synchronization paths:

- [first corrected audit](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381179025);
- [repeat audit](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381230484).

The CLI intentionally exited 1 because findings existed. The first run created
one Issue per fingerprint; the second run updated the same two Issue numbers and
created no duplicate:

| Finding | Fingerprint | Issue | Created | Updated by repeat |
|---|---|---|---|---|
| Missing source-bound WAEF check | `df909ba4dcd160d25a0d` | [#9](https://github.com/weiandata/waef-compliance-sandbox/issues/9) | `2026-07-15T01:15:29Z` | `2026-07-15T01:16:50Z` |
| Missing exact candidate caller | `3d2de0a10a5388b0ce3e` | [#10](https://github.com/weiandata/waef-compliance-sandbox/issues/10) | `2026-07-15T01:15:30Z` | `2026-07-15T01:16:50Z` |

The original plan expected one finding, but the live ref correctly produced two
orthogonal controls. Suppressing either would weaken the independent audit.

## Draft-only upgrade

[Upgrade run 29381262497](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381262497)
successfully created [Draft PR #11](https://github.com/weiandata/waef-compliance-sandbox/pull/11)
for synthetic `4.1`/`v4.1` at the candidate SHA.

- state: open and Draft;
- auto-merge: absent;
- base: unchanged `54a9b8de2e9bb8bdbd4d4144fff32409e0f37770`;
- head: `61baf760be99cb0a4fec639719c41595fafe297d`;
- changes: only the lock, caller, and generated WAEF-owned adapters;
- Project CI: success;
- [WAEF Compliance](https://github.com/weiandata/waef-compliance-sandbox/actions/runs/29381275054): failed with `WAEF-SOURCE-TAG-COMMIT` and `WAEF-SOURCE-METADATA`.

The result proves automation can open a review-only Draft without writing
`main`, while unreleased version and provenance evidence remains blocking.

## Credential evidence and revocation

During the validation window the Read App remained read-only on all installed
repositories. The Automation App installation used `Only select repositories`,
temporarily selected 12 repositories (the reviewed 11 plus only the sandbox),
and the workflows requested only the exact repositories needed per token.

Only these encrypted sandbox Secrets were present; values were never read or
printed:

| Secret | Updated |
|---|---|
| `WAEF_AUTOMATION_APP_PRIVATE_KEY` | `2026-07-15T00:52:29Z` |
| `WAEF_APP_PRIVATE_KEY` | `2026-07-15T00:52:38Z` |
| `WAEF_AUTOMATION_APP_ID` | `2026-07-15T00:52:48Z` |
| `WAEF_APP_ID` | `2026-07-15T00:52:56Z` |

Runs `29381150216`, `29381230484`, `29381262497`, `29380607635`, and
`29380900529` were scanned without downloading artifacts. Results: zero PEM
headers, zero GitHub token prefixes, and zero unmasked Authorization headers;
expected secret bindings appeared only as `***`.

Revocation status: complete.

- `gh secret list --repo weiandata/waef-compliance-sandbox` returned no names
  after all four Secrets were deleted.
- Temporary Read App key fingerprint
  `SHA256:IsWkI8FivsBA/su1BFrFyte9XHsIpbHFTZhqpD4zhEc=` was revoked; one original
  key remains.
- Temporary Automation App key fingerprint
  `SHA256:B7SLLmwu9/7CrOsTU/vM9gOXzznmLuzNBziNeFZBlJI=` was revoked; one original
  key remains.
- Automation App installation was restored to `Only select repositories`, 11
  selected, with `waef-compliance-sandbox` absent.
- Read App installation remained `All repositories`; Actions, Checks, Contents,
  and mandatory Metadata permissions were verified `Read-only`, with no write
  permission selected.
- The sandbox repository, open test PRs, and audit Issues were retained for
  review and were not deleted.

## Remaining release gates

- Remote `refs/tags/v4.0` returned HTTP 404 on 2026-07-15; final tag provenance
  is unverified by design.
- WAEF Draft PR #2 and every sandbox PR remain unmerged.
- WAEF Maintainer approval, production `compliance.yml` proof against the final
  tag, repository-template adoption, and template-derived sandbox evidence are
  still required.
- Production audit dispatch, production ruleset activation, repository
  migrations, publication, and sandbox deletion remain pending.
- GitHub emitted a non-blocking Node.js 20 deprecation warning for the pinned
  `actions/create-github-app-token` commit while forcing Node.js 24. Updating an
  immutable action pin requires a separately reviewed candidate or release.
