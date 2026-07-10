# Pull Request Standard

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

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

A pull request MUST include:

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

Self-approval MUST NOT be the sole approval for high-risk changes. Emergency integration requires explicit owner authorization and retrospective review.

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

## 9. Summary

A pull request is ready only when the change and its evidence can be reviewed as one coherent unit.

## 10. References

- [AI Code Review](19-ai-code-review.md)
- [Release Process](10-release-process.md)

