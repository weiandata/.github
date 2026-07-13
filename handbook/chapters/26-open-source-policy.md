# Open Source Policy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Open Source Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how WeianData consumes, contributes to, and publishes open-source software.

## 2. Scope

It applies to new public repositories, packages, documentation, examples, datasets, external contributions, forks, and upstream patches.

## 3. Philosophy

Open source can improve scientific transparency, trust, reuse, and professional visibility. Publication is irreversible enough to require deliberate intellectual-property, client, security, and maintenance review.

## 4. Principles

- Publish only content WeianData has the right and intent to share.
- Separate reusable methods from client-specific code and data.
- Apply the repository profile selected by the
  [Copyright and Licensing Policy](36-copyright-and-licensing-policy.md).
- Release a maintainable project, not an unexplained code dump.
- Handle vulnerabilities and community participation responsibly.

## 5. Standards

Public release MUST receive accountable approval and confirm:

- ownership and contributor rights;
- no client-confidential, restricted, credential, or proprietary third-party content;
- dependency and license compatibility;
- security review and history scan;
- accurate README, license, contribution, conduct, and security files;
- reproducible build and test evidence;
- public API and statistical-method documentation;
- maintenance owner, support status, and release process.

Client-specific repositories MUST NOT be open-sourced without explicit written authorization and independent review. Public datasets or examples MUST have clear rights, provenance, and disclosure review. External contributions made on behalf of WeianData MUST respect employer, client, and project agreements.

R packages approved for public release MUST use the R-package profile owned by
the Copyright and Licensing Policy. Public release approval does not authorize
a repository-local license substitution.

## 6. Best Practices

- Develop reusable cores with clean client adapters.
- Start with a small, well-documented public surface.
- Use issue and pull request templates to obtain reproducible reports.
- Publish a support policy that matches available capacity.
- Prefer upstream fixes over indefinite private forks.

## 7. Examples

### Example: publishing an R package

The package contains independently owned method code, synthetic examples, tests, documented statistical assumptions, a compatible license, and no client artifacts. The owner commits to a defined maintenance status before publication.

## 8. Checklist

- [ ] Rights, ownership, client obligations, and licenses are cleared.
- [ ] History and content contain no secret or restricted information.
- [ ] Build, tests, methods, interfaces, and examples are reproducible.
- [ ] Community, contribution, security, and support documents are present.
- [ ] An accountable owner approved and will maintain the release status.

## 9. Summary

WeianData publishes open source only when rights, safety, scientific quality, documentation, and maintenance are clear.

## 10. References

- [Community Guidelines](31-community-guidelines.md)
- [Release Process](10-release-process.md)
- [Copyright and Licensing Policy](36-copyright-and-licensing-policy.md)
