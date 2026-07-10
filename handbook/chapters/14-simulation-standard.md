# Simulation Standard

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Statistical Lead |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how simulation studies are designed, executed, analyzed, and reported.

## 2. Scope

It applies to method evaluation, parameter recovery, power, robustness, algorithm validation, and synthetic-data experiments.

## 3. Philosophy

A simulation is an experiment with a known data-generating process. Its credibility depends on justified scenarios, controlled randomness, adequate Monte Carlo precision, and complete reporting.

## 4. Principles

- Begin with a decision and performance measures.
- Include realistic, boundary, and failure scenarios.
- Separate data generation from estimation.
- Quantify Monte Carlo error.
- Report failed replications and computational constraints.

## 5. Standards

A simulation protocol MUST define:

- research question, target method, comparators, and estimands;
- data-generating process and justification for each varied factor;
- factorial or other scenario design, including boundary conditions;
- performance measures and acceptance criteria;
- replication count justified by Monte Carlo precision;
- random-number generator, master seed, independent streams, and parallel strategy;
- convergence and failure definitions;
- analysis model, uncertainty summaries, and multiplicity considerations where relevant;
- computational environment and reproducible execution plan.

Results MUST report scenario-level replication counts, failures, bias or error, variability, interval performance when applicable, and Monte Carlo standard errors or equivalent precision evidence. Failed runs MUST NOT be silently discarded.

## 6. Best Practices

- Pilot a small design before full execution.
- Test the generator against analytically known moments or distributions.
- Use common random numbers only when justified and documented.
- Save compact sufficient summaries rather than sensitive or excessive intermediate data.
- Visualize performance across conditions, including failure rates.

## 7. Examples

### Example: IRT parameter recovery

The study varies sample size, test length, trait distribution, item quality, and missingness. It compares estimators using bias, root mean square error, interval coverage, convergence, and runtime, with replication counts chosen to control Monte Carlo error.

## 8. Checklist

- [ ] Question, data-generating process, factors, and comparators are justified.
- [ ] Performance measures and acceptance criteria are pre-specified.
- [ ] Replications provide adequate Monte Carlo precision.
- [ ] Random streams and parallel execution are reproducible.
- [ ] Failures, uncertainty, and computational limitations are reported.

## 9. Summary

Simulation evidence must be designed and reported as carefully as an empirical study.

## 10. References

- [Statistical Validation](11-statistical-validation.md)
- [Benchmark Standard](15-benchmark-standard.md)

