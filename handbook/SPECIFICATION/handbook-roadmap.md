# WeianData Engineering Handbook Roadmap

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData |
| Effective date | 2026-07-10 |

## 1. Purpose

This roadmap defines the staged creation, publication, adoption, and evolution of the WeianData Engineering Handbook.

## 2. v1.0 publication phases

```mermaid
flowchart TD
    P1["Phase 1: Engineering Constitution"] --> P2["Phase 2: Master Specification"]
    P2 --> P3["Phase 3: Style Guide"]
    P3 --> P4["Phase 4: Review Standard"]
    P4 --> P5["Phase 5: Roadmap"]
    P5 --> P6["Phase 6: Generate Handbook Chapters"]
    P6 --> P7["Phase 7: Cross-reference and Validation"]
    P7 --> P8["Phase 8: Publish v1.0"]
```

| Phase | Deliverable | Exit criterion | v1.0 status |
|---|---|---|---|
| 1 | Authoring constitution | Immutable authoring and authority rules approved | Complete |
| 2 | Master and operational specifications | Architecture, ownership, and lifecycle defined | Complete |
| 3 | Style guide | English and Markdown conventions defined | Complete |
| 4 | Review standard | Review gates and evidence defined | Complete |
| 5 | Roadmap | Publication and adoption sequence defined | Complete |
| 6 | Numbered chapters | All planned engineering domains covered | Complete |
| 7 | Validation | Structure, links, coverage, conflicts, and confidentiality checked | Complete |
| 8 | v1.0 publication | Approved files, changelog, and validation report published | Complete |

## 3. Adoption sequence

After v1.0 publication, WeianData SHOULD adopt the handbook in this order:

1. new repositories inherit the repository template and README standard;
2. active repositories align their workflows without rewriting valid history;
3. client projects adopt data classification and tool-and-data isolation controls;
4. statistical projects adopt validation and reproducibility evidence;
5. AI agents receive the relevant handbook links as task constraints;
6. exceptions and gaps become tracked improvement work.

## 4. v1.1 priorities

The first minor release SHOULD focus on operational enforcement:

- automated handbook structure and link validation in continuous integration;
- reusable repository templates for Python, R, and mixed-language projects;
- architecture decision record and validation-report templates;
- project-level data classification and retention templates;
- reproducibility manifests for statistical deliverables;
- onboarding exercises measured against the two-hour comprehension goal.

These items are planned capabilities, not requirements of v1.0 unless another approved chapter already requires the underlying behavior.

## 5. v1.x maturity goals

- Measure handbook adoption across active repositories.
- Record recurring review findings and simplify unclear standards.
- Add examples from approved, de-identified internal practice.
- Establish scheduled security, dependency, and statistical-method reviews.
- Keep rule ownership stable while improving enforcement.

## 6. v2.0 triggers

A major release SHOULD be considered only when one or more conditions apply:

- the handbook authority model changes;
- repository governance changes incompatibly;
- the company moves from a founder-led operating model to multiple accountable engineering teams;
- a regulated product requires a materially different quality system;
- the handbook directory or chapter contract requires structural redesign.

Growth alone is not a reason for structural redesign. Prefer additive, backward-compatible standards.

## 7. Maintenance cadence

- Review security and client-data standards at least annually and after material incidents or legal changes.
- Review statistical standards when methods, evidence, or intended applications materially change.
- Review AI policy when model capabilities, data handling, or agent autonomy materially change.
- Review the full handbook before each minor or major release.
- Apply patch corrections when an error could mislead implementation.

## 8. Roadmap governance

Roadmap entries MUST identify an outcome, owner, and exit criterion before implementation begins. Dates MAY be added in project planning, but temporary schedules SHOULD remain outside the constitutional specification set.

## 9. Success measures

The roadmap succeeds when:

- new repositories inherit the standards with minimal manual setup;
- client deliveries produce consistent evidence and data controls;
- statistical results can be reproduced independently;
- AI agents can locate authoritative rules without prompt-specific interpretation;
- handbook exceptions and duplicated local policies decline over time.

