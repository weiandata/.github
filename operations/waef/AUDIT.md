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
- the immutable private reusable-workflow caller;
- governance coverage in `CODEOWNERS`;
- the WAEF tag-to-commit provenance;
- the latest default-branch `WAEF Compliance` conclusion; and
- exception expiration dates.

The workflow mints two short-lived tokens. The organization-wide audit token is
read-only so it can discover an unregistered private repository; a second token
has Issues write access but is narrowed to the eleven reviewed repositories.
The GitHub App and its installation are not created by this change and require
the separate Organization Owner approval described in the operations plan.

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
