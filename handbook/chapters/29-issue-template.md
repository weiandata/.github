# Issue Template

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | Repository Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the minimum information needed to begin trackable engineering work.

## 2. Scope

It applies to feature, defect, research, documentation, maintenance, and security work items. Sensitive vulnerability reports use the private security channel, not a public issue.

## 3. Philosophy

An issue should define an observable problem and completion condition without prescribing an unreviewed solution.

## 4. Principles

- Describe the outcome and evidence.
- Separate observed facts from hypotheses.
- Classify risk and data before attaching artifacts.
- Make scope and non-scope explicit.
- Identify ownership and dependencies.

## 5. Standards

Standard and Controlled engineering issues MUST include:

```markdown
## Problem or decision

## User, scientific, or operational impact

## Evidence and reproduction

## Scope

## Non-scope

## Acceptance criteria

## Risk classification
- Statistical:
- Security:
- Client data:
- Compatibility and operations:

## Dependencies and related decisions

## Owner
```

Defects MUST include a minimal reproduction or explain why one cannot be shared. Attachments MUST use synthetic, public, or explicitly authorized data. Security vulnerabilities and restricted client information MUST be reported through approved private channels.

Lightweight work MAY use a compact issue or pull-request brief containing only outcome, acceptance evidence, risk classification, and owner. The [review standard](../SPECIFICATION/handbook-review-standard.md) owns risk classification; the [operating modes profile](../profiles/operating-modes.md) maps it to evidence depth.

## 6. Best Practices

- Write acceptance criteria as observable outcomes.
- Include environment and version for defects.
- Link related ADRs, releases, and validation evidence.
- Split issues that have independent acceptance criteria.
- Record unanswered questions rather than converting them into assumptions.

## 7. Examples

### Example: precise defect

"Scoring rejects a valid all-zero response vector in version 1.3.0" is actionable when it includes a synthetic fixture, expected behavior, observed error, environment, and regression acceptance criterion.

## 8. Checklist

- [ ] Problem, impact, evidence, scope, and non-scope are clear.
- [ ] Acceptance criteria are observable.
- [ ] Statistical, security, client-data, and compatibility risks are classified.
- [ ] Reproduction artifacts are safe to share.
- [ ] Owner and dependencies are identified.

## 9. Summary

A good issue creates a bounded, evidence-driven starting point for the engineering workflow.

## 10. References

- [Engineering Workflow](03-engineering-workflow.md)
- [Client Data Policy](22-client-data-policy.md)
