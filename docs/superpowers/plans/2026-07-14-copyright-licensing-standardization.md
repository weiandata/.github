# Copyright and Licensing Standardization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the approved canonical company identity and GPL/proprietary licensing model to all ten repositories and encode it in the Handbook, WAEF, and repository template.

**Architecture:** The Engineering Handbook is the normative policy source, WAEF maps that policy to repository profiles, and repository-template supplies reusable licensing files. Existing repositories consume the correct profile: five R packages use GPL (>= 2) with dependency copyright boundaries; organization policy, WAEF, the template itself, and both websites use the proprietary notice.

**Tech Stack:** Markdown, JSON, R DESCRIPTION metadata, R package source archives, Git, existing Python repository validators.

## Global Constraints

- Chinese legal name: `惟安数据科技（北京）有限公司`.
- English legal name and copyright holder: `WEIAN DATA TECH (Beijing) Co., Ltd.`.
- Brand: `WEIAN DATA`.
- Human author and maintainer: `Kunxiang Ma` / `马崑翔`.
- Maintainer email: `makunxiang@weiandata.com`.
- Company, security, and licensing email: `contact@weiandata.com`.
- Default CODEOWNER: `@makunxiang-weiandata`.
- Current copyright year: `2026`.
- All current and future R packages use `GPL (>= 2)` and `inst/COPYRIGHTS`.
- Websites, WAEF, `.github`, and repository-template are proprietary.
- Do not rewrite Git history, publish to CRAN, push branches, or change APIs, algorithms, website business copy, or visual design.
- Do not run CodeGraph.

---

### Task 1: Publish the Handbook policy as version 1.2.0

**Files:**
- Create: `.github/handbook/chapters/36-copyright-and-licensing-policy.md`
- Create: `.github/CODEOWNERS`
- Modify: `.github/PROPRIETARY.md`
- Modify: `.github/README.md`
- Modify: `.github/profile/README.md`
- Modify: `.github/handbook/README.md`
- Modify: `.github/handbook/CHANGELOG.md`
- Modify: `.github/handbook/handbook-manifest.json`
- Modify: `.github/handbook/rule-registry.json`
- Modify: `.github/handbook/chapters/04-repository-standards.md`
- Modify: `.github/handbook/chapters/25-dependency-management.md`
- Modify: `.github/handbook/chapters/26-open-source-policy.md`
- Modify: `.github/handbook/chapters/27-repository-template.md`
- Modify: `.github/handbook/chapters/28-readme-standard.md`
- Create after validation: `.github/handbook/RELEASES/v1.2-validation-report.md`

**Interfaces:**
- Consumes: approved design in `.github/handbook/SPECIFICATION/2026-07-14-copyright-licensing-standardization-design.md`.
- Produces: normative rule `WD-LICENSE-001`, canonical identity, repository-profile selection rules, and Handbook 1.2.0 metadata.

- [ ] **Step 1: Add the owning policy chapter**

Write all ten required chapter sections. Its Standards section must define the canonical identity, GPL R-package requirements, proprietary repository requirements, maintainer/contact separation, dependency-boundary notice, exceptions, and precedence.

- [ ] **Step 2: Link existing chapters to the owning policy**

Replace generic “choose a license” language with links to chapter 36. Keep chapter 26 responsible for publication approval and chapter 25 responsible for dependency review; do not duplicate chapter 36’s exact rules.

- [ ] **Step 3: Update machine-readable indexes and release metadata**

Add chapter `36`, rule `WD-LICENSE-001`, and include chapter 36 in `software_change`, `client_tool_delivery`, and `open_source_release` routes. Bump the Handbook artifact version from 1.1.0 to 1.2.0 and add the changelog entry.

- [ ] **Step 4: Apply the proprietary notice and ownership files**

Use the full company name, 2026, all rights reserved, and `contact@weiandata.com`; add `* @makunxiang-weiandata` to CODEOWNERS.

- [ ] **Step 5: Validate the Handbook**

Run: `python3 handbook/tools/validate_handbook.py`

Expected: exit 0 with all chapters, links, manifest entries, and rules valid.

### Task 2: Release WAEF 3.0 with mandatory licensing profiles

**Files:**
- Create: `WAEF/PROPRIETARY.md`
- Create: `WAEF/CODEOWNERS`
- Create: `WAEF/SECURITY.md`
- Create: `WAEF/docs/COPYRIGHT_LICENSING_STANDARD.md`
- Create: `WAEF/docs/governance/WAEF-3.0-migration.md`
- Create: `WAEF/tests/scenarios/BT-011-wrong-license-profile.md`
- Modify: `WAEF/AGENTS.md`
- Modify: `WAEF/README.md`
- Modify: `WAEF/CHANGELOG.md`
- Modify: `WAEF/docs/project-profiles/r-package.md`
- Modify: `WAEF/docs/project-profiles/static-website.md`
- Modify: `WAEF/docs/project-profiles/README.md`
- Modify: `WAEF/tests/README.md`

**Interfaces:**
- Consumes: Handbook chapter 36 and canonical identity.
- Produces: WAEF 3.0 MUST rules for profile licensing and a behavioral scenario that rejects the wrong license profile.

- [ ] **Step 1: Add the generic standard and governance files**

The standard must link to the Handbook owner, require profile selection, and define validation evidence without becoming a competing company-wide authority. Because this introduces new MUST rules, set WAEF to 3.0 and include a migration note.

- [ ] **Step 2: Strengthen the R-package and static-website profiles**

R packages must verify `License: GPL (>= 2)`, canonical `Authors@R`, root GPL text, and `inst/COPYRIGHTS`. Static websites must verify the canonical proprietary notice and preserve article authorship separately.

- [ ] **Step 3: Add repository governance files and behavioral coverage**

Add the proprietary notice, CODEOWNERS, security contact, and BT-011 scenario. Update the scenario index count from 10 to 11.

- [ ] **Step 4: Run WAEF self-checks**

Run Markdown link and required-section checks described in `WAEF/tests/README.md`; manually verify BT-011 has Trigger, Expected Behavior, Pass Criteria, and Failure Criteria sections.

Expected: no broken internal links and all 11 scenarios structurally complete.

### Task 3: Make repository-template proprietary and add profile assets

**Files:**
- Delete: `repository-template/LICENSE`
- Create: `repository-template/PROPRIETARY.md`
- Create: `repository-template/templates/licensing/README.md`
- Create: `repository-template/templates/licensing/r-package/LICENSE`
- Create: `repository-template/templates/licensing/r-package/DESCRIPTION-identity.txt`
- Create: `repository-template/templates/licensing/r-package/inst/COPYRIGHTS`
- Create: `repository-template/templates/licensing/proprietary/PROPRIETARY.md`
- Modify: `repository-template/README.md`
- Modify: `repository-template/CHANGELOG.md`
- Modify: `repository-template/docs/README.md`
- Modify: `repository-template/docs/repository-standard.md`
- Modify: `repository-template/docs/Repository_Template_Development_Guide.md`

**Interfaces:**
- Consumes: Handbook chapter 36 and WAEF profiles.
- Produces: copy-ready GPL R-package files and proprietary-project files while keeping the template repository itself proprietary.

- [ ] **Step 1: Replace the template repository’s placeholder license**

Delete the non-granting LICENSE placeholder and add the canonical proprietary notice. Update the README tree and License section accordingly.

- [ ] **Step 2: Add licensing profile assets**

The R-package identity snippet must show Kunxiang Ma as `aut/cre` with `makunxiang@weiandata.com` and the company as `cph/fnd` with `contact@weiandata.com`. The dependency notice must contain explicit fields for package, use, upstream project, license, bundling status, and copyright owner.

- [ ] **Step 3: Update template guidance**

Document deterministic selection: R package -> GPL profile; static website/WAEF-style framework -> proprietary profile; other project types require accountable approval before publication.

- [ ] **Step 4: Validate template Markdown and placeholders**

Run the repository’s Markdown and link checks from `.github/workflows/ci.yml` where the local tools are available. Run `rg` to ensure `LICENSE PLACEHOLDER`, Gmail, and example maintainer addresses are absent.

Expected: checks pass or unavailable tools are reported explicitly; forbidden placeholders return no matches.

### Task 4: Migrate DCC, WFC, mergecalib, and ratecalib to GPL and normalize IRTC

**Files:**
- Modify: `DCC/DESCRIPTION`, `DCC/LICENSE`, `DCC/README.md`, `DCC/NEWS.md`, `DCC/CHANGELOG.md`, `DCC/docs/development-notes.md`, `DCC/docs/repository-standard.md`, `DCC/docs/Repository_Template_Development_Guide.md`
- Delete: `DCC/LICENSE.md`
- Create: `DCC/inst/COPYRIGHTS`
- Modify: `IRTC/DESCRIPTION`, `IRTC/README.md`, `IRTC/CHANGELOG.md`, `IRTC/cran-comments.md`, `IRTC/docs/repository-standard.md`
- Modify: `WFC/AGENTS.md`, `WFC/DESCRIPTION`, `WFC/LICENSE`, `WFC/README.md`, `WFC/README.zh-CN.md`, `WFC/NEWS.md`, `WFC/cran-comments.md`, `WFC/docs/repository-standard.md`, `WFC/docs/superpowers/plans/2026-07-09-initial-r-package.md`
- Delete: `WFC/LICENSE.md`
- Create: `WFC/inst/COPYRIGHTS`
- Modify: `mergecalib/DESCRIPTION`, `mergecalib/LICENSE`, `mergecalib/README.md`, `mergecalib/NEWS.md`, `mergecalib/cran-comments.md`, `mergecalib/docs/README.md`, `mergecalib/docs/repository-standard.md`, `mergecalib/man/mergecalib-package.Rd`, `mergecalib/vignettes/mergecalib.Rmd`
- Delete: `mergecalib/docs/LICENSE.md`
- Create: `mergecalib/inst/COPYRIGHTS`
- Modify: `ratecalib/AGENTS.md`, `ratecalib/CHANGELOG.md`, `ratecalib/DISCLAIMER.md`, `ratecalib/LICENSE`, `ratecalib/README.md`, `ratecalib/cran-comments.md`, `ratecalib/docs/PLAIN-GUIDE.md`, `ratecalib/docs/user-manual.md`, `ratecalib/docs/repository-standard.md`, `ratecalib/package/DESCRIPTION`, `ratecalib/package/LICENSE`, `ratecalib/package/NEWS.md`, `ratecalib/package/inst/DISCLAIMER.md`, `ratecalib/release/README.md`, `ratecalib/release/ratecalib_0.3.1.tar.gz`
- Create: `ratecalib/package/inst/COPYRIGHTS`

**Interfaces:**
- Consumes: GPL text from `IRTC/LICENSE`, dependency metadata from each `DESCRIPTION`, and canonical identity.
- Produces: five consistent GPL R packages, each with a human maintainer, company copyright holder/funder, and dependency boundary notice.

- [ ] **Step 1: Build verified dependency inventories**

Parse Imports, LinkingTo, and material Suggests from each DESCRIPTION. Use installed R metadata or authoritative upstream metadata for license strings; do not guess. Record separately distributed dependencies and whether any source is bundled.

- [ ] **Step 2: Apply canonical DESCRIPTION metadata**

For all five packages use:

```r
Authors@R: c(
    person("Kunxiang", "Ma", role = c("aut", "cre"),
           email = "makunxiang@weiandata.com"),
    person("WEIAN DATA TECH (Beijing) Co., Ltd.",
           role = c("cph", "fnd"), email = "contact@weiandata.com"))
License: GPL (>= 2)
Copyright: See file inst/COPYRIGHTS.
```

Preserve package-specific fields and descriptions.

- [ ] **Step 3: Replace MIT license files and add dependency notices**

Use the existing IRTC GPLv2 text as the repository GPL text. Remove MIT-only secondary files and update links to root LICENSE. Each `inst/COPYRIGHTS` must identify company ownership and keep dependency copyrights with upstream owners.

- [ ] **Step 4: Update active documentation and release notes**

Replace MIT claims, Gmail maintainer addresses, obsolete company spellings, the DCC Chinese-name typo, and the WFC example placeholder. Preserve historical CRAN 0.3.0 facts but label them as historical where retained.

- [ ] **Step 5: Rebuild the unpublished ratecalib 0.3.1 artifact**

Run: `R CMD build package`

Move the resulting `ratecalib_0.3.1.tar.gz` to `release/` using the normal build command or repository tooling, replacing only the unpublished 0.3.1 artifact. Do not change the historical 0.3.0 archive.

- [ ] **Step 6: Validate all R packages**

Run per package: DESCRIPTION parse, focused tests, `R CMD build`, and `R CMD check --no-manual` (or the repository’s documented equivalent). Inspect source tarballs to confirm GPL metadata and `inst/COPYRIGHTS` are included.

Expected: every DESCRIPTION parses; package tests pass; builds exit 0; checks report 0 ERROR and 0 WARNING, with any NOTE listed exactly.

### Task 5: Apply the canonical proprietary notice to both websites

**Files:**
- Modify: `website/PROPRIETARY.md`, `website/README.md`, `website/article.html`, `website/index.html`, `website/tools.html`, `website/en/article.html`, `website/en/index.html`, `website/en/learn.html`, `website/en/methods.html`, `website/en/tools.html`, `website/articles/A04.md`, `website/articles-en/A04.md`, `website/docs/WeianData_Website_Repository_Migration_Guide.md`, `website/docs/external-dependencies.md`, `website/docs/repository-standard.md`, `website/docs/Repository_Template_Development_Guide.md`, `website/docs/website-audit.md`
- Modify: `website-global-preview/PROPRIETARY.md`, `website-global-preview/README.md`, `website-global-preview/article.html`, `website-global-preview/index.html`, `website-global-preview/learn.html`, `website-global-preview/methods.html`, `website-global-preview/tools.html`, `website-global-preview/zh/index.html`, `website-global-preview/zh/tools.html`, `website-global-preview/articles/A04.md`, `website-global-preview/articles-en/A04.md`, `website-global-preview/docs/WeianData_Website_Repository_Migration_Guide.md`, `website-global-preview/docs/external-dependencies.md`, `website-global-preview/docs/repository-standard.md`, `website-global-preview/docs/Repository_Template_Development_Guide.md`, `website-global-preview/docs/website-audit.md`

**Interfaces:**
- Consumes: canonical proprietary notice and website attribution rule.
- Produces: consistent repository notices, footers, structured data, and article attribution without changing business meaning or design.

- [ ] **Step 1: Normalize repository and page-level legal identity**

Replace legal uses of `WeianData`, `WEIAN Data Technology...`, and `Weian Data Technology...` with the canonical legal name. Preserve URLs, repository names, file names, and product branding where they are not legal identity fields.

- [ ] **Step 2: Preserve article authorship**

Keep Ma Kunxiang/马崑翔 as author and the company as copyright holder. Use `contact@weiandata.com` for licensing requests.

- [ ] **Step 3: Run both website validators**

Run: `python3 scripts/validate_site.py` in each website repository.

Expected: exit 0 in both repositories.

### Task 6: Cross-repository consistency audit and validation report

**Files:**
- Create: `.github/handbook/RELEASES/v1.2-validation-report.md`
- Modify if evidence requires correction: only files already listed in Tasks 1-5.

**Interfaces:**
- Consumes: all migrated repositories and fresh command output.
- Produces: acceptance-criterion evidence and an exact list of any remaining limitations.

- [ ] **Step 1: Run forbidden-value scans**

Scan active text files outside `.git`, generated `dist`, vendor assets, and historical `ratecalib_0.3.0.tar.gz` for Gmail, example maintainer email, obsolete English legal names, and the DCC Chinese typo.

Expected: no active authoritative matches. Historical references must be explicitly labeled and must not be copyable current guidance.

- [ ] **Step 2: Run profile-presence checks**

Verify all five R packages contain parseable DESCRIPTION, GPL text, `inst/COPYRIGHTS`, canonical authors, company contact, and CODEOWNERS. Verify all five proprietary repositories contain the canonical proprietary notice and CODEOWNERS/security files where required.

- [ ] **Step 3: Run repository-specific validation**

Run Handbook validator, WAEF self-checks, both website validators, `git diff --check` in every repository, and the R package commands from Task 4.

- [ ] **Step 4: Write the 1.2 validation report**

Record commands, exit codes, test/check counts, known CRAN historical state, and any environmental limitation. Do not claim CI or CRAN publication.

- [ ] **Step 5: Review final diffs and statuses**

Run `git status --short` and `git diff --stat` in all ten repositories. Confirm no secret, client data, `.DS_Store`, `.codegraph`, build directory, or unrelated file entered the changes.

Expected: only planned files changed, with no whitespace errors or untracked build debris.
