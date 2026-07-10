# AI Development Policy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | AI and Engineering Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines permitted, controlled, and prohibited uses of AI in engineering.

## 2. Scope

It applies to language models, coding assistants, autonomous or semi-autonomous agents, model APIs, local models, and AI-generated engineering artifacts.

## 3. Philosophy

AI accelerates implementation and knowledge work. It does not provide scientific authority, security approval, factual certainty, or accountability.

## 4. Principles

- Match autonomy and review depth to risk.
- Minimize data disclosed to any model or tool.
- Treat generated output as untrusted until verified.
- Preserve human responsibility for scientific and risk-bearing decisions.
- Record enough provenance to review material AI contributions.

## 5. Standards

Before AI use, the operator MUST classify the task:

| Risk | Typical work | Required control |
|---|---|---|
| Low | Drafting, refactoring, test suggestions on non-sensitive code | Normal review and tests |
| Moderate | Production code, architecture options, public technical content | Independent review, tests, provenance |
| High | Statistical interpretation, security logic, client deliverables | Domain review, security or statistical validation, human approval |
| Prohibited | Unauthorized restricted data disclosure, credential handling in prompts, fabricated evidence or approval | Do not perform |

Restricted client data MUST NOT be sent to an external AI service. AI development on client work MUST use approved code, public information, synthetic data, or the minimum de-identified sample permitted by the [client data policy](22-client-data-policy.md). Model and tool retention settings MUST be evaluated before use.

AI output MUST NOT be merged, released, or delivered solely because it compiles, appears plausible, or is endorsed by another AI agent. The accountable human MUST approve high-risk output.

## 6. Best Practices

- Give agents bounded tasks, explicit constraints, and validation commands.
- Use local or client-approved execution when data or code sensitivity requires it.
- Ask AI to expose assumptions and uncertainty.
- Review diffs and primary evidence rather than accepting summaries.
- Prefer deterministic automation for checks that do not require language-model judgment.

## 7. Examples

### Example: permitted client-tool development

An AI agent receives a synthetic schema, expected transformations, tests, and no raw data. It implements the tool. A human reviews the diff, security controls, and statistical behavior. The client executes the approved artifact against real data inside its network.

## 8. Checklist

- [ ] Task, model, tool, data, and autonomy risk are classified.
- [ ] No secret or unauthorized client data is disclosed.
- [ ] Generated output is reviewed and independently verified.
- [ ] Statistical and security gates are complete where applicable.
- [ ] Material provenance and accountable human approval are recorded.

## 9. Summary

AI may perform substantial engineering work, but evidence, data control, and human accountability determine whether its output is acceptable.

## 10. References

- [AI Agent Collaboration](18-ai-agent-collaboration.md)
- [AI Code Review](19-ai-code-review.md)

