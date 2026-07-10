# Security Policy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | Security Owner |
| Effective date | 2026-07-10 |

## 1. Purpose

This chapter defines the baseline controls for protecting WeianData systems, software, identities, and information.

## 2. Scope

It applies to employees, contractors, AI agents, devices, repositories, cloud services, client tools, development environments, and third-party services.

## 3. Philosophy

Security is a continuous engineering responsibility. Controls should reduce confidentiality, integrity, and availability risk without relying on secrecy, memory, or a single person.

## 4. Principles

- Minimize access, data, exposed surface, and retained secrets.
- Authenticate identities strongly and authorize explicitly.
- Build security into the development lifecycle.
- Detect, contain, recover, and learn from incidents.
- Match controls to data classification and plausible harm.

## 5. Standards

Information MUST be classified as:

| Class | Examples | Minimum handling |
|---|---|---|
| Public | Approved website and open-source content | Integrity and publication review |
| Internal | Routine non-public operations | Authorized company access |
| Confidential | Contracts, private source, business records | Need-to-know access and controlled sharing |
| Restricted | Raw client data, direct identifiers, credentials, private keys | Explicit authorization, strongest available controls, no unapproved transfer |

All material systems MUST implement:

- unique user identities and least privilege;
- multi-factor authentication where supported, especially for administrative access;
- approved secret storage, rotation, and revocation;
- encryption in transit and at rest appropriate to the threat and service;
- supported software, dependency review, and timely risk-based remediation;
- protected source branches and security review in development;
- logging sufficient for investigation without logging secrets or unnecessary personal data;
- tested backup, recovery, and incident response proportional to business impact;
- access removal when a role, project, or service relationship ends.

Security incidents MUST be contained, recorded, investigated, and followed by corrective action. Evidence MUST be preserved without expanding unauthorized access.

## 6. Best Practices

- Prefer managed identity and secret services over locally stored credentials.
- Separate development, testing, and production access.
- Threat-model new external interfaces and data flows.
- Automate dependency, secret, and static checks while retaining human review.
- Exercise recovery and credential-revocation procedures.

## 7. Examples

### Example: restricted client tool

Development uses synthetic data. The deliverable is transferred through an approved channel, verified by checksum, and executed inside the client's controlled environment. WeianData receives only approved aggregate diagnostics.

## 8. Checklist

- [ ] Information, system, and access risks are classified.
- [ ] Identity, least privilege, secrets, and encryption controls are in place.
- [ ] Secure development and dependency checks pass.
- [ ] Logging, backup, recovery, and incident procedures are sufficient.
- [ ] Restricted information is handled only through authorized paths.

## 9. Summary

WeianData protects systems and information through risk-based, testable controls integrated into engineering work.

## 10. References

- [NIST Secure Software Development Framework](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/)
- [Client Data Policy](22-client-data-policy.md)

