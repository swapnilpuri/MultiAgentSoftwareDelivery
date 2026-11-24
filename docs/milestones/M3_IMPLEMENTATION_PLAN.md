# M3 implementation plan

Branch in every affected repository: `feature/m3-architect-agent-solution-studio`, from the current `main`. One reviewable PR per repository per phase. Contracts are published before consumers rely on them. No automatic merges.

| Phase | Slice | Repository | Deliverable | Verification |
|---|---|---|---|---|
| M3-A | 0 | MultiAgentSoftwareDelivery | Requirements, design, plan, acceptance tracker, handoff, ADR 0006/0007, PlantUML | Central gate |
| M3-A | 0 | masd-contracts | 0.4.0 architecture package JSON Schema + semantic validator; Project Service and Agent Service OpenAPI 0.4.0; architecture SSE schema; positive/negative fixtures | Contracts gate, schema validation |
| M3-A | 1 | masd-project-service | Pydantic package model, deterministic validator, PlantUML/Mermaid/Markdown exporters, additive migration, sessions/revisions/approvals/operations/history, commands, drift, compare, traceability, baseline APIs | Unit tests + real PostgreSQL suite |
| M3-A | 2–3 | masd-agent-service | Architect LangGraph (validate → analyze → clarify → generate → validate → repair → deterministic checks), deterministic fixture, `/api/v1/architect/run` | Graph tests incl. invalid JSON, repair, Gateway failure, clarification, duplicate, cancel, no tools |
| M3-A | 2 | masd-llm-gateway | Expected: no change (catalog/profiles already sufficient); verified by contract tests | Gateway gate |
| M3-B | 4 | masd-web | Architecture Studio route, dashboard, conversation, workspace, C4 SVG explorer, boundary/technology/ADR explorers, traceability, comparison | Angular unit tests, build |
| M3-C | 5 | masd-web, masd-project-service | Review/approval UI and approval-history views; authorization tests | Unit + PostgreSQL |
| M3-C | 6 | masd-infrastructure, masd-web | Compose M3 wiring; Chromium end-to-end (approved PRD → approved architecture), restart, drift, stale, unauthorized | Real browser + restart verifier |
| M3-C | 7 | all | PRs, Sourcery remediation, CI, completion report, handoff | Final reconciliation |

Checkpoints are recorded in [M3_HANDOFF.md](M3_HANDOFF.md) after each slice.
