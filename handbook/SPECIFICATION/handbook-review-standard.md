# WeianData Engineering Handbook Review Standard

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData |
| Effective date | 2026-07-10 |

## 1. Purpose

This standard defines the evidence and review gates required to approve and publish handbook content.

## 2. Roles

One person MAY hold multiple roles, but each role's decision MUST remain explicit.

| Role | Responsibility |
|---|---|
| Author | Produces the change and self-review evidence |
| Domain reviewer | Checks engineering or statistical correctness |
| Security reviewer | Checks security and client-data impact |
| Editor | Checks language, structure, links, and duplication |
| Accountable approver | Accepts residual risk and approves publication |

An AI agent MAY act as author, analyst, or automated reviewer. It MUST NOT act as the accountable approver.

## 3. Review risk classes

| Class | Examples | Minimum review |
|---|---|---|
| R1 - Editorial | Typo, broken link, clarified wording | Author self-review and automated checks |
| R2 - Operational | New workflow, repository rule, tooling requirement | Domain review and editor review |
| R3 - Scientific or security | Statistical acceptance rule, AI authority, security, client data | Domain or statistical review, security review, accountable approval |
| R4 - Constitutional | Authority, architecture, incompatible standard | All applicable reviews and major-version decision |

If uncertain, use the higher class.

## 4. Review gates

### Gate 1: Constitutional conformity

- The change respects document authority.
- The rule has one owner.
- The required chapter structure and metadata are present.
- No lower-level rule weakens a higher-level rule.

### Gate 2: Technical and scientific correctness

- Requirements are feasible and internally consistent.
- Statistical claims state assumptions, evidence, and limitations.
- Examples do not imply validity beyond their demonstrated conditions.
- Reproducibility and validation requirements are sufficient for the risk.

### Gate 3: Security and confidentiality

- The content exposes no secret, personal data, client identity beyond approved public facts, or restricted schema.
- Client-data guidance conforms to the tool-and-data isolation model.
- Examples use synthetic or public data.
- AI instructions do not authorize restricted-data disclosure.

### Gate 4: Operability

- A human or AI agent can identify required inputs, steps, outputs, and stop conditions.
- Checklists are testable.
- Ownership and escalation paths are clear.
- Exceptions require a durable record.

### Gate 5: Documentation quality

- English, Markdown, naming, and tone comply with the style guide.
- Links and anchors resolve.
- No temporary placeholders or obsolete references remain.
- Diagrams and code blocks render correctly.

### Gate 6: System consistency

- Related chapters reference rather than duplicate the new rule.
- Defined terms match the glossary.
- The table of contents, changelog, and release report are updated when required.
- The change has the correct semantic version impact.

## 5. Statistical review protocol

R3 statistical content MUST be reviewed for:

1. estimand or intended decision;
2. data-generating and sampling assumptions;
3. preprocessing and missing-data treatment;
4. model specification and identification;
5. fit, diagnostics, sensitivity, and uncertainty;
6. independent implementation or benchmark where risk warrants;
7. interpretation limits and failure conditions;
8. reproducibility of the evidence.

A successful software test is not, by itself, evidence of statistical validity.

## 6. Cross-reference validation

The release reviewer MUST verify:

- every Markdown link resolves;
- every numbered chapter appears exactly once in the README;
- filenames are lowercase and hyphen-separated;
- chapter numbers are consecutive;
- required sections are present in order;
- each normative topic has one owner;
- no approved file contains an unresolved drafting marker or placeholder.

Automated checks SHOULD be used, followed by human review for semantic duplication and conflict.

## 7. Review record

Each published release MUST include a validation report containing:

- release identifier and source revision;
- files reviewed;
- automated checks and outcomes;
- domain, statistical, and security review scope;
- known limitations;
- accountable approval statement.

The report MUST distinguish checks actually performed from recommended future checks.

## 8. Exceptions

An exception MUST record the requirement, rationale, risk, compensating control, owner, expiration or review date, and approval. Exceptions MUST be narrow and temporary. An exception MUST NOT override the master specification or authoring constitution.

## 9. Approval criteria

A document may become Approved only when:

- all applicable gates pass;
- review findings are resolved or explicitly accepted;
- the accountable approver is identified;
- version and effective date are correct;
- the document is included in the next validation report.

## 10. Review checklist

- [ ] Risk class is recorded.
- [ ] Required reviewers completed their gates.
- [ ] Statistical and security implications were evaluated.
- [ ] Automated structure and link checks pass.
- [ ] Duplicate and conflicting rules were reviewed semantically.
- [ ] Terms, metadata, table of contents, and changelog are consistent.
- [ ] No sensitive information or unresolved placeholder is present.
- [ ] The accountable human approved publication.
