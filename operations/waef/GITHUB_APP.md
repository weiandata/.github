# WAEF GitHub App operations

Status: **approved for repository-level Actions secrets**. The organization
plan does not make organization Actions secrets available to private
repositories, so the repository-level distribution below is the authoritative
interim configuration. Moving back to organization secrets requires a reviewed
platform change.

## Permission boundary

Two private, organization-owned GitHub Apps prevent repository-write
permissions from following the read-only audit into future repositories.

| App | Installation scope | Repository permissions | Repository secret names |
|---|---|---|---|
| `WeianData WAEF Read` | All repositories, including future repositories | Metadata read, Contents read, Checks read, Actions read | `WAEF_APP_ID`, `WAEF_APP_PRIVATE_KEY` |
| `WeianData WAEF Automation` | Only the eleven names in `repositories.json` | Metadata read, Contents write, Issues write, Pull requests write, Workflows write | `WAEF_AUTOMATION_APP_ID`, `WAEF_AUTOMATION_APP_PRIVATE_KEY` |

Both Apps are owned by `weiandata`, are not public or Marketplace Apps, have no
OAuth callback, and have webhooks disabled. They subscribe to no events.

The read App needs all-repository installation scope because a selected-
repository installation cannot discover a newly created private repository.
It has no write permission. The automation App has write permissions only on
reviewed repositories because upgrades create Git objects, refs, workflow-file
changes, and Pull Requests. It cannot be installed on a new repository until
that repository is reviewed and added to the inventory.

## Per-workflow token scopes

Installation scope is an upper bound. Each workflow mints a short-lived token
with a narrower repository and permission set:

| Function | App | Token repository scope | Token permissions |
|---|---|---|---|
| Consumer WAEF validation | Read | `WAEF` only | Metadata read, Contents read |
| Organization discovery and audit | Read | All repositories visible to the installation | Metadata read, Contents read, Checks read, Actions read |
| Audit Issue reporting | Automation | Eleven registered repositories | Metadata read, Issues write |
| Reviewed upgrades | Automation | Eleven registered repositories | Metadata read, Contents write, Pull requests write, Workflows write |

No token receives Administration permission. No token is persisted as an
artifact, passed to untrusted code, or printed. Default-branch rules, required
checks, and CODEOWNERS remain mandatory because Contents write permission is
capable of creating Git objects and updating non-protected refs.

The source-bound audit added during security review requires Actions read so a
green check can be tied to `.github/workflows/waef-compliance.yml`, rather than
accepted by name alone. On 2026-07-15, the Organization Owner approved the
`Actions: read` update for the live Read App and accepted it on the organization
installation. Production audit dispatch remains blocked until the private
sandbox validation is recorded in Draft Pull Request #1.

## Secret distribution

Create the four secret names exactly as listed in the table. Repository secrets
are an explicit plan-compatible fallback, not permission to broaden either App:

- create the read App pair in each of the eleven registered repositories;
- add the read App pair to a future repository only through its reviewed
  initialization;
- create the automation App pair only in `.github`;
- repository workflows refer to secret names, never values;
- local development, AI prompts, Issues, logs, caches, and artifacts never
  receive a private key.

Verify only names and update timestamps, one repository at a time, with:

```bash
gh secret list --repo weiandata/REPOSITORY
```

Never use a command or API response that prints a secret value.

### Temporary candidate-bridge boundary

The approved pre-release bridge adds exactly one temporary repository,
`weiandata/waef-compliance-sandbox`, without adding it to the production
inventory or scheduled audit. During that validation window only:

- keep the Read App's existing all-repository, read-only installation and
  generate one additional Read App key for the sandbox secret pair;
- add only `waef-compliance-sandbox` to the Automation App installation and
  generate one additional Automation App key for the sandbox secret pair;
- store the two App IDs and two additional private keys only as the four named
  encrypted repository secrets in the sandbox;
- never reuse the temporary private-key files in another repository, terminal
  command argument, report, log, artifact, Issue, Pull Request, or AI prompt;
- delete each downloaded PEM file immediately after its corresponding secret is
  set, and verify only secret names and update timestamps; and
- after the approved evidence is retained, delete the four sandbox secrets,
  revoke both additional App keys, remove the sandbox from the Automation App
  installation, and verify that the Read App remains read-only.

This exception does not authorize a production inventory change, a production
audit dispatch, a merge, a release tag, ruleset activation, or sandbox deletion.

## Creation checklist

An Organization Owner performs these steps in GitHub settings after approval:

1. create both private Apps with the exact names and permissions above;
2. disable webhooks and request no account or organization permissions;
3. install the read App on all repositories and the automation App on exactly
   the eleven inventory repositories;
4. generate one private key for each App;
5. create the read App pair as repository secrets in every registered
   repository and the automation App pair only in `.github`;
6. verify secret names only in all eleven repositories, then delete every
   downloaded private-key file from the operator workstation after secure
   secret entry;
7. run a read-only audit and inspect logs for credential material;
8. record the approval, App IDs, installation scopes, secret visibility, and
   verification URLs in the private rollout Issue without recording keys.

## Rotation and ownership

`@makunxiang-weiandata` is the initial Organization Owner and rotation owner;
`@weiandata/organization-governance` is the accountable governance role once
that team exists. Rotate both App private keys at least annually and whenever
an owner, runner, or secret boundary changes materially.

Rotation is overlap-safe: create a new App key, replace the corresponding
repository secret in every authorized repository, verify all secret names and
timestamps, run the read-only audit and one sandbox validation, then revoke the
old key. The automation key is replaced only in `.github`; the read key is
replaced in every registered repository. Record dates and evidence, not key
material. A suspected disclosure bypasses the overlap procedure and follows
`INCIDENTS.md` immediately.
