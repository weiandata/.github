# Client Delivery Profile

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | Client Delivery Owner |
| Effective date | 2026-07-10 |

## Purpose

This profile applies existing handbook standards to customized measurement, statistical-analysis, and client-side tool delivery. It is optimized for WeianData's tool-and-data isolation model and does not create duplicate policy.

## Entry conditions

Use this profile whenever work will be delivered to a client, used to support a client decision, or executed against client-controlled data. Select the Standard or Controlled mode using the [operating modes profile](operating-modes.md).

## Delivery lifecycle

| Stage | Required outcome | Owning standard |
|---|---|---|
| 1. Frame | Problem, intended decision, scope, non-scope, owner, acceptance criteria, and support boundary | [Engineering Workflow](../chapters/03-engineering-workflow.md) |
| 2. Contract data | Permitted schema, classification, location, users, transfers, AI boundary, outputs, retention, and deletion | [Client Data Policy](../chapters/22-client-data-policy.md) |
| 3. Design | Interfaces, execution boundary, model assumptions, failure modes, and material decisions | [Architecture Decision Records](../chapters/24-architecture-decision-records.md) |
| 4. Build | Reviewable source, synthetic fixtures, controlled dependencies, and bounded AI-agent work | [Coding Standards](../chapters/08-coding-standards.md), [AI Agent Collaboration](../chapters/18-ai-agent-collaboration.md) |
| 5. Verify | Software behavior, installation, invalid input, recovery, and client-environment compatibility | [Engineering Workflow](../chapters/03-engineering-workflow.md) |
| 6. Validate | Intended use, assumptions, diagnostics, sensitivity, uncertainty, and limitations | [Statistical Validation](../chapters/11-statistical-validation.md) |
| 7. Package | Immutable artifact, checksum, environment, configuration, instructions, safe logs, and rollback | [Release Process](../chapters/10-release-process.md) |
| 8. Execute and accept | Client-side real-data run, approved output return, acceptance evidence, and unresolved findings | [Client Data Policy](../chapters/22-client-data-policy.md) |
| 9. Close | Handover, support status, retention or deletion evidence, reusable knowledge, and follow-up work | [Documentation Standards](../chapters/09-documentation-standards.md) |

## Tool-and-data isolation package

The delivery package typically contains the artifacts required by the owning standards:

- source or approved executable artifact;
- artifact checksum or immutable identity;
- environment and dependency manifest;
- configuration schema with no secret values;
- synthetic validation fixture and expected output;
- installation, execution, verification, and rollback instructions;
- statistical-method documentation and limitations;
- safe diagnostic procedure that does not export row-level data;
- client acceptance and project-closure record.

The authoritative data-handling requirements remain in the [Client Data Policy](../chapters/22-client-data-policy.md).

## One-person delivery control

The [review standard](../SPECIFICATION/handbook-review-standard.md) permits the founder to perform design, implementation, validation preparation, and accountable approval. Before external reliance on a Controlled statistical, security, or client-data conclusion, that standard requires second-human review of the relevant scope. A qualified and recorded client subject-matter review can satisfy this control.

## Checklist

- [ ] Scope, acceptance, support, and ownership are agreed.
- [ ] Data and AI boundaries are recorded before development.
- [ ] Development and tests use synthetic or explicitly permitted data.
- [ ] Software verification and statistical validation are complete.
- [ ] The client-side package is identifiable, reproducible, and recoverable.
- [ ] Controlled external reliance has the required second-human review.
- [ ] Acceptance, retention or deletion, handover, and closure are recorded.

## Template

Use the [Client Delivery Record](../templates/client-delivery-record.md) to collect evidence without copying policy text.
