# Engineering Handbook Changelog

All notable changes to the WeianData Engineering Handbook are recorded here. The handbook uses Semantic Versioning.

## [1.2.0] - 2026-07-14

### Added

- Canonical legal-identity registry for company, maintainer, contact, and
  CODEOWNER values.
- Copyright and Licensing Policy with the stable rule identifier
  `WD-LICENSE-001`.
- Mandatory GPL version 2 or later profile for R packages, including dependency
  copyright boundary notices.
- Canonical proprietary profile for websites, internal frameworks, the
  organization policy repository, and the repository template.

### Changed

- Repository, dependency, open-source, template, and README standards now link
  to the single owning copyright and licensing policy.
- Software, client-delivery, and open-source-release routes now include the
  copyright and licensing chapter.

## [1.1.0] - 2026-07-10

### Added

- Lightweight, Standard, and Controlled operating modes tied to R1-R4 risk classes.
- A client-delivery profile and reusable delivery record for tool-and-data isolation projects.
- A one-to-twenty-person team-evolution profile.
- A machine-readable handbook manifest with task-to-chapter routes.
- A stable, non-normative rule registry linked to authoritative source sections.
- Continuous-integration validation for structure, links, manifest, routes, rule ownership, and exact normative duplication.
- A controlled review-exception record.

### Changed

- Clarified that company-wide standards belong in the handbook while repository-local implementation may specialize them.
- Consolidated client-data rules under the Client Data Policy and Git controls under the Git Standards.
- Made issue, pull-request, repository, and workflow evidence proportional to operating risk.
- Defined a viable second-human review path for founder-led Controlled client or public reliance.
- Prioritized active client delivery and statistical evidence ahead of generic repository rollout.
- Made References optional in validation as required by the master specification.

### Fixed

- Removed semantic duplication across branch, repository, security, AI, and client-data controls.
- Resolved the conflict between a one-person operating model and high-risk external review requirements.
- Replaced hard-coded chapter discovery with manifest-driven validation.

## [1.0.0] - 2026-07-10

### Added

- The Engineering Handbook Authoring Constitution.
- The operational handbook specification, style guide, review standard, and roadmap.
- Thirty-six numbered chapters across engineering principles, software engineering, statistical engineering, AI engineering, security and governance, open source, and appendices.
- Company-specific tool-and-data isolation controls for client delivery.
- Statistical validation requirements for measurement, IRT, simulation, benchmarking, and reproducibility.
- AI development, prompt, agent-collaboration, code-review, and knowledge-management standards.
- Repository, Git, release, governance, dependency, and open-source standards.
- The canonical table of contents and v1.0.0 validation report.

### Publication note

This is the first complete, approved handbook release. It establishes the baseline for future repository templates, automated checks, and project adoption.
