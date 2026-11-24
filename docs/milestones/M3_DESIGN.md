# M3 design — Architect Agent & Solution Architecture Studio

Status: implemented as designed in M3-A/B/C, with the corrections noted in the API table (implementation evidence in M3_COMPLETION_REPORT.md). Authorized by the M3 prompt ([M3_REQUIREMENTS.md](M3_REQUIREMENTS.md)); baseline VERIFIED_ACCEPTED. Decisions: [ADR 0006](../adr/0006-m3-architecture-package-ownership.md), [ADR 0007](../adr/0007-m3-c4-diagram-rendering.md). Diagrams: [docs/architecture/m3/](../architecture/m3/).

## 1. Service responsibilities (no new microservice)

| Service | M3 responsibility | Explicitly not |
|---|---|---|
| masd-web | Architecture Studio route in the existing shell: dashboard, Architect conversation, section workspace, C4 explorer, boundary, technology and ADR explorers, traceability, comparison, review/approval | Business rules, persistence, approval authority |
| masd-project-service | Architecture sessions, immutable revisions, approvals, operations/idempotency, history, traceability and drift queries, exports, approved-baseline API, project authorization | Model invocation |
| masd-agent-service | Architect LangGraph: source validation, analysis, clarification questions, generation, bounded repair, deterministic validation, AI quality suggestions | Database access, approval, tools, code generation, deployment |
| masd-llm-gateway | Unchanged model routing, profiles, usage reporting | Architect logic |
| masd-contracts | 0.4.0 architecture package schema, Project/Agent OpenAPI, architecture SSE schema, semantic validator | Runtime |
| masd-infrastructure | Compose wiring for the M3 profile, restart/acceptance helpers | Production deployment |

Data flow is identical to M2. The browser calls only Project Service. Project Service authorizes, claims a durable operation, sends a bounded snapshot to the Agent, validates the returned proposal again, and commits. The Agent never calls back into Project Service.

## 2. Canonical architecture package (schema 0.4.0)

Typed JSON, validated by Pydantic in Project Service and Agent Service, and by the published JSON Schema plus a semantic validator in masd-contracts. Markdown, PlantUML, Mermaid and JSON exports are rendered from it; it is never parsed back from Markdown.

| Section | Content (stable IDs) |
|---|---|
| `source` | `requirements_session_id`, `prd_revision_id`, `prd_content_hash`, `approval_id`, `approved_at` |
| `overview` | description, objectives, business context, principles, quality attributes `QA-n`, assumptions `AS-n`, constraints `CN-n`, major decisions (ADR refs), unresolved decisions `UQ-n` |
| `alternatives` | `ALT-n`: benefits, drawbacks, complexity, operational, security, cost factors, constraints, decision (selected/rejected/deferred), rationale |
| `technology` | `TECH-n` by category (frontend … ai_ml): choice, rationale, alternatives, maturity, risks, operational trade-offs, licensing/support assumptions |
| `elements` | `EL-n` C4 elements: kind (person, software_system, external_system, container, database, queue, component), parent, technology, responsibility, bounded context |
| `relationships` | `REL-n`: source, target, description, protocol, sync/async |
| `services` | `SVC-n` boundary: element, bounded context, responsibilities, owned entities, API/event refs, dependencies |
| `apis` / `events` | `API-n` (method, path, purpose, OpenAPI-compatible draft schemas, auth, versioning, errors, idempotency, pagination); `EVT-n` (producer, consumers, payload, consistency, retry). Always labelled *proposed application contract*. |
| `data` | `ENT-n` entities (owner, attributes, aggregate, retention), `DREL-n` relationships, transaction boundaries, consistency |
| `deployment` | environments, nodes, network boundaries, scaling, availability, DR, observability, secrets, CI/CD. Marked as proposals unless required |
| `security` | trust boundaries `TB-n`, controls `SEC-n`, data classification, encryption, threats `THR-n` → controls, assumptions |
| `views` | `VIEW-n` C4 views: level (context, container, component), focus element, included elements and relationships |
| `adrs` | `ADR-n`: title, status (proposed until approved), context, decision, alternatives, consequences, version, source (ai/human), review metadata |
| `risks` | `RSK-n`: category, likelihood, impact, mitigation, anti-pattern flag |
| `traceability` | per requirement: disposition (covered / not_applicable / deferred), rationale, element IDs of any type |
| `findings` | `AF-n`: rule, severity, source (deterministic / ai), element/requirement refs, status (open/accepted/rejected) |

Every element type carries `requirement_ids` and/or `rationale`. IDs are preserved across revisions: revise and rebase start from the prior document, and the deterministic validator rejects unexplained ID churn of retained elements.

## 3. Deterministic validation (Project Service and Agent; contracts validator)

Run on every save and generation, and kept separate from model-generated suggestions (`source: deterministic` vs `ai`):

- Duplicate or dangling IDs, and broken view/diagram references.
- Missing coverage: an approved requirement with neither element refs nor an explicit disposition.
- Orphaned elements: no requirement, constraint, assumption or rationale.
- Containers without an owning service; data entities without an owner, or owned by more than one service.
- External systems with no relationship; APIs whose owner is not a container/service; events without a producer.
- Inconsistent communication (async relationship without an event, or an event without an async relationship).
- Missing security control for a trust boundary; threats without mitigations.
- Material decisions (selected alternatives, technology choices) without an ADR; unresolved questions listed.
- Contradictions: the same category with two selected technologies; an alternative both selected and rejected.

## 4. Persistence (Project Service, additive Alembic migration)

New tables, following ADR 0005 patterns, with no change to M1/M2 tables:

- `architecture_sessions`: project, requirements session, source PRD revision/hash/approval, model, state, version, checkpoint (questions, messages, execution), current/submitted/approved revision pointers, active operation.
- `architecture_revisions`: append-only. Number, parent, schema version, canonical content, SHA-256 hash, copied source references, creation source (human/agent), generation metadata (provider, model, prompt version, attempts, usage as returned), author.
- `architecture_approvals`: append-only. Revision, content hash, source PRD ID/revision/hash, decision, approver, comment, scope, policy version, time.
- `architecture_operations` (idempotency key + request hash, status, result) and `architecture_messages` (history).

PostgreSQL triggers plus ORM guards enforce immutability. Uniqueness: one session per (project, requirements session) and revision numbers per session. Rollback leaves the additive tables in place (no destructive downgrade).

## 5. Lifecycle and approval

States: `CLARIFICATION_REQUIRED`, `DRAFT`, `UNDER_REVIEW`, `CHANGES_REQUESTED`, `REJECTED`, `APPROVED`. `GENERATING` is represented by an active operation, as in M2. Server-side transitions:

```text
start → CLARIFICATION_REQUIRED (questions) | DRAFT (no material questions)
DRAFT --submit(revision, hash)--> UNDER_REVIEW
UNDER_REVIEW --decide--> APPROVED | CHANGES_REQUESTED | REJECTED
CHANGES_REQUESTED / REJECTED --revise|save|rebase--> DRAFT (new revision required)
APPROVED --revise|rebase--> DRAFT (approved baseline retained)
```

Approval requires all of: human principal with approval permission (service credentials refused); the submitted revision equal to the current revision; matching expected hash and version; the source approval still valid with matching hash; and the source being the *latest* approved PRD revision. Any earlier negative decision on the same content hash blocks resubmission (M2 regression). Approval writes the record and updates the pointer in one transaction.

## 6. Drift and supersession

`GET …/drift` compares the session's source with the requirements session's current approved baseline. It returns `out_of_date`, the newer approved revision and hash, and an impact list (requirement IDs added/removed/changed, and the architecture elements referencing them). Approved architecture is never rewritten. `rebase` creates a new draft bound to the newer approved PRD, preserving IDs and carrying the impact assessment. Approval is refused while out of date.

## 7. Architect Agent (LangGraph, stateless)

`POST /api/v1/architect/run`, with actions `analyze`, `generate`, `revise`, `rebase` and `quality`. Nodes:

`validate_context` (source hash matches the snapshot; approved status present) → `analyze_requirements` → `clarify` (returns material questions; interrupt) → `generate` (Gateway, schema-constrained JSON) → `validate_structure` → `repair` (≤ 2 bounded retries with validation errors) → `deterministic_checks` → `result`.

PRD text and model output are untrusted data inside delimited blocks. The system policy forbids following embedded instructions, and the graph has no tools. The response carries provider, model, prompt version, attempts, node trace and usage only when the Gateway returned it. The Agent never returns approval states; Project Service ignores any status field in model output. Duplicate execution is prevented by the Project Service operation key plus the Agent's request-ID replay (M2 pattern). Cancellation and timeouts are bounded; restart recovery marks interrupted operations failed, and an explicit retry is required.

Model profiles reuse the Gateway catalog (provider, model, limits, streaming) and the project allow-list. The Agent adds `architect_timeout`, `architect_retries ≤ 2`, `architect_output_tokens` and the context budget. There is no provider fallback outside the allow-list.

## 8. API (Project Service, `/api/v1/projects/{project}/architecture`)

| Prompt §14 concept | Implemented route |
|---|---|
| list/create architectures | `GET/POST /sessions` (body: requirements session, model) |
| architecture, revisions | `GET /sessions/{id}`; `GET /sessions/{id}/revisions/{rev}` |
| create revision, clarify, resume, review | `POST /sessions/{id}/commands` and `/commands:stream` (SSE). Actions: analyze, answer, generate, revise, rebase, quality, save, finding, submit, decide. Idempotency-Key, expected_version |
| traceability, diagrams, ADRs | `GET /sessions/{id}/revisions/{rev}/traceability`, `/views/{view}?format=plantuml|mermaid|json`, ADRs inside the revision document |
| compare | `GET /sessions/{id}/compare?left&right` (ID-based structural diff per section) |
| approved baseline | `GET /sessions/{id}/baseline`: immutable package, content hash, approval evidence, source PRD binding and effective ADR statuses. This is the input for future agents |
| drift | `GET /sessions/{id}/drift` |
| export | `GET /sessions/{id}/revisions/{rev}/export?format=markdown|json|plantuml|mermaid` |
| history | `GET /sessions/{id}/history`: cursor pagination pinned to one snapshot (`through_sequence`) |

Errors follow the existing typed envelope, with 401/403/404/409/413/422/429/502/503/504. Input limits: package ≤ 300 000 UTF-8 bytes; list caps per section; enums validated.

## 9. Studio (masd-web)

A new lazy route `projects/:projectId/architecture[/:sessionId]` and a navigation entry beside Requirements Studio. Sections: dashboard; conversation (questions linked to requirements, model selection, progress via SSE, retry/resume); document workspace (section navigation, editable drafts, read-only approved versions); C4 explorer (native SVG, level tabs, zoom/pan, element inspector, requirement links, PlantUML/Mermaid/SVG download, validation errors shown); service-boundary, technology and ADR explorers (status filter); traceability matrix (uncovered first); revision comparison; review and approval. Recovery behaviour reuses the hardened M2 patterns (idempotency keys, settle-before-discard, latched stop).

## 10. Testing strategy

Covered with deterministic `test/structured` fixtures through the real Gateway path:
- unit tests for schema, validation, identity preservation, diff, PlantUML/Mermaid generation, transitions and approval invariants;
- real PostgreSQL integration tests;
- Agent graph tests (invalid JSON, repair, Gateway failure, clarification interrupt, duplicate request, cancellation, no tools);
- Angular unit tests;
- a Chromium end-to-end run from approved PRD to immutable approved architecture, plus restart, stale approval, drift and unauthorized-user scenarios.

There is no live-provider claim.
