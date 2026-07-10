# Glossary

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Knowledge Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This appendix defines terms that require consistent interpretation across the handbook.

## 2. Scope

These definitions apply to all handbook documents unless an external standard or client contract explicitly defines a term for its own scope.

## 3. Philosophy

Stable terminology reduces hidden assumptions and improves human and AI interpretation.

## 4. Principles

- Define a term once.
- Prefer established engineering and statistical usage.
- State scope when a term has multiple accepted meanings.
- Update dependent documents when a definition changes materially.

## 5. Standards

**Accountable human**  
The person who accepts responsibility for a decision, approval, release, or residual risk. An AI system cannot be the accountable human.

**AI agent**  
An AI system that performs a bounded task using provided context and, when authorized, tools.

**Architecture Decision Record (ADR)**  
A durable record of a material decision, its context, alternatives, consequences, evidence, and review triggers.

**Client-controlled environment**  
An execution environment whose access, data, and operational controls are administered or explicitly authorized by the client.

**De-identified data**  
Data from which direct identifiers have been removed or transformed. De-identified data may still carry re-identification risk and is not automatically anonymous.

**Evidence artifact**  
A durable, identifiable output that supports verification, validation, review, or a decision.

**Measurement**  
The disciplined assignment and interpretation of scores or values for attributes or constructs, including evidence about reliability, precision, and validity.

**Normative**  
Content that defines required, prohibited, recommended, or optional behavior using the handbook's controlled keywords.

**Reproducibility**  
The ability to regenerate a result from identified inputs, code, environment, configuration, randomness, and execution steps within permitted data boundaries.

**Restricted client data**  
Raw or derived client information requiring the strongest project controls, including direct identifiers, sensitive records, credentials, and data contractually classified as restricted.

**Statistical validation**  
Evidence that a statistical method, implementation, and output are suitable for an intended inference or decision under stated assumptions and limitations.

**Synthetic data**  
Artificially generated data designed to reproduce necessary structure or edge cases without representing real client records.

**Tool-and-data isolation**  
The delivery model in which WeianData develops and validates a tool using approved schemas and synthetic or minimally de-identified samples while real restricted data is processed inside the client's controlled environment.

**Verification**  
Evidence that an implementation behaves according to its specification.

## 6. Best Practices

- Link to a glossary term when ambiguity is plausible.
- Define project-specific terms in the project without changing company-wide meanings.
- Review statistical translations and client terminology with the relevant domain owner.

## 7. Examples

### Example: verification versus validation

Unit tests may verify that a scoring function implements its formula. Recovery studies, fit diagnostics, and intended-use review validate whether that formula and its output are appropriate for the measurement decision.

## 8. Checklist

- [ ] New terms are necessary and not synonyms for existing entries.
- [ ] Definitions are scoped, objective, and used consistently.
- [ ] Dependent chapters are updated for material definition changes.
- [ ] Project or contract definitions are distinguished from handbook definitions.

## 9. Summary

The glossary provides the shared vocabulary required for unambiguous engineering and AI execution.

## 10. References

- [Handbook Style Guide](../SPECIFICATION/handbook-style-guide.md)
- [Naming Convention](32-naming-convention.md)

