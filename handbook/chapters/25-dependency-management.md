# Dependency Management

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how third-party software, services, models, datasets, and system packages are selected and maintained.

## 2. Scope

It applies to direct and transitive runtime, development, build, AI-model, data, and service dependencies.

## 3. Philosophy

Every dependency imports capability, risk, maintenance obligations, and legal terms. A small system with understood dependencies is easier to secure and reproduce.

## 4. Principles

- Add a dependency only when its value exceeds its lifecycle cost.
- Use trustworthy sources and identifiable versions.
- Review license, security, privacy, compatibility, and maintenance.
- Update deliberately with tests and rollback.
- Remove unused or unsupported dependencies.

## 5. Standards

Every repository MUST maintain machine-readable dependency manifests and a deterministic resolution mechanism appropriate to its ecosystem. A new material dependency MUST be reviewed for:

- functional need and simpler alternatives;
- source, publisher, integrity, and release provenance;
- license and distribution compatibility;
- known vulnerabilities and security posture;
- maintenance activity, support horizon, and replacement risk;
- data collection, network access, telemetry, and AI retention behavior;
- runtime, platform, and transitive impact.

Dependencies MUST come from approved sources and use version constraints that support reproducibility. Automated vulnerability alerts SHOULD be enabled. Risk-based updates MUST be tested before release, and urgent vulnerabilities MUST have an owner, disposition, and mitigation record. Unused dependencies MUST be removed.

## 6. Best Practices

- Prefer standard libraries and mature, narrowly scoped packages.
- Pin build tools and record system packages or container digests.
- Review dependency diffs separately from application changes.
- Maintain a supported-runtime matrix.
- Use a software bill of materials for distributed or high-risk artifacts.

## 7. Examples

### Example: adding an IRT library

The review confirms parameterization, numerical behavior, license compatibility, supported R versions, dependency tree, and maintenance status. A reference fixture detects changes when the package is upgraded.

## 8. Checklist

- [ ] The dependency has a justified need and approved source.
- [ ] License, security, privacy, maintenance, and compatibility were reviewed.
- [ ] Version resolution and integrity are reproducible.
- [ ] Tests and rollback cover updates.
- [ ] Vulnerable, unsupported, and unused dependencies have an explicit disposition.

## 9. Summary

Dependencies are controlled lifecycle commitments, not free implementation shortcuts.

## 10. References

- [Security Policy](21-security-policy.md)
- [Reproducibility Standard](13-reproducibility-standard.md)

