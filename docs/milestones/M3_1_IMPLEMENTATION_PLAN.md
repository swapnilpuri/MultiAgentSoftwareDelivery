# M3.1 implementation plan — UX modernization, rich AI responses, unified auth, multi-provider models, workflow reliability

Status: **IN PROGRESS** (started 2026-11-24). M4 is blocked until M3.1 is accepted.

M3 status: the six M3 component PRs were merged into `main` on 2026-11-24 on the owner's instruction. Central PR #12 records that merge and the post-merge verification, but it is still open. Until it merges, the M3 completion report, handoff and acceptance files on `main` still describe the pre-merge state. M3 acceptance is the owner's only open M3 action.

The requirement source is [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md): the owner's milestone prompt (R1–R10 and the acceptance scenario), recorded verbatim. The output-quality reference is `HRMSSystem.pdf`, which is supplied by the owner and kept outside Git.

## 1. Baseline inspected (read-only)

| Area | Implementation on `main` before M3.1 |
|---|---|
| Web shell | Angular, flat 11-item nav (`masd-web/src/app/navigation.ts`); 7 items route to a `Future` placeholder; no breadcrumbs or shared project context |
| Login | Cookie human session in Project Service (`human_auth.py`, `/auth/session`), but Requirements Studio and Architecture Studio each render their **own** login form; AI Chat (`workspace.py`) does not use human auth at all (`local_user_id`) |
| Requirements ops | `requirement_operations(id, session_id, key, request_hash, status, result)`; generation runs **inside** the HTTP request (`commands` / `commands:stream`) |
| Architecture ops | Same pattern (`architecture.py`, `architecture_operations`) |
| Startup recovery | `main.py` lifespan marks running requirements and architecture operations `failed`; no reason or code is recorded. M3.1 B1 changes this for requirements operations only: they become `failed`/`INTERRUPTED` with a reason (see §2a). Architecture operations keep the old behaviour until B3. |
| Gateway | `masd-llm-gateway`, LiteLLM; providers `openai`, `anthropic`, `ollama`, `test`; no Gemini, no OpenAI-compatible custom endpoint |
| AI Chat rendering | `markdown-view.ts` (30 lines); no tables, code highlighting, diagrams, versions, profiles |
| Upload / import | None |
| Limits | Hard-coded Pydantic `max_length` (12 000 description, 4 000 instruction); nginx `client_max_body_size 100k`; no capability endpoint |
| Response→artifact | None; PRD and architecture are generated only by their own agents |

## 2. Root cause of the Generate PRD freeze (R6)

The freeze comes from three defects that compound each other:

1. **Execution is coupled to the HTTP stream.** `stream_command` starts `command()` as a child task, and its `finally:` **cancels** that task when the response ends. This happens on a client abort, the 250 s client timer, the nginx `proxy_read_timeout 240s`, a tab reload or a network drop. The cancellation marks the operation `failed`, and the generated PRD is discarded.
2. **The same-key replay is a dead end.** A replay of a `failed` key, or of a key that is still `running`, gets the same 409, "Operation is running or interrupted; reload before explicit retry". That text is wrong for a failed key. No server state can ever make that key succeed, and no failure reason is stored.
3. **The client locks itself.** After a non-4xx failure, `RequirementsStudio.retry()` keeps `pending` with `uncertain: true`, and persists it to browser session storage. Several things then block the user:
   - `run()` refuses every action while `pending` is set.
   - `canLeave()` and the `requirementsLeave` guard block navigation to every other section.
   - `beforeunload` prompts on reload.
   - `retry()` resends the dead key and gets the 409 again.
   - `discardPending()` needs a 60 s settle time and a `window.confirm`.

   The pending record is restored after a reload. The user sees the 409, cannot navigate, and must hard-refresh, which only brings the lock back.

The fix keeps the existing architecture: Project Service stays authoritative and the Agent stays stateless. Section 4, B1–B2, describes it.

## 2a. Operation lifecycle after B1 (requirements operations)

- **States.** `running`, then exactly one of `completed`, `failed` or `cancelled`. The `stage` field records real progress: `queued`, `generating`, `validating`, then the terminal value. `error_code` and `failure_reason` explain every `failed` or `cancelled` row. Startup and shutdown use `INTERRUPTED`, cancellation uses `CANCELLED`, and a failed final commit uses `COMMIT_FAILED`. `INTERRUPTED` is an error code rather than a state, because the service never resumes an operation: an explicit retry with a new key starts a new one.
- **Ownership.** An app-owned task executes the operation with its own DB session. Requests and streams only observe it, so a lost observer never cancels the work.
- **Exclusive terminal transition.** Completion and cancellation cannot both win:
  - Failure, cancellation and restart release an operation with conditional updates: `UPDATE requirement_operations ... WHERE status = 'running'`, plus clearing `requirements_sessions.active_operation_id` only if it still names the operation.
  - The runner saves a result only after re-reading the session under its row lock (`FOR UPDATE NOWAIT` on PostgreSQL) and checking that `active_operation_id` still names its operation.
  - Whichever transition takes the session row first wins. The other becomes a no-op, or the runner gets a 409 and saves nothing.
  - This is covered by `test_cancel_and_completion_cannot_both_win`.
- **Backstops.** `finalize_if_running` and background `ensure_terminal` record outcomes the worker could not persist. Startup recovery reconciles any row that is still `running`.

## 3. Gap analysis

| Req | Gap | Batch |
|---|---|---|
| R1 Unified UI | New shell with 6 sections, breadcrumbs, project context, page header, help, loading, empty and error states; existing CSS tokens reused | B4 |
| R2 Rich AI Workspace | Markdown with GFM tables, highlighted code, Mermaid rendered in a sandbox, collapsible sections, streaming, copy/regenerate/save, response versions, profiles (Concise/Standard/Comprehensive), virtualised long rendering | B6 |
| R3 Response→artifact | `promotions` record (source response and version, selected sections, hash, target type) → draft artifact → human approval; source edits never mutate an approved artifact | B8 |
| R4 Upload/import | `sources` service in Project Service: PDF and text with signature checks, a URL fetcher with an SSRF guard, provider handlers for ChatGPT/Claude/Gemini shared links (best effort with explicit failure reasons), transcript paste fallback, untrusted-content delimiting, audit, retention | B7 |
| R5 Limits | A `GET /api/v1/capabilities` endpoint feeding the UI counters; server-side enforcement; a documented chunking and extraction strategy | B5 |
| R6 PRD reliability | Durable background operation; attach, observe or replay by key; explicit retry with a new key; failure reasons; restart reconciliation; non-blocking client | **B1–B2** |
| R7 Operation visibility | Operation resource and list (project-scoped); reusable operation panel; SSE observe with polling fallback; no fabricated percentages (stage only) | B1–B3 |
| R8 Unified auth | One app-level login and route guard; studio-local login removed; AI Workspace moved onto the human principal; central logout; session renewal. An OIDC provider integration needs an owner decision (§5) | B4 |
| R9 Multi-provider | Gateway adds `gemini` and `openai_compatible`; capability metadata, status and errors; credentials only from server configuration | B5 |
| R10 Quality/docs | Contract tests per service, Playwright journeys, docs | every batch, then B9 |

## 4. Batches (each one is a coherent PR set; contracts land first)

| Batch | Repos | Scope |
|---|---|---|
| B1 | project-service, contracts | Durable requirements operations: migration `0005`, an app-owned runner that is independent of the request, observe/attach on replay, operation GET/list/cancel, failure reasons, startup reconciliation, regenerated 0.5.0 OpenAPI |
| B2 | web | Requirements Studio: non-blocking generation, reconnect after a reload, an operation status panel, explicit retry, no navigation lock while the server is running |
| B3 | project-service, web | Apply the B1/B2 pattern to Architecture operations; add a project-level Operations/Activity page |
| B4 | web, project-service | Application shell plus unified login; Chat on the human principal |
| B5 | llm-gateway, project-service, web | Providers (Gemini, OpenAI-compatible), capability endpoint, limits UI |
| B6 | web, project-service | Rich AI Workspace, profiles, versions |
| B7 | project-service, web, infrastructure | Upload and import with security controls |
| B8 | project-service, web | Response→artifact promotion and traceability into Requirements and Architecture Studio |
| B9 | web, infrastructure, central | E2E acceptance scenario, final regression, completion report |

## 5. Owner decisions needed (non-blocking for B1–B3)

1. **OIDC provider:** the options are a Keycloak container in the dev stack or an external IdP. Until the owner decides, B4 unifies the existing cookie session behind an OIDC-ready boundary.
2. **Live-provider credentials:** these are needed only for the optional smoke test. Deterministic mock providers are used otherwise.

## 6. Progress

| Batch | Branch | PRs | Status |
|---|---|---|---|
| B1 | feature/m3.1-durable-operations | [contracts#6](https://github.com/swapnilpuri/masd-contracts/pull/6), [project-service#6](https://github.com/swapnilpuri/masd-project-service/pull/6), [infrastructure#7](https://github.com/swapnilpuri/masd-infrastructure/pull/7) | PR open, awaiting CI and review |
| B2 | feature/m3.1-durable-operations | [web#7](https://github.com/swapnilpuri/masd-web/pull/7) | PR open, awaiting CI and review |
| B3–B9 | — | — | not started |

### B1–B2 evidence (2026-11-24, branch heads after review round 1)

| Check | Result |
|---|---|
| contracts `scripts.check` | 83 passed; 8 OpenAPI documents valid; 0.1.0–0.4.0 byte-identical |
| project-service `scripts.check` | 181 passed / 6 PostgreSQL-only skips; ruff, mypy, secrets and audit clean |
| project-service on real PostgreSQL 17 (throwaway container) | 187 passed, 0 skipped |
| web `scripts.check` (from `C:\`) | 106 Angular tests, build and 22 Python tests |
| infrastructure `scripts.check` | 74 passed (+1 POSIX-only skip) |
| Chromium, rebuilt `masd-m2` stack | 5/5 |
| `verify_m2_restart` / `verify_m3_restart` | PASS / PASS. M2 asserts that the replay names exactly the recorded `INTERRUPTED` reason |
| `verify_m2 runtime-secrets` | PASS |
| Review round 1 | 34 Sourcery findings (contracts 6, project-service 8, web 15, infrastructure 1, central 4). All were fixed with a regression test or a document change, then replied to and resolved |

Not yet demonstrated live: a browser reload during a *long* generation. The deterministic adapter answers too fast for that, so it is covered by the service disconnect test and the web unit tests. It is scheduled for the B9 acceptance run.
