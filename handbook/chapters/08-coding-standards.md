# Coding Standards

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines language-independent requirements for production and research code.

## 2. Scope

It applies to Python, R, TypeScript, SQL, shell code, configuration, and future implementation languages.

## 3. Philosophy

Code should make correct behavior easy to inspect and incorrect behavior difficult to express or ignore.

## 4. Principles

- Prefer clarity over cleverness.
- Make interfaces, invariants, and failure modes explicit.
- Separate domain logic from input/output and infrastructure.
- Test behavior at the lowest useful level and at critical boundaries.
- Design statistical code for determinism, diagnostics, and traceability.

## 5. Standards

Every repository MUST declare its formatter, linter, test runner, supported runtime versions, and type or static-analysis policy. Code MUST:

- use descriptive names defined by the [naming convention](32-naming-convention.md);
- validate external inputs at system boundaries;
- fail with actionable errors and preserve the underlying cause;
- avoid hidden global state and undocumented side effects;
- keep secrets and environment-specific values outside source code;
- include tests for normal, boundary, invalid, and regression behavior;
- document public interfaces and scientifically meaningful calculations;
- make randomness controllable and record seeds where reproducibility requires it;
- avoid silent coercion, silent data loss, and silent fallback in scientific paths.

Language-specific rules MAY be stricter and MUST be documented in the repository.

## 6. Best Practices

- Keep functions focused on one level of abstraction.
- Prefer pure transformations for statistical logic.
- Use types or validated schemas at component boundaries.
- Make units, scales, missing values, and categorical encodings explicit.
- Optimize only after measurement and preserve a clear reference implementation for sensitive algorithms.

## 7. Examples

### Example: explicit scoring boundary

A scoring function accepts a validated response matrix and immutable model parameters. It rejects unknown item identifiers, reports non-finite inputs, accepts a controlled random seed when sampling is used, and returns diagnostics with estimates.

## 8. Checklist

- [ ] Tooling and supported runtimes are declared.
- [ ] Inputs, outputs, invariants, and errors are explicit.
- [ ] Tests cover boundaries and prior defects.
- [ ] Randomness, missingness, units, and encodings are controlled.
- [ ] Scientific calculations and public interfaces are documented.

## 9. Summary

WeianData code must be clear, testable, explicit about data behavior, and suitable for scientific review.

## 10. References

- [Statistical Validation](11-statistical-validation.md)
- [Reproducibility Standard](13-reproducibility-standard.md)

