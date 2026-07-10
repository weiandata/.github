# Statistical Validation

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Statistical Lead |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the evidence required to trust statistically meaningful software and results.

## 2. Scope

It applies to descriptive analyses, models, scoring, Item Response Theory (IRT), Classical Test Theory (CTT), equating, Differential Item Functioning (DIF), simulation, automated reports, and statistical software.

## 3. Philosophy

Software verification asks whether the implementation behaves as specified. Statistical validation asks whether the specification and output are suitable for the intended inference or decision. Both are required.

## 4. Principles

- Define the intended use and estimand before examining preferred results.
- Treat data quality and measurement assumptions as part of validation.
- Use evidence from more than one perspective: theory, tests, diagnostics, simulation, reference comparison, and sensitivity.
- Report uncertainty and failure, not only point estimates and success.
- Require human scientific judgment for acceptance.

## 5. Standards

Every material statistical output MUST have a validation plan proportional to its risk. The plan MUST identify:

1. intended use, population, decision, and estimand;
2. data provenance, sampling, exclusions, coding, missingness, and quality checks;
3. model, identification, estimation, convergence, and numerical tolerances;
4. assumptions and diagnostics;
5. reference results, analytic cases, independent implementation, or simulation evidence;
6. sensitivity to plausible preprocessing, model, and tuning choices;
7. uncertainty, limitations, failure conditions, and interpretation boundaries;
8. reproducible evidence artifacts and accountable approval.

For IRT or measurement models, validation MUST consider the applicable items among dimensionality, local dependence, item and person fit, parameter recovery, scale identification, score precision, invariance or DIF, equating or linking stability, extreme response patterns, and consequences of missing or not-reached responses. Thresholds MUST be justified for the intended use; the handbook does not define universal cutoffs.

An AI-generated interpretation, successful convergence flag, high predictive metric, or passing unit test MUST NOT be treated as sufficient validation by itself.

## 6. Best Practices

- Pre-specify acceptance criteria before final analysis.
- Maintain a simple reference implementation for sensitive algorithms.
- Compare against trusted software using documented parameterization and tolerances.
- Include adversarial, boundary, and degenerate datasets.
- Separate exploratory findings from confirmatory claims.
- Review practical consequences, not only statistical significance.

## 7. Examples

### Example: IRT scoring engine

Validation includes analytic edge cases, parameter recovery under realistic sample sizes, comparison with a trusted implementation, convergence diagnostics, sensitivity to starting values, scoring precision across the trait range, missing-response behavior, and documented limitations. The statistical lead approves the intended use.

## 8. Checklist

- [ ] Intended use, population, estimand, and acceptance criteria are explicit.
- [ ] Data provenance, coding, missingness, and quality are validated.
- [ ] Model assumptions, identification, convergence, fit, and uncertainty are reviewed.
- [ ] Reference, simulation, and sensitivity evidence are sufficient for the risk.
- [ ] Limitations and failure conditions are reported.
- [ ] Evidence is reproducible and a human statistical owner approved use.

## 9. Summary

Statistical work is acceptable only when its implementation, assumptions, evidence, uncertainty, and intended interpretation have been reviewed together.

## 10. References

- [Research Workflow](12-research-workflow.md)
- [Simulation Standard](14-simulation-standard.md)
- [Reproducibility Standard](13-reproducibility-standard.md)

