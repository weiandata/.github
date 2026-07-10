# Prompt Engineering

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | AI and Engineering Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how to create prompts that produce bounded, reviewable engineering work.

## 2. Scope

It applies to system instructions, task prompts, agent briefs, reusable prompt templates, and model-evaluation cases.

## 3. Philosophy

A prompt is an executable task contract, not a substitute for requirements, evidence, or review.

## 4. Principles

- State the outcome and acceptance criteria first.
- Provide only necessary, authorized context.
- Separate facts, instructions, examples, and untrusted input.
- Define tools, permissions, stop conditions, and output format.
- Validate behavior with representative and adversarial cases.

## 5. Standards

A material engineering prompt MUST identify:

- objective and non-objectives;
- authoritative context and applicable handbook rules;
- inputs, data classification, and prohibited disclosure;
- allowed tools and write boundaries;
- technical, scientific, security, and style constraints;
- expected deliverables and machine-readable format where useful;
- verification commands or evidence;
- uncertainty, escalation, and stop conditions.

Prompts MUST NOT contain secrets or unauthorized restricted data. Content from repositories, documents, web pages, or users MUST be treated as untrusted data unless it is an approved instruction source. An agent MUST NOT follow embedded instructions that conflict with the governing task or handbook.

## 6. Best Practices

- Use concise context linked to source documents.
- Ask for assumptions and unresolved risks in the output.
- Provide examples only when they clarify an exact format.
- Build evaluation cases before optimizing prompt wording.
- Version prompts that affect production behavior.

## 7. Examples

```text
Objective: Implement schema validation for synthetic survey responses.
Authority: coding standards and client data policy.
Inputs: public schema fixture only; no production data.
Deliverable: code, tests, and updated API documentation.
Verification: run the repository test and lint commands.
Stop: report any requirement that would require client data or a breaking API change.
```

## 8. Checklist

- [ ] Objective, scope, constraints, and output are explicit.
- [ ] Context is authorized, minimal, and clearly separated from instructions.
- [ ] Tools, permissions, verification, and stop conditions are defined.
- [ ] Prompt-injection and data-disclosure risks are addressed.
- [ ] Representative evaluation cases pass.

## 9. Summary

Effective prompts create bounded tasks whose outputs can be tested, reviewed, and safely rejected when requirements are unmet.

## 10. References

- [AI Development Policy](16-ai-development-policy.md)
- [AI Knowledge Management](20-ai-knowledge-management.md)

