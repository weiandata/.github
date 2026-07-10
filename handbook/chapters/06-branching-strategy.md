# Branching Strategy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how changes move from isolated work to the protected default branch.

## 2. Scope

It applies to all active WeianData repositories.

## 3. Philosophy

Short-lived branches reduce integration risk and make review clearer. The default branch should remain releasable.

## 4. Principles

- Branch from an up-to-date protected default branch.
- Keep each branch focused on one outcome.
- Integrate frequently and delete merged branches.
- Use release branches only when a maintained release line requires them.

## 5. Standards

WeianData uses a trunk-based default:

- `main` is the preferred default branch name.
- Work MUST occur on a short-lived topic branch unless the repository documents a safer automated path.
- Branch names MUST use a category and concise kebab-case topic: `<category>/<topic>`.
- Approved categories are `feature`, `fix`, `docs`, `refactor`, `test`, `release`, and `hotfix`.
- A topic branch MUST map to one issue or clearly bounded outcome.
- A pull request MUST pass required checks before integration.
- The repository MUST document whether it uses squash, rebase, or merge commits; one method SHOULD be used consistently.

Long-lived environment branches SHOULD NOT be used. Release branches MAY exist for supported maintenance lines and MUST identify their support policy.

## 6. Best Practices

- Open a draft pull request early for risky work.
- Split work that cannot be reviewed as one coherent change.
- Synchronize with `main` before final review.
- Prefer feature flags to long-lived divergence when incomplete behavior must merge safely.

## 7. Examples

```text
feature/irt-fit-diagnostics
fix/missing-score-guard
docs/client-data-boundary
```

## 8. Checklist

- [ ] The branch has one bounded outcome.
- [ ] The name follows the approved category and naming pattern.
- [ ] The branch is based on a current protected default branch.
- [ ] Required checks and review are complete.
- [ ] The branch will be deleted after integration.

## 9. Summary

Use short-lived, focused branches to keep the default branch safe and continuously integrable.

## 10. References

- [Git Standards](05-git-standards.md)
- [Pull Request Standard](30-pull-request-standard.md)

