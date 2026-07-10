# Naming Convention

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## 1. Purpose

This appendix defines stable naming rules for documents, repositories, branches, code, data fields, and artifacts.

## 2. Scope

It applies across company engineering unless an ecosystem or external interface requires a different convention.

## 3. Philosophy

Names are interfaces. They should communicate domain meaning, remain stable, and avoid dependence on private context.

## 4. Principles

- Prefer domain meaning over implementation detail.
- Use one name for one concept.
- Follow language-native conventions where they improve interoperability.
- Avoid dates, versions, and status words in canonical names unless they are part of the identity.
- Expand unfamiliar acronyms on first use.

## 5. Standards

- Markdown documents and directories MUST use lowercase kebab-case, except ecosystem-required names such as `README.md`, `LICENSE`, and `CHANGELOG.md`.
- Repositories MUST use concise lowercase kebab-case.
- Branches MUST follow `<category>/<kebab-case-topic>` as defined by the branching strategy.
- Code MUST follow the declared language convention consistently.
- Public interface names MUST be descriptive and MUST NOT encode temporary implementation choices.
- Data fields MUST define meaning, type, units, allowed values, missing-value representation, and versioned schema ownership.
- Boolean names SHOULD read as predicates, such as `is_valid` or `has_converged`.
- Units SHOULD appear in a name when ambiguity is plausible, such as `timeout_seconds`.

Names such as `final`, `new`, `latest`, `temp`, `misc`, `data2`, and person initials MUST NOT be used as durable identifiers without a domain-specific meaning.

## 6. Best Practices

- Use a glossary term before inventing a synonym.
- Keep abbreviations conventional within measurement or software engineering.
- Name functions for actions and data types for concepts.
- Use identifiers rather than names as join keys.
- Review names as part of public API review.

## 7. Examples

| Avoid | Prefer |
|---|---|
| `FinalAnalysis2.md` | `score-validation.md` |
| `feature/newIRT` | `feature/irt-fit-diagnostics` |
| `x1` | `item_difficulty` |
| `timeout` | `timeout_seconds` |

## 8. Checklist

- [ ] Names express stable domain meaning.
- [ ] Files, repositories, and branches follow their required form.
- [ ] Code follows one declared language convention.
- [ ] Data fields define units, values, missingness, and schema ownership.
- [ ] Temporary, personal, or ambiguous names are absent.

## 9. Summary

Stable, descriptive names reduce ambiguity for maintainers, clients, and AI agents.

## 10. References

- [Branching Strategy](06-branching-strategy.md)
- [Glossary](35-glossary.md)

