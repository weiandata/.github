# Team Evolution Profile

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | WeianData |
| Effective date | 2026-07-10 |

## Purpose

This profile shows how the same handbook scales from one person to a team of twenty without changing rule ownership or rebuilding the handbook architecture.

## Evolution model

| Team size | Operating model | Required organizational emphasis |
|---|---|---|
| 1 | Founder holds multiple explicit roles; AI agents perform bounded implementation | Operating-mode selection, client review for Controlled reliance, durable evidence, company-controlled accounts |
| 2–5 | Named repository and project owners; at least two recovery-capable administrators when staffing permits | Second-human review for Controlled work, ownership backup, access removal, shared review queue |
| 6–10 | Stable project or service ownership with delegated technical leads | CODEOWNERS or equivalent, onboarding and offboarding checklist, incident owner, scheduled dependency and method review |
| 11–20 | Multiple accountable delivery groups with cross-cutting statistical and security stewardship | Service catalog, escalation paths, cross-project architecture review, statistical-method steward, security steward, capacity and succession planning |

## Rules that remain stable

At every size:

- the handbook remains the company-wide source of truth;
- repositories may specialize but not weaken handbook standards;
- scientific and security acceptance remains human-accountable;
- client data follows tool-and-data isolation by default;
- AI agents receive bounded authority and evidence requirements;
- repository, decision, release, and knowledge ownership is role-based.

## Promotion triggers

Adopt the next stage's controls before reaching the next headcount when any condition applies:

- one person is the only administrator or recovery path for a critical system;
- review or release queues depend on one unavailable person;
- multiple client projects share code or infrastructure;
- a security or statistical decision affects more than one project;
- onboarding requires repeated oral explanation;
- ownership or incident escalation is ambiguous.

## Compatibility

Moving between stages is normally a backward-compatible v1.x adoption change. Under the [versioning guide](../chapters/34-versioning-guide.md), a major handbook version is required only when authority, ownership, or compatibility rules change incompatibly; growth alone is not sufficient.

## Checklist

- [ ] Current stage and accountable owners are recorded.
- [ ] No critical system depends on an undocumented individual-only recovery path.
- [ ] Review separation matches the current team and risk.
- [ ] Access, onboarding, offboarding, incident, and succession controls match the stage.
- [ ] Promotion triggers are reviewed before adding organizational complexity.

## References

- [Repository Governance](../chapters/23-repository-governance.md)
- [AI Knowledge Management](../chapters/20-ai-knowledge-management.md)
- [Handbook Roadmap](../SPECIFICATION/handbook-roadmap.md)
