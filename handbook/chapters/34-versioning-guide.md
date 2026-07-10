# Versioning Guide

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This appendix defines how WeianData identifies compatible and incompatible changes.

## 2. Scope

It applies to software, APIs, packages, schemas, models, client tools, documents, and handbook releases.

## 3. Philosophy

A version communicates a compatibility contract. It must identify a stable artifact and a meaningful change boundary.

## 4. Principles

- Version public behavior, not internal activity.
- Define the compatibility surface before assigning a version.
- Make breaking changes explicit and provide migration.
- Keep artifact identity immutable after release.
- Version schemas, models, and software independently when their lifecycles differ.

## 5. Standards

Stable released artifacts MUST use Semantic Versioning in the form `MAJOR.MINOR.PATCH`:

- **MAJOR**: incompatible public behavior, schema, statistical interpretation, or handbook structure;
- **MINOR**: backward-compatible capability or standard;
- **PATCH**: backward-compatible correction with no intended new capability.

Pre-release identifiers MAY be used, for example `2.0.0-rc.1`. Release tags MUST use a leading `v`, such as `v1.4.2`, and MUST identify an immutable source revision.

A release MUST define its compatibility surface. Statistical compatibility includes parameterization, scale, scoring rules, defaults, and interpretation, not only function signatures. A model artifact MUST record the compatible code and schema versions. A data schema change MUST state migration and backward-read behavior.

Version numbers MUST NOT be reused. A released artifact MUST be corrected with a new version, not replaced in place.

## 6. Best Practices

- Start with `0.y.z` while the public contract is intentionally unstable.
- Deprecate before removing when risk and maintenance allow it.
- Test supported old inputs and clients against new releases.
- Include machine-readable schema and model versions in artifacts.
- Tie the changelog to user-visible and scientific consequences.

## 7. Examples

| Change | Version effect |
|---|---|
| Correct documentation typo | Patch |
| Add optional diagnostic output | Minor |
| Change default scoring scale | Major |
| Add backward-compatible handbook chapter | Minor |
| Renumber handbook architecture | Major |

## 8. Checklist

- [ ] The compatibility surface is defined.
- [ ] Version impact matches user and scientific consequences.
- [ ] Migration, deprecation, and supported versions are documented.
- [ ] Model, schema, code, and handbook versions are related explicitly.
- [ ] The tag and artifact are immutable and uniquely identifiable.

## 9. Summary

Versions communicate compatibility across software behavior, statistical meaning, data schemas, models, and handbook rules.

## 10. References

- [Release Process](10-release-process.md)
- [Commit Convention](07-commit-convention.md)

