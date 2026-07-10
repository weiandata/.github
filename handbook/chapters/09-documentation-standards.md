# Documentation Standards

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines documentation required to use, validate, operate, and maintain engineering work.

## 2. Scope

It applies to repositories, APIs, statistical methods, client tools, research artifacts, operations, and releases.

## 3. Philosophy

Documentation is part of the product and part of the evidence. Undocumented behavior is not a reliable organizational capability.

## 4. Principles

- Write for the reader's task.
- Keep documentation close to its source of truth.
- Explain rationale, assumptions, limits, and recovery paths.
- Prefer executable or automatically checked examples.
- Update documentation in the same change as behavior.

## 5. Standards

Material systems MUST document:

- purpose, intended users, and supported use cases;
- setup, configuration, and verified execution commands;
- inputs, outputs, schemas, units, and error behavior;
- architecture and material decisions;
- test, validation, release, and rollback procedures;
- security and data-classification boundaries;
- ownership, support status, and known limitations.

Statistical methods MUST additionally document the estimand, assumptions, preprocessing, model specification, diagnostics, uncertainty, validation evidence, and interpretation limits. Public interfaces MUST have reference documentation. Operational procedures MUST include verification and recovery steps.

## 6. Best Practices

- Use layered documentation: README for orientation, guides for tasks, reference for exact behavior, and decision records for rationale.
- Test code examples in continuous integration when practical.
- Link to evidence rather than copying results into multiple documents.
- Mark deprecated behavior and identify its replacement.

## 7. Examples

### Example: method documentation

An IRT calibration guide defines response coding, model family, identification, estimation settings, fit checks, DIF procedure, uncertainty output, failure conditions, and a reproducible example using synthetic data.

## 8. Checklist

- [ ] Users can understand purpose, setup, and supported behavior.
- [ ] Interfaces, schemas, errors, and limits are documented.
- [ ] Scientific assumptions and evidence are present where applicable.
- [ ] Security, data, ownership, release, and recovery information is clear.
- [ ] Documentation changed with the implementation.

## 9. Summary

Complete documentation makes software and methods usable, reviewable, and maintainable without hidden knowledge.

## 10. References

- [README Standard](28-readme-standard.md)
- [Architecture Decision Records](24-architecture-decision-records.md)

