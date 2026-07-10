# File Structure Convention

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This appendix defines how files are organized so source, configuration, data, evidence, and generated outputs remain distinguishable.

## 2. Scope

It applies to repositories and project delivery directories. Language-native package layouts MAY adapt the generic structure.

## 3. Philosophy

Location communicates lifecycle and authority. A file should have one obvious home based on what it is and how it changes.

## 4. Principles

- Separate source from generated output.
- Separate immutable inputs from transformations and derived data.
- Keep tests and safe fixtures discoverable.
- Keep durable decisions with documentation.
- Never rely on a local untracked file for a required production behavior.

## 5. Standards

Use the [repository template](27-repository-template.md) as the baseline. Within analytical projects, use the applicable form of:

```text
project/
├── config/             # non-secret versioned configuration
├── data/
│   ├── README.md       # classification, provenance, and access rules
│   ├── raw/            # immutable inputs; usually excluded from Git
│   ├── interim/        # reproducible transformations
│   └── derived/        # reproducible analysis-ready data
├── docs/
│   ├── architecture/
│   └── decisions/
├── reports/            # source documents, not manual final edits
├── src/                # reusable implementation
├── tests/
│   └── fixtures/       # synthetic or public safe data
└── build/              # generated artifacts; usually excluded from Git
```

Raw inputs MUST be immutable. Derived files MUST be reproducible from controlled inputs and code. Restricted client data MUST NOT be placed in a WeianData repository. Secrets MUST NOT be stored in configuration files. Generated output MUST NOT be manually edited as the source of truth.

Each non-obvious directory SHOULD contain a short README describing ownership, lifecycle, generation, and data classification.

## 6. Best Practices

- Use a single build directory that can be safely recreated.
- Keep small synthetic fixtures close to tests.
- Place one-off migration scripts in a clearly dated or versioned migration directory.
- Avoid deeply nested structures that add no ownership boundary.
- Make cleanup and archival procedures explicit.

## 7. Examples

### Example: client-side execution package

The package contains source, configuration schema, synthetic fixture, tests, and build manifest. The client supplies raw data to a documented mount or directory that is excluded from the package and logs.

## 8. Checklist

- [ ] Every file has one obvious lifecycle-based location.
- [ ] Source, configuration, tests, inputs, derived data, reports, and builds are separated.
- [ ] Raw inputs are immutable and derived outputs reproducible.
- [ ] Secrets and restricted client data are absent from repositories.
- [ ] Non-obvious directories document ownership and lifecycle.

## 9. Summary

The file structure makes authority, reproducibility, data boundaries, and generated state visible.

## 10. References

- [Repository Template](27-repository-template.md)
- [Client Data Policy](22-client-data-policy.md)

