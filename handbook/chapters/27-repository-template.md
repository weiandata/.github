# Repository Template

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the required starting scaffold for new repositories.

## 2. Scope

It applies to new internal, client, research, product, and open-source repositories, with visibility-specific files added as needed.

## 3. Philosophy

A template should encode safe defaults while leaving language and project choices explicit.

## 4. Principles

- Start compliant rather than repair compliance later.
- Keep the common core small.
- Separate source, tests, documentation, configuration, and generated artifacts.
- Provide automation for setup and verification.

## 5. Standards

The [repository standards](04-repository-standards.md) own the required capabilities. New repositories SHOULD implement the applicable baseline with this non-normative scaffold:

```text
.
├── README.md
├── LICENSE or PROPRIETARY.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── SECURITY.md
├── .gitignore
├── .editorconfig
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   ├── architecture/
│   └── decisions/
├── src/ or language-native source directory/
├── tests/
├── scripts/
└── dependency manifests and lock files
```

The scaffold MUST be tailored to the selected operating mode and language ecosystem. It MUST NOT be interpreted as requiring an irrelevant directory or tool. Statistical repositories use the validation location required by their owning standards. Directories without a project need SHOULD be omitted rather than left empty.

## 6. Best Practices

- Provide one task runner or command surface for common actions.
- Include synthetic fixtures under `tests/fixtures/`.
- Put ADRs under `docs/decisions/`.
- Keep generated reports under a declared build directory and out of source control unless intentionally released.
- Configure branch protection and required checks immediately.

## 7. Examples

### Example: R package adaptation

An R package uses its native `R/`, `man/`, `tests/testthat/`, and `vignettes/` directories while retaining the governance files, workflows, decision records, validation evidence, and lock file required by this template.

## 8. Checklist

- [ ] Governance, ownership, security, and license files are present.
- [ ] Source, tests, docs, fixtures, and generated output are separated.
- [ ] Setup and verification commands are automated and documented.
- [ ] Dependency and environment state is reproducible.
- [ ] Branch protection and continuous integration are configured.

## 9. Summary

The repository template provides a small, safe, reproducible starting point adapted to each language ecosystem.

## 10. References

- [Repository Standards](04-repository-standards.md)
- [File Structure Convention](33-file-structure-convention.md)
