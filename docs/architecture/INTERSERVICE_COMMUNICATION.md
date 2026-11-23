# Interservice communication

M0 contract candidate: masd-contracts/openapi/project-service-0.1.0.json. GET /api/v1/health returns status=ok; GET /api/v1/ready returns status=ready. Both include service=masd-project-service and version=0.1.0. Consistent error JSON contains code and detail. Health means the process responds; readiness currently has no downstream dependencies.

Consumers hold identical 0.1.0 snapshots; no sibling checkout or live registry is required to compile. Contract CI validates OpenAPI structurally and checks mandatory operations. Backend tests validate real responses against the pinned schemas and check operation IDs. Frontend uses a typed API abstraction, runtime response validation and contract-based unit tests. Publish immutable v0.1.0 after review; until then snapshots are explicitly candidates, not published releases.

Future policy: semantic contract versions; additive compatible changes within a major version; removing fields, tightening input requirements or incompatible semantics requires a new major API/event version and a migration window. Preserve supported old operations until consumers migrate. Compatibility review is mandatory; M0 has no previous published baseline for automated historical diffing.

Future events carry schema_version, event_id, type, occurred_at, project_id, correlation_id, causation_id and domain payload. Publish schemas before events, use idempotent consumers and outbox/inbox delivery, tolerate duplicates and define ordering per aggregate. Use saga compensation for multi-domain workflows. AuthN/AuthZ and trace context must cross boundaries; they are planned, not enforced in M0.
