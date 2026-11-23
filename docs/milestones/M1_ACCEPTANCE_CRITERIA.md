# M1 acceptance criteria

Status: implementation verification completed for independent human acceptance review. No automatic milestone acceptance or PR merge is claimed.

| Criterion | Status | Implementation and actual evidence |
| --- | --- | --- |
| AC-01 Standards | PASSED | Six manifests/AGENTS references; mandatory compliance and negative regressions, local and independent CI |
| AC-02 Angular create/PostgreSQL | PASSED | Projects/ProjectForm; real Compose browser create plus Project Service PostgreSQL tests |
| AC-03 Project lifecycle | PASSED | workspace APIs, Angular list/detail/edit/archive; browser archive retained history/read-only composer |
| AC-04 Independent Project Service | PASSED | Own migrations/dependencies/Dockerfile/CI; 35 tests, independent image build |
| AC-05 Independent gateway | PASSED | Separate private repo, health/readiness, isolated Docker context and CI |
| AC-06 Three provider adapters | PASSED | LiteLLM OpenAI/Anthropic/Ollama mocked routing tests; live credentials not available, explicitly separate |
| AC-07 Select model | PASSED | Angular default/allowlist and conversation selector; configured deterministic model selected in real workflow |
| AC-08 Scoped conversations | PASSED | Create/list/get/rename APIs and sidebar; persistence/retrieval and browser workflow |
| AC-09 Stream rendering | PASSED | Incremental SSE, formal event schema validation, browser receiving/completion, component streaming tests |
| AC-10 Restart persistence | PASSED | Page reload and PostgreSQL/API/gateway restart retained message IDs and completed outcome |
| AC-11 Project/user isolation | PASSED | Owner/project predicates; distinct configured user tests, cross-project API denial and browser A/B isolation |
| AC-12 Safe failures | PASSED | Normalized credential/model/rate/context/timeout/unavailable/unsupported failures; redaction and recovery tests |
| AC-13 Credential isolation | PASSED | Gateway-only optional keys, generated ignored secrets, source/log checks; no production-security claim |
| AC-14 Published contracts | PASSED | Immutable contracts-v0.2.0-rc.2 OpenAPI/SSE candidate; exact consumer blobs, offline validation and real payload checks |
| AC-15 Unit/integration tests | PASSED | 174 Python tests, 13 Angular tests, 35-test real PostgreSQL run and 3-browser workflow; exact commands in report |
| AC-16 Local integration | PASSED | Four healthy Compose services, smoke, real browser, persistence and restart verification |
| AC-17 Independent deployment | PASSED | UI image update preserved backend images/containers; gateway standalone build and per-service contexts |
| AC-18 Independent CI | PASSED | Six pipelines configured; required checks block failure, full-SHA actions; exact final-head status linked on PRs |
| AC-19 Durable handoff | PASSED | Central and per-repository M1 handoffs, compatible commits, commands, results and limits |
| AC-20 Current architecture | PASSED | ADR 0004, data/security/service boundaries and authorized roadmap updated |
| AC-21 No autonomous execution | PASSED | Only catalog-selected chat; no tools/system-command/coding/deployment endpoints or agent runtime |
| AC-22 Git workflow | PASSED | M1 feature branches, independent stacked PRs, private gateway authorization; no protected merge/force-push |

Optional live commercial/installed-Ollama smoke tests are NOT EXECUTED, not passed. Production identity, multi-replica recovery, policy enforcement and cloud deployment remain future scope. Independent human architectural/acceptance review and stable release promotion remain outstanding.
