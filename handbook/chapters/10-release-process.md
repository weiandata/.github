# Release Process

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Release Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how a reviewed change becomes an identifiable, distributable release.

## 2. Scope

It applies to software packages, applications, client tools, models, data products, documentation, and the handbook.

## 3. Philosophy

A release is an evidence-backed promise about a specific artifact, not merely a tag or uploaded file.

## 4. Principles

- Release from an immutable reviewed source revision.
- Match evidence to the risk and intended use.
- Make versions, contents, limitations, and recovery explicit.
- Separate internal approval from public publication.
- Preserve enough provenance to reproduce the artifact.

## 5. Standards

Every release MUST:

1. identify an accountable release owner;
2. use the [versioning guide](34-versioning-guide.md);
3. originate from a protected, reviewed source revision;
4. pass required build, test, security, documentation, and license checks;
5. pass [statistical validation](11-statistical-validation.md) when outputs carry scientific meaning;
6. include release notes covering changes, compatibility, migration, limitations, and known issues;
7. produce checksummed or otherwise identifiable artifacts;
8. record environment and dependency provenance;
9. define rollback, withdrawal, or correction procedures;
10. receive accountable human approval.

Client releases MUST also follow the client-data policy and record acceptance criteria. Public releases MUST pass the open-source policy.

## 6. Best Practices

- Build artifacts in controlled automation.
- Test the artifact that will be distributed, not only source code.
- Use release candidates for high-risk or externally integrated changes.
- Keep release notes user-oriented and link detailed evidence.
- Conduct a post-release check for installation, observability, and critical behavior.

## 7. Examples

### Example: R package release

The release is built from a reviewed tag, passes package checks on supported R versions, reproduces validation fixtures, records dependency state, includes method changes and migration notes, and receives human approval before distribution.

## 8. Checklist

- [ ] Version, owner, source revision, and artifact identity are recorded.
- [ ] Required engineering, statistical, security, and license gates pass.
- [ ] Release notes and compatibility information are complete.
- [ ] Environment and dependencies are reproducible.
- [ ] Rollback or correction is possible and approval is recorded.

## 9. Summary

A WeianData release is a reviewed, validated, reproducible artifact with clear ownership and recovery.

## 10. References

- [Open Source Policy](26-open-source-policy.md)
- [Dependency Management](25-dependency-management.md)

