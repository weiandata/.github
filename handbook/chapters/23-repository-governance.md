# Repository Governance

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Organization Administrator |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines repository creation, ownership, access, transfer, archival, and deletion governance.

## 2. Scope

It applies to repositories owned by WeianData or administered for a client or collaboration.

## 3. Philosophy

Repository administration is a company control. No repository should depend on an individual's private account, memory, or continued availability.

## 4. Principles

- Company work belongs in company-controlled systems.
- Every repository has an accountable owner and maintenance status.
- Access follows least privilege and project need.
- Visibility and transfer are deliberate decisions.
- Archival preserves evidence; deletion is exceptional.

## 5. Standards

Repository creation MUST record purpose, owner, visibility, data classification, license or proprietary status, and expected lifecycle. Company intellectual property MUST be stored in a company-controlled organization unless a contract requires a client-controlled repository.

Administrative access MUST be limited and protected with strong authentication. Protected-branch rules and required reviews MUST be configured for active repositories. Access MUST be reviewed when people, contracts, or project roles change.

Changing a repository from private to public, transferring ownership, deleting it, or removing material history requires accountable approval plus security, client-data, intellectual-property, and license review.

Inactive repositories MUST be marked Archived or Retired, preserve release and provenance information, and identify any successor. Client repositories MUST follow contractual return, retention, and access-removal obligations.

## 6. Best Practices

- Use teams or roles rather than granting permissions individually.
- Maintain at least two recovery-capable organization administrators when staffing permits.
- Review inactive and unowned repositories on a regular cadence.
- Export or preserve critical evidence before external ownership changes.
- Automate baseline settings for new repositories.

## 7. Examples

### Example: client-owned repository

The contract requires development in the client's organization. WeianData records its authorized users and branch controls, avoids copying restricted content elsewhere, and removes access with evidence at project closure.

## 8. Checklist

- [ ] Purpose, owner, visibility, classification, license, and lifecycle are recorded.
- [ ] Administrative and branch controls meet the repository risk.
- [ ] Access is current and least-privileged.
- [ ] Publication, transfer, archive, or deletion received required review.
- [ ] Client and company ownership obligations are satisfied.

## 9. Summary

Repositories are governed company assets with explicit ownership, access, visibility, and lifecycle controls.

## 10. References

- [Repository Standards](04-repository-standards.md)
- [Open Source Policy](26-open-source-policy.md)

