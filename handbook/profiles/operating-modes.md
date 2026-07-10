# Operating Modes Profile

| Field | Value |
|---|---|
| Version | 1.1.0 |
| Status | Approved |
| Owner | WeianData Engineering |
| Effective date | 2026-07-10 |

## Purpose

This profile makes the handbook practical for a founder-led company by selecting evidence and review depth according to risk. It does not create new standards; every requirement remains owned by the linked chapter.

## Mode selection

Use the highest applicable mode.

| Mode | Review class | Typical work | External reliance |
|---|---|---|---|
| Lightweight | R1 | Typo, documentation correction, safe internal maintenance | No material scientific, security, or client consequence |
| Standard | R2 | Production code, ordinary tooling, repository workflow, non-sensitive automation | Permitted after normal evidence and accountable approval |
| Controlled | R3 or R4 | Statistical acceptance, client deliverable, restricted-data boundary, security logic, constitutional change | Requires the applicable domain gates and human approval |

Under the [review standard](../SPECIFICATION/handbook-review-standard.md), work moves to a higher mode when scope introduces scientific interpretation, restricted client data, security boundaries, incompatible behavior, irreversible action, or material external reliance.

## Evidence matrix

| Evidence | Lightweight | Standard | Controlled |
|---|---|---|---|
| Issue or brief | Compact outcome, risk, evidence, owner | Full issue fields | Full issue plus decision and review scope |
| Branch and pull request | Focused pull request or approved safe automation | Required reviewable branch and pull request | Required reviewable branch and pull request |
| Verification | Relevant deterministic checks | Full repository checks | Full checks plus adversarial and boundary evidence |
| Statistical validation | Not applicable | When output has scientific meaning | Required for statistical reliance |
| ADR | Only for a lasting decision | When an ADR trigger applies | Required for material architecture, data, or inference decisions |
| Independent human | Not required | Not required unless another rule requires it | Required before client or public reliance on the affected high-risk conclusion |
| Release evidence | Compact change evidence | Release-process evidence when distributed | Full release, recovery, provenance, and acceptance evidence |
| Knowledge capture | Only durable changes | Required for reusable behavior | Required, including limitations and review triggers |

The owning standards are [Engineering Workflow](../chapters/03-engineering-workflow.md), [Review Standard](../SPECIFICATION/handbook-review-standard.md), [Pull Request Standard](../chapters/30-pull-request-standard.md), and [Release Process](../chapters/10-release-process.md).

## Founder-led execution

In a one-person operation:

- the review standard permits the founder to hold author, reviewer, security, statistical, and accountable-owner roles for Lightweight and Standard work;
- the AI policy permits AI agents to provide adversarial review and deterministic evidence but not accountable approval;
- Controlled work can proceed internally without a second person while it remains reversible and creates no external reliance;
- the review standard requires a qualified client reviewer or contracted specialist to review the relevant high-risk scope before client or public reliance;
- the review record identifies what the second human reviewed and what remained outside the review.

## Stop and escalation conditions

Stop the current mode and reclassify when:

- real client data becomes necessary;
- an implementation changes statistical interpretation or a scoring scale;
- a security or trust boundary changes;
- an irreversible or externally visible action is required;
- acceptance evidence cannot be produced;
- the qualified reviewer cannot review the high-risk scope before external reliance.

## Examples

### Lightweight

Correct a broken handbook link. Record R1, run the validator, review the diff, and merge through the protected path.

### Standard

Add a schema parser using synthetic fixtures. Record R2, implement tests, review AI contributions, document the interface, and release when distributed.

### Controlled

Change an IRT scoring default for a client deliverable. Record R3, create an ADR, run statistical validation and sensitivity analysis, obtain a qualified second-human review, and preserve client acceptance evidence.

## Checklist

- [ ] The selected mode matches the highest risk and intended reliance.
- [ ] Only evidence required by the selected mode and owning rules is produced.
- [ ] Mode escalation conditions were monitored.
- [ ] Controlled external reliance has a qualified second-human review.
- [ ] AI participation and accountable approval are recorded.

## References

- [Handbook Review Standard](../SPECIFICATION/handbook-review-standard.md)
- [AI Development Policy](../chapters/16-ai-development-policy.md)
