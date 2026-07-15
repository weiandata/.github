# Reviewed WAEF upgrades

The manual `WAEF Reviewed Upgrade Pull Requests` workflow is dispatched only
after a WAEF release has an immutable tag, migration instructions, changelog,
and validation evidence. The dispatcher must provide concrete changed-MUST-rule
and migration-step summaries; blank summaries fail before authentication.
Before any repository branch is written, the workflow runs the complete
organization-automation test suite and verifies the private tag with
`git ls-remote`, preferring the peeled commit for an annotated tag.

For each registered repository the automation creates or reuses
`automation/waef-MAJOR.MINOR`, then changes only:

- the exact lock version, tag, commit, and `updated_by` Pull Request URL;
- the reusable workflow reference and `waef_commit` input; and
- generated-version markers inside WAEF-owned adapter blocks.

Text outside `<!-- WAEF:START -->` and `<!-- WAEF:END -->` is project-owned and
is preserved byte-for-byte. Missing, duplicated, or reversed markers stop the
upgrade. Changed template obligations are intentionally left for the Pull
Request author and reviewers to implement from the migration guide; WAEF and
project CI must remain red until those semantic changes are complete.

The rendered thin caller runs on both `pull_request` and `push`. Pull Requests
provide the merge-gating result; a successful push run at the exact
default-branch HEAD provides independently auditable post-merge evidence.

The lock's `updated_by` field must contain the URL of the Pull Request that is
being created. GitHub assigns that URL only after a branch exists, so a new
upgrade is recorded in two ordinary, non-forced commits:

1. create the upgrade branch and draft Pull Request while retaining the prior
   valid `updated_by` value; and
2. add the newly assigned Pull Request URL to the lock.

The final Pull Request has one logical purpose: adopt one exact WAEF release.
Its body contains the supplied changed-rule and migration-step summaries rather
than only linking reviewers to another document.
Existing open upgrade Pull Requests are updated rather than duplicated. The
automation never calls a merge endpoint, enables merge automation, pushes the
default branch, or force-updates a ref.

The short-lived upgrade token is restricted to the eleven reviewed
repositories. It needs Metadata read, Contents write, Pull Requests write, and
Workflows write because the governed caller lives under `.github/workflows/`.
GitHub App creation, installation, and secret distribution remain a separate
Organization Owner approval checkpoint.

All dispatch inputs enter shell commands through quoted environment variables;
GitHub expressions are never interpolated directly into shell source.
