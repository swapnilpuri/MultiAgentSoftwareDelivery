# M3 — Claude Code Execution Instructions

You are implementing M3 — Architect Agent & Solution Architecture Studio using Claude Code in VS Code.

The complete M3 implementation prompt follows this instruction.

## Operating model

- ChatGPT UI owns architecture and milestone definition.
- Claude Code owns implementation, testing, debugging and PR preparation.
- Humans own required approvals and PR merges.
- Git repositories and versioned documentation are the source of truth.

Read existing AGENTS.md and AIEngineeringStandards. Create a concise CLAUDE.md referencing those standards if one does not exist.

Do not replace the existing architecture or create duplicate governance rules.

## Execution strategy

Implement M3 in three phases:

**M3-A — Backend and Architect Agent**

Implement canonical architecture models, contracts, persistence, LangGraph execution, Gateway integration and backend tests.

**M3-B — Architecture Studio UI**

Implement Angular screens, C4 visualization, architecture comparisons, ADRs and traceability.

**M3-C — Approval and acceptance**

Implement approval workflows, full integration, security checks, end-to-end tests, Sourcery remediation and delivery evidence.

## Efficiency requirements

- Read the approved M2 baseline once and reuse verified evidence.
- Do not repeat completed investigations.
- Prefer implementation over prolonged deliberation.
- Use existing abstractions and established patterns.
- Avoid unrelated refactoring.
- Run targeted tests during development.
- Run full regression at required integration checkpoints.
- Process Sourcery findings in bounded batches.
- Fix mandatory actionable findings without suppressing security alerts.
- If repeated reviewer cycles do not converge, document outstanding findings and stop at the required governance boundary.
- Maintain a concise checkpoint file so another session can resume safely.
- Continue through ordinary tasks without requesting repeated approvals.

## GitHub rules

- Use independent feature branches for each affected repository.
- Keep independent CI/CD pipelines intact.
- Create reviewable PRs.
- Address all actionable comments.
- Resolve required conversations appropriately.
- Verify final-head CI and review status.
- Never merge automatically.

## Security

Use normal workspace permissions. Do not bypass permission controls to improve speed.

Request human authorization for sensitive operations.

## Final objective

Implement and verify M3 against its acceptance criteria, produce consolidated handoff evidence, and prepare PRs for human approval.

Do not begin M4.

Start by reading the approved M2 handoff and validating the M3 prerequisites, then execute M3-A.



# M3 — Execution Efficiency and Baseline Instructions

We are starting M3 — Architect Agent & Solution Architecture Studio.

M2 has been completed and reported accepted.

Before implementation, perform a focused verification that the approved M2 implementation exists on `main`, its required acceptance evidence is available, and its contracts are compatible with M3.

Do not repeat the entire historical M2 investigation unless a material inconsistency is discovered.

Follow the existing AIEngineeringStandards and Codex efficiency guidelines.

**Execution requirements:**
- Use Medium reasoning effort for routine implementation when available.
- Reuse approved architectural decisions.
- Avoid prolonged analysis and repeated planning.
- Implement in small, independently testable slices.
- Run focused tests during development and full regression at integration boundaries.
- Avoid unrelated refactoring.
- Process Sourcery review findings in controlled batches.
- Fix all actionable review comments and resolve required conversations.
- Do not bypass mandatory security, review, CI or human approval gates.
- Maintain concise checkpoints and persistent handoff documentation.
- Continue autonomously unless a genuine human authorization is required.
- Never merge PRs automatically.

If the M2 baseline is verified, proceed immediately with the complete M3 implementation instructions below.



# MultiAgentSoftwareDelivery — Milestone M3
## Architect Agent & Solution Architecture Studio
### Complete Codex Implementation Prompt

