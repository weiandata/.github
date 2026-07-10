# Architecture Decision Records

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Architecture Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how material engineering decisions and their rationale are preserved.

## 2. Scope

It applies to decisions with lasting architectural, statistical, security, data, dependency, compatibility, cost, or operational consequences.

## 3. Philosophy

An Architecture Decision Record (ADR) captures why a choice was reasonable at the time. It prevents future maintainers and AI agents from reconstructing rationale from code alone.

## 4. Principles

- Record decisions when alternatives and consequences matter.
- Keep each ADR focused on one decision.
- Preserve history by superseding rather than rewriting accepted decisions.
- Separate context and evidence from the final decision.
- State consequences and review triggers honestly.

## 5. Standards

An ADR MUST be created before or with a material decision that:

- establishes or changes a system boundary or public interface;
- selects a difficult-to-reverse dependency or service;
- changes data location, classification, or trust boundary;
- changes a statistical estimator, scale, or interpretation;
- accepts a material trade-off, exception, or operational risk;
- creates an incompatible migration.

Each ADR MUST contain identifier, title, status, date, owners, context, decision drivers, considered options, decision, consequences, validation evidence, security and data implications, and review triggers. Status values are Proposed, Accepted, Superseded, Rejected, and Retired.

Accepted ADRs MUST NOT be edited to change the historical decision. A new ADR MUST supersede them.

## 6. Best Practices

- Write the ADR while alternatives are still understood.
- Include a "do nothing" option when meaningful.
- Link benchmarks, experiments, threat models, and statistical evidence.
- Record uncertainty and what would cause reconsideration.
- Keep implementation detail in the repository documentation.

## 7. Examples

```text
ADR-0007: Execute restricted survey scoring inside the client environment
Status: Accepted
Decision: Deliver a signed, reproducible tool; do not transfer raw responses.
Consequences: Client-side environment support is required; confidentiality risk is reduced.
Review trigger: Contract or execution environment changes.
```

## 8. Checklist

- [ ] The decision is material and focused.
- [ ] Context, drivers, options, evidence, and consequences are complete.
- [ ] Statistical, security, data, and operational impacts are explicit.
- [ ] Owners and review triggers are identified.
- [ ] A prior decision is superseded rather than rewritten, if applicable.

## 9. Summary

ADRs preserve material decisions as reviewable company knowledge.

## 10. References

- [Engineering Philosophy](02-engineering-philosophy.md)
- [AI Knowledge Management](20-ai-knowledge-management.md)

