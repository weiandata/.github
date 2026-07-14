# Security Policy

Do not report vulnerabilities, credentials, personal information, or client data in a public issue.

Use GitHub private vulnerability reporting when available or contact `contact@weiandata.com` with the minimum information required to begin a private response. Do not attach real client data.

The company-wide control baseline is defined by the [Security Policy](handbook/chapters/21-security-policy.md) and [Client Data Policy](handbook/chapters/22-client-data-policy.md).

## WAEF automation credentials

WAEF uses separate read-only and repository-limited automation GitHub Apps.
Their approved scopes, secret distribution, annual rotation, and verification
procedure are documented in
[`operations/waef/GITHUB_APP.md`](operations/waef/GITHUB_APP.md). Suspected App
key or installation-token disclosure follows
[`operations/waef/INCIDENTS.md`](operations/waef/INCIDENTS.md) immediately.

Never paste a WAEF App ID/private-key pair, installation token, or secret value
into an Issue, Pull Request, log, artifact, local agent prompt, or support
message. App configuration and secret changes require an Organization Owner.
