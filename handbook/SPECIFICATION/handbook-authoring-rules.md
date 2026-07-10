# WeianData Engineering Handbook Authoring Constitution

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData |
| Effective date | 2026-07-10 |
| Authority | Level 1 - Authoring Constitution |

## 1. Purpose

This constitution defines the immutable rules for creating, changing, reviewing, and publishing the WeianData Engineering Handbook. It converts the principles in the [master specification](engineering-handbook-master-specification.md) into authoring constraints that humans and AI agents can apply deterministically.

## 2. Scope

This constitution applies to every file under `handbook/`, including specifications, chapters, appendices, release notes, examples, and validation reports. It also applies when a handbook rule is quoted or incorporated into another repository.

## 3. Authority and precedence

When documents conflict, use this order:

1. The approved master specification.
2. This authoring constitution.
3. The engineering handbook specification.
4. The style guide and review standard.
5. An owning handbook chapter.
6. Repository-local instructions.
7. Tool defaults, generated suggestions, and informal practice.

A lower-level document MUST NOT weaken a higher-level requirement. A conflict MUST be resolved at its source; it MUST NOT be hidden by adding an exception elsewhere.

## 4. Normative language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative:

- **MUST** and **MUST NOT** define mandatory behavior.
- **SHOULD** and **SHOULD NOT** define the default; deviation requires written rationale.
- **MAY** defines an optional practice.

Rules MUST identify a subject and an observable action. Avoid vague requirements such as "use best judgment" unless the decision criteria are stated.

## 5. Constitutional invariants

Every handbook document MUST:

- be written in English;
- use standard GitHub Markdown;
- be understandable by both engineers and AI agents;
- identify its owner, version, status, and effective date;
- define a stable scope and an explicit source of authority;
- keep normative rules in exactly one owning document;
- link to an owning rule rather than restating it;
- distinguish mandatory standards from examples and recommendations;
- avoid client secrets, personal data, credentials, and restricted data;
- avoid temporary project decisions that belong in an issue, plan, or architecture decision record;
- preserve scientific correctness, reproducibility, security, and maintainability.

## 6. Single-source-of-truth rule

Each normative topic has one owner. The owner is recorded in the [handbook specification](engineering-handbook-specification.md#7-rule-ownership). Other documents MAY summarize the intent in one sentence but MUST link to the owner for the operative rule.

When duplication is discovered:

1. identify the authoritative statement;
2. remove or demote the duplicate to non-normative context;
3. add a relative link to the authoritative statement;
4. validate that no meaning was lost.

## 7. Chapter contract

Every numbered chapter MUST contain these sections in this order:

1. Purpose
2. Scope
3. Philosophy
4. Principles
5. Standards
6. Best Practices
7. Examples
8. Checklist
9. Summary
10. References, when references exist

Each chapter MUST be independently readable while avoiding copied policy. Operational chapters MUST end with an actionable checklist. Examples MUST be clearly labeled non-normative unless they illustrate a mandatory format.

## 8. Evidence and scientific claims

Scientific and statistical requirements MUST identify their assumptions, validation evidence, and limitations. A method MUST NOT be presented as universally valid when its use depends on model fit, sampling, data quality, measurement invariance, or domain judgment.

External facts that materially affect a standard SHOULD cite a primary source. Client-specific facts MUST be documented in the client project, not generalized into the handbook without review.

## 9. Human and AI authorship

AI agents MAY draft, analyze, implement, and validate handbook content. An accountable human owner MUST approve:

- scientific or statistical policy;
- security and client-data policy;
- changes to constitutional or specification-level documents;
- exceptions that alter risk;
- release publication.

AI-generated content MUST be reviewed as untrusted until its claims, links, examples, and internal consistency pass the review standard. An AI agent MUST report uncertainty and MUST NOT invent evidence, client facts, approvals, or completed controls.

## 10. Change control

Every change MUST be classified:

| Change | Version effect | Required review |
|---|---|---|
| Correction with no rule change | Patch | Editorial and link validation |
| New or materially expanded standard | Minor | Domain and cross-reference review |
| Structural redesign or incompatible rule | Major | Constitution, architecture, and migration review |

A change MUST update affected metadata, links, release notes, and validation evidence. Emergency corrections MAY be published quickly, but MUST receive retrospective review before the next release.

## 11. Prohibited authoring patterns

Handbook documents MUST NOT contain:

- unresolved drafting markers or promised future content in an approved release;
- conflicting definitions for the same term;
- rules that depend only on a named individual;
- unbounded phrases such as "always use the latest" without a controlled update process;
- fake citations, unverifiable claims, or implied approvals;
- copied confidential client material;
- marketing claims presented as engineering requirements;
- instructions that bypass statistical validation, security review, or human accountability.

## 12. Enforcement

A document is conformant only when it passes the [handbook review standard](handbook-review-standard.md). Nonconforming content remains Draft and MUST NOT be described as an approved WeianData standard.

Changes to this constitution require a major handbook release unless they only correct wording without changing meaning.
