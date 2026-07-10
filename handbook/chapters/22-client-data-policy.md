# Client Data Policy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Client Data Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines how WeianData protects client data while delivering customized statistical and engineering tools.

## 2. Scope

It applies to client-provided data, schemas, samples, metadata, outputs, credentials, documentation, communications, backups, logs, AI tools, and subcontractors.

## 3. Philosophy

The default delivery model is tool-and-data isolation: WeianData builds and validates tools with the minimum permitted schema and synthetic or de-identified sample; real restricted data is executed inside the client's controlled environment.

## 4. Principles

- Data does not move merely because a tool can process it.
- Collect and retain only what the approved purpose requires.
- Treat de-identification as risk reduction, not automatic anonymization.
- Keep client ownership, access, location, retention, and outputs explicit.
- Prefer client-side execution for restricted data.

## 5. Standards

Before accessing client information, the project MUST record:

- contractual purpose, permitted data, roles, and approved users;
- classification, sensitivity, identifiers, and re-identification risk;
- permitted storage, processing location, transfer channels, and AI services;
- retention, deletion, backup, incident, and return obligations;
- approved outputs and disclosure thresholds;
- accountable client and WeianData owners.

Restricted client data MUST remain in the client environment unless a written agreement and risk review explicitly authorize another arrangement. It MUST NOT be placed in source control, general-purpose chat, email attachments, public issue trackers, unapproved cloud storage, or external AI prompts.

WeianData development SHOULD use synthetic data that preserves necessary schema and edge cases. If a de-identified sample is required, the project MUST minimize fields and rows, remove direct identifiers, assess linkage risk, restrict access, and delete it according to the approved retention schedule.

Tools delivered for client-side execution MUST include integrity identification, environment requirements, validation checks, logs that avoid sensitive values, and a procedure for returning only approved results or diagnostics.

Projects processing personal information MUST obtain appropriate contractual and legal review for the intended jurisdiction, purpose, transfer, and individual rights. This handbook is an engineering control standard, not a substitute for legal advice.

## 6. Best Practices

- Design against a data contract before receiving any sample.
- Generate statistically realistic synthetic fixtures for development and tests.
- Return counts, aggregates, or redacted diagnostics instead of row-level records.
- Use client-controlled secrets and execution accounts.
- Confirm deletion with an evidence record at project closure.

## 7. Examples

### Example: isolated survey processing

The client supplies a schema and synthetic response file. WeianData builds and validates the pipeline. The client verifies the artifact, runs it on raw survey data in its network, and shares only approved aggregate quality metrics and final tables.

## 8. Checklist

- [ ] Purpose, roles, classification, location, access, and contract are recorded.
- [ ] Development uses the minimum synthetic or permitted de-identified data.
- [ ] Restricted data stays within the approved client environment.
- [ ] AI, storage, transfer, logging, retention, and deletion controls are explicit.
- [ ] Delivered tools have integrity, validation, and safe-output controls.
- [ ] Required contractual and legal review is complete.

## 9. Summary

WeianData delivers precise tools without taking unnecessary custody of real client data.

## 10. References

- [Personal Information Protection Law of the People's Republic of China](https://en.spp.gov.cn/2021-12/29/c_948419.htm)
- [Security Policy](21-security-policy.md)
- [AI Development Policy](16-ai-development-policy.md)

