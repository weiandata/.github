# README Standard

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the orientation information every repository README must provide.

## 2. Scope

It applies to the top-level `README.md` of every active repository.

## 3. Philosophy

A reader should be able to decide what the repository is, whether it applies to them, and how to verify it within minutes.

## 4. Principles

- Lead with purpose and supported use.
- Make the shortest verified path executable.
- State status, ownership, and limitations honestly.
- Link detail rather than overloading the README.

## 5. Standards

A README MUST include, in a sensible order:

1. project name and one-sentence purpose;
2. status, intended users, and supported use cases;
3. key capabilities and explicit non-goals;
4. prerequisites and a minimal verified setup;
5. minimal usage example using safe data;
6. test or validation command;
7. architecture or documentation links;
8. data, security, and privacy boundaries;
9. contribution and support paths;
10. license or proprietary notice, owner, and citation where applicable.

Badges MUST reflect automated facts and MUST NOT substitute for explanation. Claims about performance or statistical validity MUST link to reproducible evidence.

## 6. Best Practices

- Keep the quick start copyable and tested.
- Put detailed API, methods, and operations content in dedicated documentation.
- Include example output only when it helps verify success.
- State maintenance status prominently for experimental or archived work.
- Update the README in the same change as setup or interface changes.

## 7. Examples

```markdown
# Survey Scoring Toolkit

Reproducible client-side scoring for validated survey instruments.

Status: Active, internal. Raw client data must remain in the client environment.

## Quick start

Run `make test` with the included synthetic fixture.
```

## 8. Checklist

- [ ] Purpose, audience, status, owner, and limitations are clear.
- [ ] Setup, safe example, and verification command work.
- [ ] Documentation and architecture links resolve.
- [ ] Data and security boundaries are explicit.
- [ ] Claims, support, contribution, and license information are accurate.

## 9. Summary

The README is the reliable front door to a repository, not its complete documentation system.

## 10. References

- [Documentation Standards](09-documentation-standards.md)
- [Open Source Policy](26-open-source-policy.md)

