# Commit Convention

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines a consistent, machine-readable commit message format.

## 2. Scope

It applies to commits intended for shared WeianData history.

## 3. Philosophy

A commit message should make the reason for a change understandable without reading the entire diff.

## 4. Principles

- Describe intent, not file activity.
- Keep the subject concise and specific.
- Explain rationale and consequences when they are not obvious.
- Identify breaking changes explicitly.

## 5. Standards

Commit messages MUST follow this form:

```text
<type>(<optional-scope>): <imperative summary>

<optional body explaining why and important consequences>

<optional trailers>
```

Allowed types are:

| Type | Use |
|---|---|
| `feat` | New user-visible capability |
| `fix` | Defect correction |
| `docs` | Documentation-only change |
| `refactor` | Internal change without intended behavior change |
| `test` | Test-only change |
| `perf` | Measured performance improvement |
| `build` | Build or packaging change |
| `ci` | Continuous-integration change |
| `chore` | Necessary maintenance not covered above |
| `revert` | Reversal of a prior commit |

The subject MUST use imperative mood, start lowercase after the colon, omit a final period, and remain concise. Breaking changes MUST include `BREAKING CHANGE:` in the footer.

## 6. Best Practices

- Use a scope that names a stable component, not a filename.
- State why the change is needed in the body.
- Reference an issue or decision record in a trailer when relevant.
- Avoid mixing formatting, refactoring, and behavior changes.

## 7. Examples

```text
fix(scoring): reject non-finite response weights

Prevent invalid weights from propagating into ability estimates.

Refs: #142
```

## 8. Checklist

- [ ] The type matches the change.
- [ ] The summary states intent in imperative form.
- [ ] Scope is stable and useful, if present.
- [ ] Rationale and consequences are recorded when needed.
- [ ] Breaking changes and issue references are explicit.

## 9. Summary

Consistent commit messages make history readable, searchable, and suitable for automation.

## 10. References

- [Git Standards](05-git-standards.md)
- [Versioning Guide](34-versioning-guide.md)

