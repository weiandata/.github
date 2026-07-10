# AI Code Review

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines review controls for code created or materially modified by AI.

## 2. Scope

It applies whether AI generated an entire change, a fragment, tests, migration code, statistical logic, or a review recommendation.

## 3. Philosophy

AI-generated code is untrusted third-party input. Plausibility and fluency increase the need for evidence; they do not reduce it.

## 4. Principles

- Review the diff and behavior, not the model's explanation.
- Verify dependencies, licenses, APIs, and security assumptions.
- Test failure paths and boundaries that generated code commonly overlooks.
- Require statistical review for scientifically meaningful logic.
- Preserve enough provenance to investigate defects.

## 5. Standards

The reviewer MUST:

1. understand the intended behavior and acceptance criteria;
2. inspect every material diff and generated dependency;
3. verify APIs and facts against authoritative sources;
4. run formatter, linter, type, unit, integration, and security checks applicable to the repository;
5. test invalid input, error handling, resource limits, concurrency, and data leakage where relevant;
6. check for fabricated functions, insecure defaults, silent fallback, weak validation, and unnecessary complexity;
7. apply the statistical validation standard to statistical logic;
8. confirm documentation and provenance;
9. obtain a qualified human approval for high-risk changes.

AI-generated tests MUST NOT be the only evidence for AI-generated implementation. A human or independently specified oracle MUST establish expected behavior.

## 6. Best Practices

- Ask the AI to identify uncertain code paths, then verify them independently.
- Compare sensitive algorithms with a clear reference implementation.
- Use mutation, property-based, or adversarial tests for critical logic.
- Inspect transitive dependency and license impact.
- Reduce large generated changes before review.

## 7. Examples

### Example: generated estimation routine

The reviewer checks the parameterization against primary documentation, compares results with a trusted implementation, tests non-convergence and extreme inputs, examines numerical stability, and rejects an undocumented fallback that changed the estimator.

## 8. Checklist

- [ ] Intended behavior is independently understood.
- [ ] Every material diff, API, dependency, and license was verified.
- [ ] Required tests include boundaries and failure paths.
- [ ] Security, privacy, and statistical review are complete.
- [ ] Provenance, documentation, and human approval are recorded.

## 9. Summary

AI-authored code is accepted only through direct inspection, independent evidence, and risk-appropriate human review.

## 10. References

- [Coding Standards](08-coding-standards.md)
- [AI Development Policy](16-ai-development-policy.md)

