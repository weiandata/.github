# WAEF automation credential incidents

Treat any App private key in a log, artifact, cache, local prompt, copied file,
unexpected process, or unauthorized workflow as compromised. Do not wait for
proof of misuse.

## Immediate containment

The Organization Owner or incident commander must:

1. suspend the affected GitHub App installation or revoke the exposed private
   key immediately;
2. disable the WAEF audit/upgrade workflows if they could mint further tokens;
3. delete or replace every affected repository secret without reading or
   printing its value; because the read App key is distributed to registered
   repositories, one exposed copy requires rotation of every copy;
4. preserve workflow URLs, timestamps, actor identities, App audit events, and
   affected repository names in a private incident record;
5. contact `contact@weiandata.com` and `@makunxiang-weiandata`; do not use a
   public Issue.

Installation tokens expire after at most one hour, but key revocation is still
immediate because an App private key can mint new tokens while valid.

## Investigation

Review GitHub organization audit logs, App installation changes, Actions runs,
unexpected refs, Pull Requests, Issues, workflow changes, and secret visibility
changes. Compare every affected default branch with the last green WAEF audit.
Do not clone confidential repositories to an unmanaged incident workspace.

Classify whether exposure affected the read App, the automation App, or both:

- read App exposure requires assessment of unauthorized private-source access;
- automation App exposure additionally requires inspection for created Git
  objects, modified refs, workflow edits, Issues, and Pull Requests;
- any default-branch or release mutation triggers the company security and
  release rollback procedures.

## Recovery

Create a replacement key only after the exposure path is closed. Replace every
authorized repository secret, confirm names and update timestamps without
printing values, restore the App installation, and run:

1. organization automation unit tests;
2. the independent read-only audit;
3. one approved sandbox compliance run; and
4. one sandbox upgrade that remains unmerged.

Re-enable production workflows only when evidence is reviewed by the
Organization Owner and WAEF Maintainer. Document root cause, scope, containment,
key identifiers and revocation times, repository verification, corrective
actions, and a follow-up owner. Never include key material in the record.
