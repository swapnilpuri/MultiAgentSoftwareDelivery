# M3 requirements — Architect Agent & Solution Architecture Studio

Status: authorized specification; implementation and verification complete, **READY_FOR_HUMAN_APPROVAL** (see [M3_COMPLETION_REPORT.md](M3_COMPLETION_REPORT.md)). M2 baseline VERIFIED_ACCEPTED on 2026-11-24 ([M3_BASELINE_VERIFICATION.md](M3_BASELINE_VERIFICATION.md)).

## Authoritative source

The complete authorized requirements are the versioned prompt package. It is not duplicated here, to avoid divergent copies:

| Part | File | Sections |
|---|---|---|
| Execution model | [M3_PROMPT/00_START_HERE.md](M3_PROMPT/00_START_HERE.md) | Phases M3-A/B/C, efficiency, GitHub rules |
| Architecture and model | [M3_PROMPT/01_ARCHITECTURE_AND_MODEL.md](M3_PROMPT/01_ARCHITECTURE_AND_MODEL.md) | §1–8: baseline gate, mission, principles, ownership, package sections A–J, canonical model, C4 |
| Agent, UI, governance | [M3_PROMPT/02_AGENT_UI_AND_GOVERNANCE.md](M3_PROMPT/02_AGENT_UI_AND_GOVERNANCE.md) | §9–16: LangGraph workflow, model invocation, traceability/drift, Angular Studio, approval, API, persistence, security |
| Delivery and acceptance | [M3_PROMPT/03_DELIVERY_AND_ACCEPTANCE.md](M3_PROMPT/03_DELIVERY_AND_ACCEPTANCE.md) | §17–25: slices, testing, 44 acceptance criteria, PR/review rules, deliverables, handoff |

SHA-256 values for these files are recorded in M3_BASELINE_VERIFICATION.md.

## Scope summary

In scope: transform an approved M2 PRD revision into a structured, versioned, human-approved solution architecture package. The package covers the overview, alternatives, technology stack, service boundaries, API and event proposals, data, deployment, security, proposed ADRs, risks, C4 context/container/component diagrams, requirement traceability, drift detection, revision comparison, exports, and an approved-baseline API for future agents.

Out of scope (explicitly prohibited for M3): generating or deploying target-application code; modifying the target application's or any production infrastructure (development-platform wiring in masd-infrastructure, such as Compose and verification scripts, is in scope); merging PRs; agent self-approval; altering approved PRDs; automatically triggering development agents; C4 level-4 code diagrams; production identity; M4 planning.

## Interpretation decisions (within the approved scope)

These resolve points the prompt leaves to "established conventions". Each is recorded in M3_DESIGN.md or an ADR:

1. **Ownership.** Project Service owns architecture sessions, immutable revisions, approvals, operations and history (mirrors M2 / ADR 0005). Agent Service runs a stateless Architect graph via the Gateway. See ADR 0006.
2. **Durable workflow state.** Project Service persists the authoritative checkpoint per operation. LangGraph executes nodes in-process, and its checkpoint does not replace domain persistence (prompt §9; M2 precedent).
3. **Diagrams.** The canonical model holds a structured C4 graph. PlantUML/C4-PlantUML and Mermaid sources are generated deterministically from it. The Studio renders a safe native SVG from the same graph; there is no server-side PlantUML execution. See ADR 0007.
4. **Supersession policy.** An architecture revision may be approved only against the requirements session's *latest* approved PRD revision with matching hash. A newer approved PRD makes the session out of date, and approval requires an explicit rebase revision.
5. **Contracts.** Additive release 0.4.0 (architecture package schema, Project Service and Agent Service OpenAPI, architecture SSE). 0.1.0–0.3.0 stay unchanged.
