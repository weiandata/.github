# Copyright and Licensing Standardization Design

| Field | Value |
|---|---|
| Status | Approved design |
| Owner | WeianData Engineering |
| Approved date | 2026-07-14 |

## 1. Objective

Standardize company identity, copyright ownership, maintainer identity,
contact addresses, and licensing across existing repositories, then encode the
same rules in the Engineering Handbook, WAEF, and the repository template so
new repositories start compliant.

## 2. Canonical identity

- Chinese legal name: `惟安数据科技（北京）有限公司`
- English legal name: `WEIAN DATA TECH (Beijing) Co., Ltd.`
- Public brand: `WEIAN DATA`
- Copyright holder: `WEIAN DATA TECH (Beijing) Co., Ltd.`
- Individual author and maintainer: `Kunxiang Ma` / `马崑翔`
- Maintainer email: `makunxiang@weiandata.com`
- Company, security, and licensing contact: `contact@weiandata.com`
- GitHub organization: `weiandata`
- Default CODEOWNER: `@makunxiang-weiandata`
- Copyright year for the current repository set: `2026`

The maintainer email identifies the human CRAN maintainer and Git author. The
company contact address is not used as a substitute Git author identity.

## 3. Licensing model

### 3.1 R packages

All current and future WeianData R packages use `GPL (>= 2)`. Each package
must:

1. record Kunxiang Ma as `aut` and `cre` with the maintainer email;
2. record the company as `cph` and `fnd` with the company contact address;
3. declare `License: GPL (>= 2)` in `DESCRIPTION`;
4. include the GPL version 2 license text at the package root;
5. include `inst/COPYRIGHTS` describing company ownership and the boundary
   between package code and separately distributed runtime dependencies;
6. keep README, NEWS, release notes, CRAN comments, generated package metadata,
   and source-file notices consistent with this model.

Dependency notices list direct runtime dependencies, their role, upstream
project, and license when known. They state that dependencies remain under
their respective owners and are not bundled unless the repository proves
otherwise. Suggested packages may be listed when they are material to the
distributed feature set, but the notice must not imply that listing a package
changes its license.

Changing the license does not rewrite Git history. Previously published CRAN
metadata remains historical; corrected metadata reaches CRAN through a new
accepted release.

### 3.2 Proprietary repositories

Static websites, WAEF, the organization policy repository, and the repository
template itself are proprietary. Their repository-level notice uses the full
canonical company name, the 2026 copyright year, an all-rights-reserved
statement, and the company contact address. Website article attribution keeps
the company as copyright holder and Ma Kunxiang as author.

### 3.3 Generated repositories

The repository template is proprietary, but its generated projects select a
profile-specific rights model:

- R package profile: GPL (>= 2) plus dependency copyright boundary notice.
- Static website and WAEF-style internal framework profiles: proprietary.
- Any other profile: no publication until an accountable owner selects an
  approved profile or receives a documented exception.

The template must not expose a placeholder license as if it were a grant of
rights.

## 4. Sources of authority

The Engineering Handbook owns the company-wide policy and canonical identity.
WAEF converts that policy into project-profile rules and verification
requirements. The repository template provides reusable files and selection
instructions. Individual repositories implement the selected profile without
redefining company identity.

If these layers conflict, precedence is:

1. approved legal or accountable-owner exception;
2. Engineering Handbook copyright and licensing policy;
3. WAEF project profile;
4. repository template;
5. repository-local documentation.

## 5. Repository migration scope

The migration covers:

- R packages: DCC, IRTC, WFC, mergecalib, and ratecalib;
- proprietary repositories: `.github`, WAEF, repository-template, website,
  and website-global-preview;
- copied repository-standard and template-development documentation where it
  contains conflicting licensing guidance;
- current source, documentation, release metadata, and checked-in release
  artifacts that present authoritative ownership or licensing information.

Historical planning documents remain unchanged only when clearly marked as
historical and incapable of being mistaken for current policy. Placeholder
emails or obsolete identity examples that can be copied into active work are
removed or replaced.

## 6. Validation and failure handling

Validation must prove:

- no active file contains obsolete company names, the personal Gmail
  maintainer address, or the known placeholder maintainer address;
- every R package parses its `DESCRIPTION`, declares `GPL (>= 2)`, contains
  canonical `Authors@R`, and ships `inst/COPYRIGHTS` plus the GPL text;
- every proprietary repository has a canonical proprietary notice;
- CODEOWNERS and security contacts are present where the repository profile
  requires them;
- WAEF behavioral tests and handbook validation pass;
- website repository validators pass;
- R package tests and checks pass in proportion to the metadata and packaging
  changes.

Generated files and release archives must be rebuilt from canonical sources
rather than edited internally. If dependency license data cannot be verified
from installed or repository metadata, the notice records the uncertainty and
the migration stops short of making an unsupported claim.

## 7. Out of scope

- Rewriting Git history or changing past CRAN records.
- Publishing packages to CRAN, pushing branches, or opening pull requests.
- Changing package APIs, algorithms, website business copy, or visual design.
- Changing the selected GPL/proprietary model without a new approved policy
  decision.

## 8. Acceptance criteria

1. All ten repositories use the canonical identity in active authoritative
   files.
2. All five R packages implement the GPL and dependency-boundary model.
3. Both websites, WAEF, `.github`, and repository-template implement the
   proprietary model.
4. The Handbook, WAEF profiles, and repository template encode the rules for
   future repositories.
5. Fresh validation evidence covers string consistency, metadata parsing,
   repository-specific checks, and generated artifacts.
