# AI Agent Collaboration

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | AI and Engineering Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines safe coordination between humans and one or more AI agents.

## 2. Scope

It applies to delegated implementation, research assistance, review, documentation, test generation, and multi-agent workflows.

## 3. Philosophy

Parallel capability creates value only when ownership, write scope, evidence, and integration remain controlled.

## 4. Principles

- One accountable human owns the overall outcome.
- One coordinator owns task decomposition and integration.
- Each agent receives a bounded objective and explicit permissions.
- Evidence travels with every handoff.
- Independent review must not become circular AI endorsement.

## 5. Standards

An agent task MUST define objective, inputs, applicable rules, allowed tools, write scope, deliverables, verification, and stop conditions. In multi-agent work:

- tasks MUST have non-overlapping ownership or an explicit integration protocol;
- only one actor MAY own a file or mutable artifact at a time unless edits are serialized;
- agents MUST report assumptions, files changed, commands run, evidence, and unresolved risks;
- the coordinator MUST inspect primary artifacts before integration;
- high-risk conclusions require a qualified human reviewer;
- agents MUST NOT expand scope, disclose data, publish, or perform irreversible actions without authority;
- a failed or uncertain result MUST be reported, not concealed by another agent's summary.

Risk classification and human-review separation MUST follow the [operating modes profile](../profiles/operating-modes.md). AI review evidence does not satisfy the second-human requirement for Controlled external reliance.

## 6. Best Practices

- Delegate independent research, implementation, and test work with clear interfaces.
- Keep the smallest useful context per agent.
- Use structured handoffs and deterministic validation.
- Assign an adversarial reviewer for statistical, security, or migration risk.
- Stop parallel work when shared assumptions diverge.

## 7. Examples

### Example: bounded parallel work

One agent implements a parser, another designs independent test fixtures, and a third reviews documentation. They do not edit the same files. The coordinator runs the complete test suite, reviews diffs, resolves contradictions, and obtains human approval for release.

## 8. Checklist

- [ ] The accountable human and coordinating owner are identified.
- [ ] Each agent has a bounded task, permissions, and stop conditions.
- [ ] Mutable ownership does not conflict.
- [ ] Handoffs include primary evidence and unresolved risks.
- [ ] Integrated output receives independent validation and required human approval.

## 9. Summary

AI agents collaborate safely when tasks are bounded, ownership is explicit, evidence is preserved, and humans remain accountable.

## 10. References

- [Prompt Engineering](17-prompt-engineering.md)
- [AI Code Review](19-ai-code-review.md)
