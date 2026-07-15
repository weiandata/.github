# Pull Request Standard

| Field | Value |
|---|---|
| Version | 1.2.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-15 |

## 1. Purpose

This chapter defines the evidence required to review and integrate a change.

## 2. Scope

It applies to changes entering a protected branch.

## 3. Philosophy

A pull request is a review package: problem, change, evidence, risk, and recovery presented together.

## 4. Principles

- Keep changes focused and understandable.
- Show primary evidence, not only conclusions.
- Make risk and compatibility explicit.
- Resolve review findings before integration.
- Do not use approval to bypass required automated or domain checks.

## 5. Standards

Standard and Controlled pull requests MUST include:

```markdown
## Outcome

## Context and linked issue

## Changes

## Non-changes

## Verification evidence

## Statistical validation

## Security and client-data review

## Compatibility, migration, and rollback

## Documentation and release impact

## AI contribution

## Reviewer checklist
```

The author MUST disclose material AI assistance and identify how the output was verified. Required checks MUST pass. Statistical, security, dependency, license, data, and domain reviewers MUST be requested when their areas are affected. The author MUST respond to findings with a change, evidence-based rationale, or documented follow-up approved by the reviewer.

Pull requests entering a governed default branch MUST pass strict, source-bound `compliance / WAEF Compliance` and `Project CI` checks for the final reviewed head. Required human approval, code-owner review, and resolved conversations remain independent gates; a green automated check does not replace them.

Lightweight pull requests MAY contain only outcome, risk class, verification evidence, and owner self-review. Before a Controlled result is relied on by a client or the public, self-approval MUST NOT be the sole human approval. A qualified client reviewer or contracted specialist MAY provide the second review when the scope and evidence are recorded. Emergency integration requires explicit owner authorization and retrospective review, but it MUST NOT create external reliance on an unreviewed high-risk result.

## 6. Best Practices

- Keep diffs small enough for complete review.
- Use draft status until the evidence package is ready.
- Add comments that explain surprising intent, not obvious syntax.
- Review generated files through their source and reproducible build.
- Re-run checks after material review changes.

## 7. Examples

### Example: statistical change

The pull request links the issue and ADR, compares estimates with the reference implementation, attaches simulation and sensitivity summaries, documents parameterization, discloses AI-generated scaffolding, and identifies the statistical approver.

## 8. Checklist

- [ ] Outcome, context, scope, and linked issue are clear.
- [ ] Tests and primary verification evidence pass.
- [ ] Statistical, security, data, dependency, and license impact are reviewed.
- [ ] Compatibility, documentation, release, and rollback are addressed.
- [ ] AI contribution and human verification are disclosed.
- [ ] Required reviewers approved the final material state.
- [ ] Source-bound WAEF and project checks pass for the final reviewed head.

## 9. Summary

A pull request is ready only when the change and its evidence can be reviewed as one coherent unit.

## 10. References

- [AI Code Review](19-ai-code-review.md)
- [Release Process](10-release-process.md)
- [WAEF Governance Framework](https://github.com/weiandata/WAEF)
- [Staged WAEF Organization Ruleset](https://github.com/weiandata/.github/blob/main/operations/waef/RULESET.md)
