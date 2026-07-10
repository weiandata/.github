# Reproducibility Standard

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the evidence required for an independent operator to reproduce an engineering or statistical result.

## 2. Scope

It applies to analyses, models, simulations, reports, software builds, benchmarks, and client tools.

## 3. Philosophy

Reproducibility is a property of the entire execution chain, not only the availability of code.

## 4. Principles

- Identify every material input and transformation.
- Control environments, dependencies, randomness, and configuration.
- Separate immutable inputs from generated outputs.
- Prefer one-command or automated execution.
- Preserve evidence without violating client-data restrictions.

## 5. Standards

Every material result MUST include a reproducibility manifest containing:

- source revision and uncommitted-change status;
- execution command or workflow entry point;
- runtime, operating-system, and dependency versions;
- configuration and feature flags without secrets;
- input identities, schemas, classifications, and checksums where permitted;
- random-number generator, seed, and parallel-stream strategy when applicable;
- transformation lineage and generated artifact identities;
- test and validation results;
- execution date, operator or automation identity, and known nondeterminism.

Dependencies MUST be locked, snapshotted, or otherwise resolved deterministically. Restricted inputs MUST remain in the approved environment; reproducibility MAY be demonstrated with synthetic fixtures plus client-side evidence. Manual steps MUST be documented and minimized.

## 6. Best Practices

- Provide a clean-environment reproduction command.
- Cache external inputs only when licensing and security allow it.
- Make pipelines idempotent and fail on unexpected schema changes.
- Record session information automatically in R and Python workflows.
- Compare output hashes or tolerance-based summaries in regression tests.

## 7. Examples

```text
Source revision: 4f62...
Command: make validation-report
Environment: container image digest sha256:...
Inputs: restricted/client-side; schema fixture v3
Random seed: 20260710; independent streams per scenario
Outputs: report.pdf and validation.json with checksums
```

## 8. Checklist

- [ ] Source, command, environment, dependencies, and configuration are identified.
- [ ] Inputs and transformations have permitted provenance and integrity evidence.
- [ ] Randomness and parallel execution are controlled.
- [ ] Outputs and validation evidence are identifiable.
- [ ] A clean or client-controlled reproduction has been demonstrated.

## 9. Summary

A result is reproducible when its complete execution context and evidence can be reconstructed without hidden knowledge or unauthorized data movement.

## 10. References

- [Dependency Management](25-dependency-management.md)
- [Client Data Policy](22-client-data-policy.md)

