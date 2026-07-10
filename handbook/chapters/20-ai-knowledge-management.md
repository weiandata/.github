# AI Knowledge Management

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | Knowledge Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how engineering knowledge is prepared, approved, and maintained for reliable reuse by humans and AI agents.

## 2. Scope

It applies to handbooks, repository instructions, prompts, examples, decision records, runbooks, retrieval indexes, and generated summaries.

## 3. Philosophy

AI is only as reliable as the authority, freshness, scope, and confidentiality of the knowledge it receives. Chat history is not a durable source of truth.

## 4. Principles

- Curate authoritative knowledge before optimizing retrieval.
- Record ownership, version, scope, and effective date.
- Separate approved standards from examples, drafts, and observations.
- Minimize sensitive content and enforce access boundaries.
- Retire obsolete knowledge visibly.

## 5. Standards

Knowledge provided to AI agents MUST:

- identify its authority and owner;
- be versioned or tied to an immutable source revision;
- state intended scope and known limitations;
- use stable terminology and resolvable links;
- exclude secrets and unauthorized client data;
- distinguish normative requirements from non-normative examples;
- have a review and retirement path.

Generated chat summaries, model memories, and vector-index entries MUST NOT become normative without promotion into an approved source document. Retrieval systems MUST preserve source attribution and access control. Conflicting sources MUST be resolved by the handbook authority order.

AI agents SHOULD use `handbook-manifest.json` to select applicable documents and `rule-registry.json` to cite stable rule identifiers. These files are non-normative indexes; the linked Markdown source remains authoritative.

## 6. Best Practices

- Keep repository-specific instructions short and link company standards.
- Test whether agents retrieve the correct source for representative tasks.
- Include negative examples and stop conditions for high-risk work.
- Review stale or low-use knowledge and remove duplication.
- Capture durable decisions after a project rather than preserving raw chat transcripts as policy.

## 7. Examples

### Example: promoting project knowledge

A client project discovers a reusable schema-validation pattern. The team removes client-specific details, validates the pattern, records its scope and limitations, and adds it to the owning engineering document. The original chat remains non-authoritative.

## 8. Checklist

- [ ] Knowledge has an owner, authority, version, scope, and review path.
- [ ] Normative rules are separated from drafts and examples.
- [ ] Access control and data minimization are appropriate.
- [ ] Links and source attribution are preserved.
- [ ] Obsolete, conflicting, or duplicated knowledge is resolved.

## 9. Summary

AI-reusable knowledge must be authoritative, scoped, current, attributable, and safe.

## 10. References

- [Documentation Standards](09-documentation-standards.md)
- [Architecture Decision Records](24-architecture-decision-records.md)
