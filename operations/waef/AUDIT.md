# WAEF organization audit

The daily audit is an independent control owned by `weiandata/.github`. It
enumerates organization repositories from GitHub and compares them with the
reviewed `repositories.json` inventory. A repository cannot suppress this
audit by deleting, renaming, skipping, or weakening its local WAEF workflow.

For every registered, non-archived repository the audit reads the default
branch and verifies:

- the WAEF bootstrap in `AGENTS.md`;
- the exact `.waef/waef.lock.yml` and selected profiles;
- `.waef/project.yml`, including the reviewed accountable owner;
- the byte-exact immutable private reusable-workflow caller, triggered for both
  Pull Requests and pushes;
- governance coverage in `CODEOWNERS`;
- the WAEF tag-to-commit provenance;
- exactly one successful default-branch `WAEF Compliance` check and a
  successful `push` run bound to
  `.github/workflows/waef-compliance.yml@DEFAULT_BRANCH` at the exact current
  default-branch HEAD; and
- exception expiration dates.

The workflow mints two short-lived tokens. The organization-wide audit token is
read-only so it can discover an unregistered private repository and read the
Actions workflow-run source; a second token has Issues write access but is
narrowed to the eleven reviewed repositories. Enabling Actions read on the live
Read App remains a separate Organization Owner approval described in
`GITHUB_APP.md`.

Findings have a stable fingerprint derived from repository, rule ID, and path.
The first observation creates a labelled Issue; later observations update that
same Issue. The audit does not silently register new repositories, close an
unchanged finding, downgrade a failure to a warning, or expose credentials in
an uploaded artifact.

Run a read-only local audit with an installation token:

```bash
GH_TOKEN=... python3 -m operations.waef.audit --no-sync-issues
```

Omit `--no-sync-issues` only when `WAEF_ISSUE_TOKEN` contains a separately
scoped Issues-write installation token and the operator intends to create or
update audit Issues. Exit status is `0` for a green audit and `1` when any
finding exists.
