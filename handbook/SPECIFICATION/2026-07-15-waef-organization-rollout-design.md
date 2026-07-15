# WAEF Organization-Wide Rollout Design

| Field | Value |
|---|---|
| Status | Approved design |
| Owner | WeianData Engineering |
| Approved date | 2026-07-15 |
| Initial target | WAEF 4.0 |

## 1. Objective

Apply the WeianData Agent Engineering Framework (WAEF) to every existing
WeianData repository and make it the mandatory default for every future
repository. The resulting system governs AI coding agents, human contributors,
Pull Requests, CI, review, release, and deployment.

Compliance is enforced through an exact WAEF version lock, a local repository
entry point, private reusable GitHub Actions, required status checks,
CODEOWNERS, organization rulesets, automated upgrade Pull Requests, and daily
drift audits. A WAEF release never changes a consuming repository until that
repository reviews and merges its own upgrade Pull Request.

## 2. Approved decisions

The following decisions are final for this design:

1. WAEF is mandatory, not advisory.
2. WAEF governs AI, developers, Pull Requests, CI, review, release, and
   deployment.
3. Every repository pins one exact WAEF release and immutable commit SHA.
4. WAEF upgrades are proposed by automation and require project review; they
   are never merged automatically.
5. WAEF remains a private repository and the unique source of framework rules.
6. Repositories use a lightweight local entry point and lock file instead of
   copying the framework documents.
7. Compliance failures block merging and publishing by default.
8. The repository template makes the same controls mandatory for future
   projects.

## 3. Current state and reason for WAEF 4.0

The company directory contains eleven independent Git repositories:

- R packages: DCC, IRTC, WFC, mergecalib, and ratecalib;
- static websites: website and website-global-preview;
- organization and governance infrastructure: `.github`, WAEF, and
  repository-template;
- LISTR, a planned statistical and engineering package that has not begun
  product development.

WAEF 3.0 describes itself and its skill library as a framework for AI coding
agents. Extending its mandatory scope to humans, Pull Requests, CI, review,
release, and deployment introduces new obligations that can make a previously
compliant consumer non-compliant. Under WAEF's own versioning policy, that is a
breaking change and requires a new MAJOR release.

The rollout therefore begins with WAEF 4.0. WAEF 4.0 must include a migration
note, a changelog entry, complete framework self-checks, and behavioral tests
covering its expanded governance scope. Existing repositories do not claim
full organization-wide compliance while pinned to WAEF 3.0.

## 4. Authority and precedence

The Engineering Handbook remains the authority for company policy, legal
identity, security posture, and organization-wide governance. WAEF translates
those policies into executable engineering lifecycle requirements, project
profiles, evidence requirements, validation rules, and behavioral tests.
Individual repositories declare their applicable profiles and project-specific
rules.

Precedence is:

1. approved legal or accountable-owner exception;
2. Engineering Handbook policy;
3. repository-specific `AGENTS.md` rules that make requirements stricter;
4. selected WAEF project profiles;
5. WAEF generic standards and lifecycle procedures.

A repository rule may make a WAEF requirement stricter. It may not silently
weaken a WAEF or Handbook MUST requirement. Any necessary relaxation uses the
explicit, time-limited exception process in this design.

## 5. WAEF 4.0 deliverables

WAEF 4.0 adds the framework capabilities required for organization-wide
operation:

- standards and skills addressed to both human and AI participants;
- a version-lock schema and lock validator;
- a private reusable compliance workflow and repository validator;
- machine-readable project-profile requirements;
- governance-framework and repository-template profiles;
- updated R-package and static-website profiles;
- explicit rules for project-local strengthening and approved exceptions;
- behavioral scenarios for lock drift, expired exceptions, missing evidence,
  workflow bypass attempts, human review obligations, and unsafe releases;
- migration instructions from WAEF 3.0;
- test fixtures representing compliant and non-compliant repositories for
  every supported profile.

The actual `v4.0` release commit is written into consumer lock files only after
the release is created. No consuming repository may retain a symbolic or
placeholder commit value.

## 6. System architecture

### 6.1 WAEF repository

The private `weiandata/WAEF` repository owns:

- normative standards, skills, profiles, templates, and behavioral scenarios;
- the lock-file schema;
- the repository validator;
- the private reusable `WAEF Compliance` workflow;
- WAEF release metadata, migration notes, and self-validation evidence.

The repository is configured so private repositories in the `weiandata`
organization may call its reusable workflow. The caller references an immutable
WAEF release commit, not `main` or a mutable version label.

### 6.2 Organization `.github` repository

The private `weiandata/.github` repository owns:

- the Engineering Handbook and policy registry;
- organization audit inventory and reporting;
- WAEF release-to-repository upgrade automation;
- GitHub App configuration documentation;
- organization ruleset configuration and operational runbooks.

### 6.3 Consuming repositories

Each repository stores only its local bootstrap contract, exact WAEF lock,
thin workflow caller, generated GitHub-facing templates, project evidence, and
project-specific rules. Full normative WAEF content is read from the private
pinned source in CI and is cached locally in a gitignored directory for AI and
human use.

### 6.4 Pull Request flow

1. A contributor or AI opens or updates a Pull Request.
2. The repository's thin workflow caller reads the WAEF lock.
3. The caller invokes the private reusable workflow at the same immutable WAEF
   commit recorded by the lock.
4. A least-privilege GitHub App token gives the workflow read access to that
   exact WAEF commit and the metadata required for validation.
5. WAEF validates the repository contract, applicable profiles, Pull Request
   evidence, and machine-checkable lifecycle requirements.
6. The repository's own language- and product-specific CI runs independently.
7. CODEOWNERS review covers protected governance files and human-judgment
   requirements.
8. The organization ruleset permits merging only when all required checks and
   approvals pass.

GitHub supports sharing private actions and reusable workflows inside an
organization, required status checks in repository rulesets on supported paid
plans, and GitHub App installation tokens for cross-repository access. The
implementation must confirm the organization's GitHub plan before enabling the
ruleset; if the plan lacks the required private-repository feature, migration
stops for an accountable platform decision rather than silently reducing the
control.

## 7. Repository contract

Every active or planned repository must contain the following controls.

### 7.1 `AGENTS.md`

`AGENTS.md` is the first local entry point for AI and developers. It must:

- point to `.waef/waef.lock.yml`;
- require the exact locked WAEF content to be read before work begins;
- list the selected profiles;
- preserve project-specific architecture, data, language, and protected-content
  rules;
- state that work stops if the locked WAEF version cannot be read or verified;
- state that project-local rules may strengthen but not silently weaken WAEF.

Existing detailed files, such as those in ratecalib and WFC, are preserved.
The WAEF bootstrap is added above their project knowledge; migration does not
replace that knowledge with a generic template.

### 7.2 `.waef/waef.lock.yml`

The tracked lock contains:

| Field | Meaning |
|---|---|
| `schema` | Lock schema version understood by the validator |
| `framework` | Constant framework identifier `WAEF` |
| `version` | Exact framework release, initially `4.0` |
| `repository` | Private source `weiandata/WAEF` |
| `tag` | Release tag corresponding to the exact version |
| `commit` | Full immutable commit SHA; authoritative if metadata disagrees |
| `profiles` | One or more applicable project profiles |
| `updated_by` | URL of the approved adoption or upgrade Pull Request |

CI verifies that the version, tag, commit, workflow reference, and fetched
framework metadata all agree. A mutable branch is never a valid lock target.

### 7.3 `.github/workflows/waef-compliance.yml`

The thin caller contains no independent policy logic. It invokes the private
WAEF reusable workflow at the immutable commit recorded in the lock, passes the
minimum required inputs, and grants read-only permissions except for narrowly
defined reporting operations.

### 7.4 Protected ownership

`CODEOWNERS` must require a WAEF maintainer or designated organization
governance owner to review changes to:

- `AGENTS.md`;
- `.waef/`;
- the WAEF compliance workflow;
- license and copyright declarations;
- release and deployment controls;
- CODEOWNERS and branch-governance configuration.

### 7.5 Local cache

`.waef/cache/` is gitignored. A local bootstrap operation authenticates to the
private WAEF repository, checks out the exact locked SHA, and verifies it before
AI or human work proceeds. A missing or mismatched cache causes a stop; it is
not replaced with the latest framework release.

### 7.6 Exceptions

Repositories have no exceptions by default. When an exception is necessary,
`.waef/exceptions.yml` records the affected rule, rationale, linked Issue or
ADR, responsible owner, approvals, creation date, and expiration date.

An exception requires approval from both the Project Owner and WAEF Maintainer.
Expired, incomplete, or overly broad exceptions fail compliance. An exception
does not authorize direct pushes, hidden test skips, secret exposure, or
publication of confidential information.

### 7.7 Human entry points and generated templates

`CONTRIBUTING.md` must point human contributors to the exact WAEF lock and
summarize the required Issue, plan, branch, Pull Request, validation, review,
and release sequence. GitHub cannot render Issue and Pull Request templates
from another private repository, so each consumer stores generated local
adapters for the WAEF Issue, Pull Request, validation report, design, ADR, and
release templates.

These adapters are derived interface files, not independent policy sources.
Their generated WAEF version is recorded and the validator checks their
required sections. An upgrade Pull Request regenerates them when a compatible
WAEF release changes the template contract; project-specific fields may be
added but required WAEF fields may not be removed.

## 8. Three enforcement layers

### 8.1 Machine enforcement

CI directly blocks:

- missing or malformed bootstrap and lock files;
- disagreement between WAEF version, tag, commit, and workflow reference;
- missing, incompatible, or unapproved profiles;
- incorrect copyright, licensing, and ownership metadata;
- non-compliant branch and commit conventions;
- Pull Requests without the required Issue relationship;
- missing validation or release evidence fields;
- failed static analysis, tests, builds, security checks, or project CI;
- deleted, renamed, skipped, or weakened required checks;
- expired or invalid exceptions.

### 8.2 Evidence enforcement

Pull Requests must contain or link to a requirement statement, scope,
acceptance criteria, implementation plan, affected files, risks, exact
validation commands, actual results, and a verdict. Release Pull Requests also
require versioning, changelog, rollback, human approval, and post-release
verification plans.

CI checks that structured evidence is present and internally consistent. It
does not claim to understand business intent merely because a field is filled.

### 8.3 Human enforcement

Human review remains mandatory for questions that cannot be reliably reduced
to static checks, including:

- whether the business requirement is unambiguous;
- whether an architecture change is justified and approved;
- whether a bug analysis found the actual root cause;
- whether security, compatibility, and maintainability are acceptable;
- whether an irreversible release or deployment should proceed.

Green CI is necessary but never sufficient for approval.

## 9. Authentication and supply-chain controls

Private reusable workflow access is limited to approved repositories in the
`weiandata` organization. Cross-repository reads and upgrade Pull Requests use
a GitHub App instead of a personal access token. The App receives the smallest
repository set and permissions required for each function; validation and
upgrade automation may use separate installations or permission boundaries.

Secrets are stored as organization or environment secrets with explicit
repository access. They are never printed, persisted in artifacts, made
available to untrusted fork code, or shared with local agent prompts. Actions
and reusable workflows are pinned to immutable commits. Authentication failure
causes compliance to fail closed.

Primary implementation references are:

- <https://docs.github.com/en/actions/how-tos/reuse-automations/share-with-your-organization>
- <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>
- <https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow>

## 10. Existing-repository rollout

Migration is staged so an incomplete control cannot block every repository at
once.

### Wave 0: framework and platform foundation

- release WAEF 4.0 with the deliverables in Section 5;
- add organization audit and upgrade automation to `.github`;
- create and scope the GitHub App;
- prepare repository contract generation in repository-template;
- configure rulesets in non-enforcing or pilot scope.

### Wave 1: representative pilots

Pilot four different responsibilities:

- WAEF, proving that the framework governs itself;
- repository-template, proving future-project generation;
- DCC, proving the R-package profile;
- website, proving the static-website profile.

Rulesets initially target only these repositories. Pilot failures are fixed in
WAEF, the template, or the repository adapter according to the location of the
root cause.

### Wave 2: remaining developed R packages

Migrate IRTC, WFC, mergecalib, and ratecalib. Preserve all valid project-specific
instructions and run each package's existing full validation suite.

### Wave 3: remaining infrastructure and website

Migrate `.github` and website-global-preview. Create LISTR through the new
future-project path rather than treating its current template state as a
finished product repository. Before LISTR receives business code, its language,
build system, owner, risk level, and WAEF profiles must be recorded.

### Wave 4: organization-wide enforcement

Enable the organization ruleset for all eleven repositories only after the
audit proves that every repository has a valid bootstrap, exact lock, selected
profiles, green compliance check, protected ownership, and working project CI.
The initial organization-wide audit is stored as the rollout baseline.

## 11. Future-project lifecycle

Every future repository is created from repository-template and follows this
sequence:

1. create the repository with GitHub's template mechanism;
2. run the project initialization workflow;
3. record purpose, audience, status, owner, language, repository type, risk
   level, publication intent, and applicable profiles;
4. generate `AGENTS.md`, the exact WAEF lock, thin compliance caller, ownership
   rules, license assets, Issue/PR/release templates, and project validation
   skeleton;
5. open the first governance Pull Request;
6. pass WAEF compliance and project bootstrap checks;
7. obtain required ownership review;
8. allow the organization ruleset to govern all later changes.

A project with no matching profile may be designed internally but may not be
published or deployed until the WAEF Maintainer adds a profile or approves a
documented exception.

LISTR is the first planned project used to validate this greenfield flow. Its
specific language profile is selected during initialization rather than
inferred from the current template files.

## 12. Version-upgrade lifecycle

When WAEF publishes a new release:

1. the release includes changelog, compatibility classification, migration
   instructions, and fresh framework validation evidence;
2. organization automation enumerates registered repositories;
3. a GitHub App opens one upgrade Pull Request per repository;
4. the Pull Request updates the exact version, tag, commit, and workflow
   reference and makes only required compatibility changes;
5. the Pull Request summarizes changed obligations and migration steps;
6. both the new WAEF validator and the repository's complete CI run;
7. a MINOR upgrade requires Project Owner approval;
8. a MAJOR upgrade requires Project Owner and WAEF Maintainer approval;
9. each repository merges independently.

Automation never merges an upgrade Pull Request. A failed or conflicted upgrade
remains open with evidence and a tracking Issue while that repository continues
using its previous exact WAEF version.

## 13. Daily audit

The `.github` repository runs a daily organization audit. The required targets
are:

| Metric | Target |
|---|---|
| Active repositories with AGENTS, lock, profiles, and WAEF CI | 100% |
| Locks with verifiable and consistent tag/commit metadata | 100% |
| Default branches with green `WAEF Compliance` | 100% |
| Expired exceptions | 0 |
| Unregistered repositories or repositories without an owner | 0 |
| Deleted, renamed, skipped, or weakened required checks | 0 |

The audit creates a repository Issue for each actionable failure and publishes
an organization summary in `.github`. An unchanged failure remains visible; it
is not silently closed or downgraded.

## 14. Failure handling and rollback

- Private-repository authentication failure: fail closed, repair GitHub App
  access, and rerun. Do not replace the App with a personal token.
- Central workflow or GitHub Actions failure: stop merging and record a
  platform incident. Do not remove the required check.
- Validator false positive: correct the validator or use the explicit,
  time-limited exception process. Do not convert the rule to a warning.
- Missing profile: block publication or deployment until a profile or approved
  exception exists.
- Upgrade conflict: the Project Owner resolves it and reruns full validation;
  automation does not force-push.
- Post-upgrade regression: open a normal rollback Pull Request that restores
  the previous exact WAEF SHA, retain the failed evidence, and track the root
  cause separately.
- Permission or business blocker: stop and report the blocker with the evidence
  already collected.

The system fails closed. There is no silent path that follows `latest`, skips
required checks, directly pushes the default branch, or hides failed evidence.

## 15. Validation strategy

### 15.1 Framework validation

- unit tests for lock parsing, schema validation, profile selection, evidence
  validation, and exception expiration;
- compliant and non-compliant fixture repositories for every profile;
- all existing BT-001 through BT-011 scenarios;
- new scenarios for human lifecycle obligations, WAEF version drift, expired
  exceptions, workflow bypass, missing upgrade approval, and unsafe release;
- link, required-section, changelog, migration-note, and release checks.

### 15.2 Platform integration validation

- a private sandbox repository proves reusable-workflow sharing and GitHub App
  authentication;
- destructive fixtures deliberately break the lock, workflow reference,
  profile, license, plan evidence, and tests and prove that merge is blocked;
- an upgrade simulation proves that the bot opens but does not merge Pull
  Requests;
- a rollback simulation proves that a repository can restore its previous
  exact SHA with complete audit history;
- pilot rulesets prove behavior before organization-wide activation;
- secret scanning and workflow-log inspection prove that credentials do not
  leak.

### 15.3 Repository validation

Each repository continues to run its own language-, product-, security-, and
release-specific validation. WAEF compliance complements those suites and does
not replace them.

## 16. Acceptance criteria

The rollout is complete only when:

1. WAEF 4.0 is released with expanded scope, migration documentation,
   validator, profiles, and passing framework tests.
2. The ten currently developed repositories pin WAEF 4.0 and pass compliance.
3. LISTR passes the new-project initialization path and records its language
   and project profiles before business development.
4. All eleven repositories are protected by the required WAEF status check and
   governance CODEOWNERS.
5. A sandbox repository created from repository-template becomes compliant
   without copying WAEF's normative documents.
6. Incorrect locks, licenses, missing plans, red project CI, expired
   exceptions, and weakened workflows demonstrably block merging.
7. WAEF release automation opens reviewable upgrade Pull Requests and never
   auto-merges them.
8. The daily audit detects new repositories, version drift, missing owners,
   missing checks, and expired exceptions.
9. A tested rollback restores the previous immutable WAEF commit while
   retaining complete audit evidence.
10. No validation or upgrade credential is exposed to untrusted code, logs, or
    local agent context.

## 17. Out of scope

- Implementing WAEF 4.0, validators, workflows, GitHub Apps, or rulesets in this
  design change.
- Publishing, deploying, or changing product behavior in any repository.
- Replacing repository-specific build, test, security, or release automation
  with generic WAEF checks.
- Automatically merging WAEF upgrades.
- Rewriting Git history to retrofit past compliance.
- Inferring LISTR's programming language before its project initialization
  decision.
