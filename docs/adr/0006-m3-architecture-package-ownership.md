# ADR 0006: M3 architecture package ownership and persistence

Status: accepted for M3 implementation (Slice 0); human approval via the M3 PR.

## Context

M3 must persist architecture sessions, generation attempts, immutable revisions, approvals and audit history that survive restarts. Future Planning, Development, QA and DevOps agents must be able to consume an approved architecture without scraping Markdown. ADR 0005 already established, and M2 accepted, a pattern: Project Service owns durable artifacts and approvals; Agent Service is stateless, bounded and has no database.

## Decision

- Project Service owns all M3 state in new additive PostgreSQL tables (`architecture_sessions`, `architecture_revisions`, `architecture_approvals`, `architecture_operations`, `architecture_history`). Revisions and approvals are append-only, enforced by triggers and ORM guards. No new microservice and no shared database.
- The canonical representation is a typed JSON **architecture package** (schema 0.4.0, published in masd-contracts). Exports (Markdown, JSON, PlantUML, Mermaid) are generated from it, one-way.
- Each architecture session is bound to one requirements session. Each revision copies the source PRD revision ID, content hash and approval ID. Approval requires that source to be the *latest* approved PRD revision with a matching hash. Otherwise an explicit `rebase` revision is required (supersession policy).
- The Agent Service runs a stateless LangGraph Architect graph. Project Service persists the authoritative checkpoint per operation, and the LangGraph checkpoint is not domain state. Interrupted operations fail at startup and require an explicit retry (M2 behaviour).
- Human approval is a Project Service domain operation bound to the exact revision, hash, source PRD and policy version. Model output can never set a status.

## Alternatives considered

- **Generalize the M2 requirements tables into a shared artifact store.** Rejected for M3: it would migrate accepted M2 tables and risk regressions in the approved baseline. Shared helpers are reused instead, and a generic artifact store can be revisited when a third artifact type appears.
- **New Architecture Service.** Rejected: no new domain boundary, since Project Service already owns project artifacts and authorization. A new service would add a distributed transaction to approval.
- **LangGraph checkpointer as durable state.** Rejected: it would duplicate canonical state in a second store owned by the Agent, contradicting ADR 0005.

## Consequences

The Project Service schema grows with five additive tables, plus a migration test on real PostgreSQL. The architecture package becomes a stable contract for future agents through `GET …/architecture/approved`. Rollback retains the tables (no destructive downgrade).
