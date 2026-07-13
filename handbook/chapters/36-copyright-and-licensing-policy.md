# Copyright and Licensing Policy

| Field | Value |
|---|---|
| Version | 1.0.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-14 |

## 1. Purpose

This chapter defines the canonical identity, copyright ownership, maintainer
identity, contact roles, and repository licensing profiles used by WeianData.

## 2. Scope

It applies to every company-controlled repository, R package, website,
framework, template, release artifact, and public package registry record.

## 3. Philosophy

Rights and responsibilities should remain unambiguous from source repository
through distributed artifact. A project must identify its human maintainer,
company copyright holder, third-party boundaries, and permitted uses without
forcing readers to reconstruct intent from inconsistent files.

## 4. Principles

- Keep legal identity in one controlled registry.
- Separate human authorship and maintenance from company ownership.
- Apply licensing by repository profile, not by ad hoc local preference.
- Preserve third-party ownership and license boundaries.
- Correct published metadata through new releases rather than rewritten
  history.

## 5. Standards

Repositories MUST use the exact identity values in the controlled repository
file `LEGAL-IDENTITY.md`. The individual maintainer address identifies the
human CRAN maintainer and Git author. The company address is used for company
enquiries, security reports, licensing, and permissions and MUST NOT replace
the human Git author identity.

Every current and future WeianData R package MUST:

- declare `License: GPL (>= 2)` in `DESCRIPTION`;
- record Kunxiang Ma as `aut` and `cre` with the maintainer email;
- record the company as `cph` and `fnd` with the company contact email;
- include the GNU General Public License version 2 text at the package root;
- ship `inst/COPYRIGHTS` identifying company ownership and separately
  distributed dependency boundaries;
- keep README, NEWS, CRAN comments, generated metadata, and release artifacts
  consistent with the package metadata.

Static websites, WAEF-style internal frameworks, the organization policy
repository, and the repository template itself MUST use the canonical
proprietary notice. That notice MUST include the full company name, copyright
year, all-rights-reserved statement, and company contact address. Website
article notices MUST keep the company as copyright holder while recording the
individual author separately.

The repository template MUST provide profile-specific licensing assets. An R
package selects the GPL profile. A static website or WAEF-style internal
framework selects the proprietary profile. Any other project type MUST NOT be
published until an accountable owner selects an approved profile or records an
exception.

Dependency copyright notices MUST state each material dependency's use,
upstream project, license when verified, bundling status, and retained upstream
ownership. A dependency listing MUST NOT imply ownership transfer, endorsement,
or a change to the dependency's license.

An exception requires accountable owner approval, documented rights and
compatibility review, scope, duration, and migration or review date. Historical
Git and CRAN records MUST NOT be rewritten; corrected public metadata is issued
through a new reviewed release.

## 6. Best Practices

- Generate package notices from reviewed dependency metadata.
- Use stable company-controlled maintainer addresses for public registries.
- Check repository and built-artifact metadata in the same release gate.
- Keep copyright notices concise and link detailed boundaries from the README.

## 7. Examples

### Example: R package

The package records the individual as author and maintainer, the company as
copyright holder and funder, declares GPL version 2 or later, and ships a
dependency notice that states external package source is not bundled.

### Example: static website

The repository carries the proprietary notice. Article pages separately name
the company as copyright holder, the individual writer as author, and the
company contact address for permission requests.

## 8. Checklist

- [ ] Identity values match `LEGAL-IDENTITY.md` exactly.
- [ ] The repository selected the required licensing profile.
- [ ] Human maintainer and company contact roles are separate.
- [ ] Dependencies retain verified ownership and license boundaries.
- [ ] README, metadata, notices, and release artifacts agree.
- [ ] Any exception has accountable approval and a review date.

## 9. Summary

WeianData uses one controlled identity, GPL version 2 or later for R packages,
and the canonical proprietary notice for websites, internal frameworks, policy,
and template repositories.

## 10. References

- [Repository Standards](04-repository-standards.md)
- [Dependency Management](25-dependency-management.md)
- [Open Source Policy](26-open-source-policy.md)
- [Repository Template](27-repository-template.md)
- [README Standard](28-readme-standard.md)
