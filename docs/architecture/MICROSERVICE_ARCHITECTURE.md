# Microservice architecture

Approved by revised M0: each application/service owns a separate Git repository, build, tests, image, CI pipeline and version. M0 bootstraps only central governance, web, project service, contracts and infrastructure. Independent builds cannot require another service source checkout.

Services own their logical database/schema. No cross-service table reads or shared persistence model. Prefer domain APIs and versioned events; use sagas and eventual consistency instead of distributed transactions. Dependencies must form an acyclic graph. Avoid long synchronous chains; orchestrator coordinates long-running work without making services share a release cadence.

M0's UI talks directly to Project Service through a development or nginx reverse proxy. A separate API gateway is planned when identity/routing requirements justify it. Contracts are copied as explicitly pinned candidate inputs and later published as immutable versions; consumers do not build from unreleased branch heads. Infrastructure may coordinate runtime images without coupling their compilation.

Retained technical baseline: Angular/TypeScript, Python/FastAPI/Pydantic; future Temporal, LangGraph, LiteLLM, PostgreSQL/pgvector, Docker Compose, Kubernetes, Terraform/OpenTofu, OIDC, OPA, OpenTelemetry, Prometheus/Grafana and potential Langfuse. OpenHands SDK remains an evaluation candidate. UI uses a consistent reusable CSS shell; selection of a larger component library remains open.
