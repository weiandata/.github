# Repository Standards

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the minimum quality and governance baseline for every WeianData repository.

## 2. Scope

It applies to internal, client-specific, research, product, infrastructure, and open-source repositories.

## 3. Philosophy

A repository is a durable unit of ownership, evidence, and knowledge. It should be understandable without access to its creator's memory.

## 4. Principles

- One clear purpose and accountable owner per repository.
- Safe defaults for branches, secrets, data, and releases.
- Reproducible setup and automated verification.
- Documentation and evidence live close to the code they describe.
- Public and private content are separated deliberately.

## 5. Standards

Every active repository MUST satisfy a baseline proportionate to its [operating mode](../profiles/operating-modes.md) and contain or explicitly link to:

- a README conforming to the [README standard](28-readme-standard.md);
- ownership and maintenance status;
- the profile-selected license or proprietary notice required by the
  [Copyright and Licensing Policy](36-copyright-and-licensing-policy.md);
- contribution and review instructions;
- security reporting guidance appropriate to visibility;
- dependency manifests and lock or snapshot evidence;
- automated tests and a documented test command when executable behavior exists;
- continuous integration for required deterministic checks when the repository is shared, released, or used for Controlled work;
- release and version information when artifacts are distributed;
- data classification and storage rules when data is used.

Git history and branch controls MUST follow the [Git standards](05-git-standards.md). Information stored in a repository MUST follow the [security policy](21-security-policy.md) and [client data policy](22-client-data-policy.md). Generated artifacts SHOULD be excluded unless they are required evidence or distributed deliverables.

## 6. Best Practices

- Start from the approved repository template.
- Keep build, test, lint, and documentation commands discoverable.
- Archive or mark inactive repositories rather than leaving ambiguous ownership.
- Separate reusable library code from client configuration.
- Use repository settings as code when practical.

## 7. Examples

### Example: statistical package repository

The repository includes package metadata, locked dependencies, tests, method documentation, validation fixtures, a changelog, and a release workflow. Restricted data is represented by synthetic fixtures only.

## 8. Checklist

- [ ] Purpose, owner, visibility, and status are explicit.
- [ ] README, license, security, contribution, and release information are present.
- [ ] Required checks run automatically.
- [ ] Dependencies and environment are reproducible.
- [ ] No credential or restricted client data is stored.

## 9. Summary

Every repository must be owned, reproducible, reviewable, and safe to maintain independently of its original author.

## 10. References

- [Repository Template](27-repository-template.md)
- [File Structure Convention](33-file-structure-convention.md)
- [Repository Governance](23-repository-governance.md)
- [Copyright and Licensing Policy](36-copyright-and-licensing-policy.md)
