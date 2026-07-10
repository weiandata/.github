# Git Standards

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines safe, auditable use of Git.

## 2. Scope

It applies to every Git repository managed by or for WeianData.

## 3. Philosophy

Version history is engineering evidence. It should explain how and why the system changed without exposing secrets or confidential data.

## 4. Principles

- Preserve reviewable history.
- Prefer small, atomic changes.
- Protect shared branches.
- Never use version control as secret or restricted-data storage.
- Make recovery possible before rewriting history.

## 5. Standards

- Changes to a protected branch MUST arrive through an approved pull request unless an emergency procedure is invoked.
- Commits MUST follow the [commit convention](07-commit-convention.md).
- Branches MUST follow the [branching strategy](06-branching-strategy.md).
- Secrets, credentials, private keys, raw client data, and directly identifying data MUST NOT be committed, including in deleted history.
- Force pushes to protected branches MUST be disabled. A history rewrite on any shared branch requires owner approval and coordination.
- Commits SHOULD be atomic: one coherent reason to change, with tests and documentation included when relevant.
- Generated or binary files MUST be intentionally tracked and justified.

If sensitive content enters Git history, the incident MUST be treated as exposure: revoke or rotate the secret, contain access, remove the content safely, and record the incident.

## 6. Best Practices

- Review staged changes before every commit.
- Rebase or merge according to repository policy before requesting final review.
- Use tags only for immutable release points.
- Keep local experiments out of shared history until they are understandable.
- Use `.gitignore` and pre-commit secret checks as preventive controls.

## 7. Examples

### Example: atomic history

One commit introduces a parser and unit tests. A second commit updates documentation. The pull request explains their shared purpose. Neither commit contains unrelated formatting across the repository.

## 8. Checklist

- [ ] Staged changes contain no secret or restricted data.
- [ ] The branch and commits follow their owning standards.
- [ ] Each commit is coherent and reviewable.
- [ ] Shared history was not rewritten without approval.
- [ ] Release tags, if any, identify immutable reviewed states.

## 9. Summary

Git history must be safe, explainable, and useful as long-term engineering evidence.

## 10. References

- [Security Policy](21-security-policy.md)
- [Client Data Policy](22-client-data-policy.md)

