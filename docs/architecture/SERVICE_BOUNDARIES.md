# Repository ownership and service boundaries

Initial accountable repository owner is swapnilpuri. Team assignment can change independently; domain ownership remains explicit in repository.json.

| Repository | Owns | Interfaces/dependencies | Status / milestone |
| --- | --- | --- | --- |
| MultiAgentSoftwareDelivery | Architecture, ADRs, governance, consolidated acceptance | Standards references, cross-repo release evidence | M0 |
| masd-web | Angular control center and user interaction | Versioned domain APIs; no database access | M0 shell only |
| masd-project-service | Project lifecycle metadata; future PRDs/requirements | /api/v1 health/readiness now; future own PostgreSQL schema | M0 stateless |
| masd-contracts | OpenAPI/event schemas, compatibility rules, immutable releases | Reviewed snapshots consumed independently | M0 candidate |
| masd-infrastructure | Local Compose, future deployment modules | Independently tagged service images | M0 local only |
| masd-api-gateway | External identity, routing, rate limits | Domain APIs; never domain persistence | Future, before external exposure |
| masd-orchestrator | Durable delivery workflow state | Temporal, domain APIs/events, approved tasks | Future M3 |
| masd-agent-service | Logical agent definitions and LangGraph execution state | LLM gateway, proposed tool actions | Future M3 |
| masd-llm-gateway | Model/provider routing and quotas | LiteLLM, OpenAI/Anthropic/Ollama | M1 provider routing implemented; no agents |
| masd-governance-service | Standards bundles, policy/approval decisions | OPA or equivalent, independent policy persistence | Future M3/M6 |
| masd-integration-service | GitHub and enterprise adapters | Scoped external APIs; isolated credentials | Future M2/M4 |
| masd-execution-worker | Isolated code/test/tool execution | Approved task envelopes → evidence/artifacts | Future M4 |

No empty implementation is created for future repositories. Agent roles (PM, architecture, QA, security, DevOps) do not justify new services by themselves. A new service requires an independently owned domain and deployment reason. Project service alone owns future project tables; workflow, policy and adapter data belong to their respective domains.


M1 update: Project Service owns PostgreSQL projects, settings, conversations, messages and turn/usage records. masd-llm-gateway is now implemented independently for authorized LiteLLM discovery/routing/streaming; it has no database access. Angular calls Project Service only. Contracts 0.2.0 are additive; all other future services remain unimplemented.
