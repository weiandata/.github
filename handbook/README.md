# WeianData Engineering Handbook

| Field | Value |
|---|---|
| Release | v1.3.0 |
| Status | Published |
| Owner | WeianData |
| Publication date | 2026-07-15 |

The WeianData Engineering Handbook is the company's engineering operating system. It defines how humans and AI agents build, validate, secure, deliver, and preserve trustworthy software for trustworthy measurement.

## Authority

Read governing documents in this order:

1. [Engineering Handbook Master Specification](SPECIFICATION/engineering-handbook-master-specification.md)
2. [Engineering Handbook Authoring Constitution](SPECIFICATION/handbook-authoring-rules.md)
3. [Engineering Handbook Specification](SPECIFICATION/engineering-handbook-specification.md)
4. [Handbook Style Guide](SPECIFICATION/handbook-style-guide.md)
5. [Handbook Review Standard](SPECIFICATION/handbook-review-standard.md)
6. [Handbook Roadmap](SPECIFICATION/handbook-roadmap.md)

The [authoring constitution](SPECIFICATION/handbook-authoring-rules.md#3-authority-and-precedence) defines conflict precedence. Numbered chapters own operational rules by topic.

## Operating profiles and AI navigation

- [Operating Modes Profile](profiles/operating-modes.md) selects Lightweight, Standard, or Controlled evidence by risk.
- [Client Delivery Profile](profiles/client-delivery-profile.md) applies existing rules to customized client work and tool-and-data isolation.
- [Team Evolution Profile](profiles/team-evolution-profile.md) scales ownership and review from one person to twenty.
- [`handbook-manifest.json`](handbook-manifest.json) provides machine-readable document metadata and task routes.
- [`rule-registry.json`](rule-registry.json) provides stable, non-normative rule identifiers linked to authoritative Markdown sections.

AI agents SHOULD select a task route from the manifest, read the profile and required chapters, and cite stable rule identifiers while treating the linked Markdown as authoritative.

## Recommended reading paths

### Two-hour orientation

Read chapters 00–03, then 11, 13, 16, 21, 22, 30, and the glossary. Use the remaining chapters as task-specific reference.

### Statistical project

Read 03, 08–14, 16–19, 22, 25, and 30.

### Client tool delivery

Start with the [Client Delivery Profile](profiles/client-delivery-profile.md), then read the chapters selected by its manifest route.

### New open-source repository

Read 04–10, 21, 23, 25–34, and 36.

## Part I: Engineering Principles

| No. | Chapter | Primary question |
|---|---|---|
| 00 | [Engineering Handbook](chapters/00-engineering-handbook.md) | How should this system be used? |
| 01 | [Company Mission](chapters/01-company-mission.md) | What outcomes should engineering serve? |
| 02 | [Engineering Philosophy](chapters/02-engineering-philosophy.md) | How are trade-offs decided? |
| 03 | [Engineering Workflow](chapters/03-engineering-workflow.md) | How does work move from request to evidence? |

## Part II: Software Engineering

| No. | Chapter | Primary question |
|---|---|---|
| 04 | [Repository Standards](chapters/04-repository-standards.md) | What must every repository provide? |
| 05 | [Git Standards](chapters/05-git-standards.md) | How is safe, auditable history maintained? |
| 06 | [Branching Strategy](chapters/06-branching-strategy.md) | How are changes isolated and integrated? |
| 07 | [Commit Convention](chapters/07-commit-convention.md) | How are commits described? |
| 08 | [Coding Standards](chapters/08-coding-standards.md) | What makes source code acceptable? |
| 09 | [Documentation Standards](chapters/09-documentation-standards.md) | What must be documented? |
| 10 | [Release Process](chapters/10-release-process.md) | How does reviewed work become a release? |

## Part III: Statistical Engineering

| No. | Chapter | Primary question |
|---|---|---|
| 11 | [Statistical Validation](chapters/11-statistical-validation.md) | What evidence makes a statistical result trustworthy? |
| 12 | [Research Workflow](chapters/12-research-workflow.md) | How is research kept traceable? |
| 13 | [Reproducibility Standard](chapters/13-reproducibility-standard.md) | How can a result be reproduced? |
| 14 | [Simulation Standard](chapters/14-simulation-standard.md) | How are simulation studies made credible? |
| 15 | [Benchmark Standard](chapters/15-benchmark-standard.md) | How is performance measured fairly? |

## Part IV: AI Engineering

| No. | Chapter | Primary question |
|---|---|---|
| 16 | [AI Development Policy](chapters/16-ai-development-policy.md) | What AI use is permitted and controlled? |
| 17 | [Prompt Engineering](chapters/17-prompt-engineering.md) | How is an AI task specified? |
| 18 | [AI Agent Collaboration](chapters/18-ai-agent-collaboration.md) | How do humans and agents coordinate safely? |
| 19 | [AI Code Review](chapters/19-ai-code-review.md) | How is AI-authored code verified? |
| 20 | [AI Knowledge Management](chapters/20-ai-knowledge-management.md) | What knowledge may AI treat as authoritative? |

## Part V: Security and Governance

| No. | Chapter | Primary question |
|---|---|---|
| 21 | [Security Policy](chapters/21-security-policy.md) | What baseline protects systems and information? |
| 22 | [Client Data Policy](chapters/22-client-data-policy.md) | How is real client data kept isolated? |
| 23 | [Repository Governance](chapters/23-repository-governance.md) | Who controls repository lifecycle and access? |
| 24 | [Architecture Decision Records](chapters/24-architecture-decision-records.md) | How are material decisions preserved? |
| 25 | [Dependency Management](chapters/25-dependency-management.md) | How are third-party risks controlled? |

## Part VI: Open Source

| No. | Chapter | Primary question |
|---|---|---|
| 26 | [Open Source Policy](chapters/26-open-source-policy.md) | What may WeianData publish or contribute? |
| 27 | [Repository Template](chapters/27-repository-template.md) | How should a new repository start? |
| 28 | [README Standard](chapters/28-readme-standard.md) | What is the repository front door? |
| 29 | [Issue Template](chapters/29-issue-template.md) | What information begins engineering work? |
| 30 | [Pull Request Standard](chapters/30-pull-request-standard.md) | What evidence is required for review? |
| 31 | [Community Guidelines](chapters/31-community-guidelines.md) | How does public collaboration remain safe and constructive? |

## Appendix

| No. | Chapter | Primary question |
|---|---|---|
| 32 | [Naming Convention](chapters/32-naming-convention.md) | How are durable identifiers named? |
| 33 | [File Structure Convention](chapters/33-file-structure-convention.md) | Where does each kind of file belong? |
| 34 | [Versioning Guide](chapters/34-versioning-guide.md) | How are compatibility changes identified? |
| 35 | [Glossary](chapters/35-glossary.md) | What do shared terms mean? |
| 36 | [Copyright and Licensing Policy](chapters/36-copyright-and-licensing-policy.md) | Which identity and licensing profile must a repository use? |

## Release information

- [Changelog](CHANGELOG.md)
- [v1.2.0 Validation Report](RELEASES/v1.2-validation-report.md)
- [v1.1.0 Validation Report](RELEASES/v1.1-validation-report.md)
- [v1.0.0 Validation Report](RELEASES/v1.0-validation-report.md)

## Using the handbook in a repository

Repository instructions SHOULD link to the applicable owning chapters and state only stricter or project-specific requirements. They MUST NOT copy or weaken company standards.

When a rule is unclear, open a handbook issue that states the affected decision, ambiguous text, and proposed evidence. Do not invent a local interpretation for scientific, security, or client-data requirements.
