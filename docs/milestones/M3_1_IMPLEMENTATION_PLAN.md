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

### Deployment order for migrations 0005 and 0006

Project Service runs as a **single replica**. The runtime ownership guard (`runtime_guard.py`, unchanged since M2) refuses to serve while another instance holds ownership, and readiness pins the exact required revision. Upgrades are therefore **stop, then migrate, then start**:
1. Stop the old instance. Its running operations are marked `INTERRUPTED` with a reason at shutdown, or at the next startup.
2. Start the new image, which applies the additive migration.
3. Wait for readiness.

A rolling upgrade with mixed versions is not supported. Both migrations only add nullable columns, so `downgrade` restores the previous schema if a rollback is needed. The `masd-m2` compose stack and the restart verifiers use exactly this order.

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
| B4 | contracts, project-service, infrastructure, web, central | Application shell plus unified login (Keycloak in the dev stack, OIDC through Project Service, contract 0.7.0); Chat on the human principal |
| B5 | llm-gateway, project-service, web | Providers (Gemini, OpenAI-compatible), capability endpoint, limits UI |
| B6 | web, project-service, llm-gateway, contracts, infrastructure | Rich AI Workspace, profiles, versions; removes the short-answer limits (gateway 0.4.0) |
| B7 | contracts, project-service, web, infrastructure, central | Upload and import with security controls |
| B8 | project-service, web | Response→artifact promotion and traceability into Requirements and Architecture Studio |
| B9 | web, infrastructure, central | E2E acceptance scenario, final regression, completion report |

## 5. Owner decisions needed (non-blocking for B1–B3)

1. **OIDC provider:** decided 2026-11-24. The owner chose a **Keycloak** container in the dev stack, so B4 adds Keycloak and moves the single login onto OIDC.
2. **Live-provider credentials:** these are needed only for the optional smoke test. Deterministic mock providers are used otherwise.

## 6. Progress

| Batch | Branch | PRs | Status |
|---|---|---|---|
| B1 | feature/m3.1-durable-operations | [contracts#6](https://github.com/swapnilpuri/masd-contracts/pull/6), [project-service#6](https://github.com/swapnilpuri/masd-project-service/pull/6), [infrastructure#7](https://github.com/swapnilpuri/masd-infrastructure/pull/7) | merged |
| B2 | feature/m3.1-durable-operations | [web#7](https://github.com/swapnilpuri/masd-web/pull/7) | merged |
| B3 | feature/m3.1-architecture-operations | [contracts#7](https://github.com/swapnilpuri/masd-contracts/pull/7), [project-service#7](https://github.com/swapnilpuri/masd-project-service/pull/7), [web#8](https://github.com/swapnilpuri/masd-web/pull/8), [infrastructure#8](https://github.com/swapnilpuri/masd-infrastructure/pull/8) | merged |
| B4 | feature/m3.1-shell-auth | [contracts#8](https://github.com/swapnilpuri/masd-contracts/pull/8), [project-service#8](https://github.com/swapnilpuri/masd-project-service/pull/8), [infrastructure#9](https://github.com/swapnilpuri/masd-infrastructure/pull/9), [web#9](https://github.com/swapnilpuri/masd-web/pull/9), [central#15](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/15) | merged |
| B5 | feature/m3.1-providers-limits | [contracts#9](https://github.com/swapnilpuri/masd-contracts/pull/9), [llm-gateway#4](https://github.com/swapnilpuri/masd-llm-gateway/pull/4), [project-service#9](https://github.com/swapnilpuri/masd-project-service/pull/9), [web#10](https://github.com/swapnilpuri/masd-web/pull/10), [infrastructure#10](https://github.com/swapnilpuri/masd-infrastructure/pull/10), [central#17](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/17) | merged |
| B6 | feature/m3.1-rich-workspace | [contracts#10](https://github.com/swapnilpuri/masd-contracts/pull/10), [llm-gateway#5](https://github.com/swapnilpuri/masd-llm-gateway/pull/5), [project-service#10](https://github.com/swapnilpuri/masd-project-service/pull/10), [web#11](https://github.com/swapnilpuri/masd-web/pull/11), [infrastructure#11](https://github.com/swapnilpuri/masd-infrastructure/pull/11), [central#19](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/19) | Merged 2026-11-25: contracts `4dcbdcd`, llm-gateway `4704e39`, project-service `2dcc88d`, web `1c31f5a`, infrastructure `20f5b77`, central `d486376` |
| B7 | feature/m3.1-upload-import | [contracts#11](https://github.com/swapnilpuri/masd-contracts/pull/11), [project-service#11](https://github.com/swapnilpuri/masd-project-service/pull/11), [web#12](https://github.com/swapnilpuri/masd-web/pull/12), [infrastructure#12](https://github.com/swapnilpuri/masd-infrastructure/pull/12), [central#21](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/21) | Merged 2026-11-26: contracts `1ebe098`, project-service `e500d59`, web `842a531`, infrastructure `9d93152`, central `ee7afa2` |
| B8–B9 | — | — | not started |

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

### B3 evidence (2026-11-24, branch heads)

| Check | Result |
|---|---|
| contracts `scripts.check` | 85 passed; 9 OpenAPI documents; 0.1.0–0.5.0 byte-identical |
| project-service `scripts.check` / real PostgreSQL 17 | 188 passed / 6 skipped; **194 passed, 0 skipped** |
| web `scripts.check` | 110 Angular tests, build |
| infrastructure `scripts.check` | 74 passed (+1 POSIX-only skip) |
| Chromium, rebuilt `masd-m2` stack (all B3 branches) | 5/5 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS (architecture now records `INTERRUPTED`) / PASS |
| Operations page visual check | 1280 px and 390 px; no overflow |

Not yet demonstrated live: a browser reload during a *long* generation. The deterministic adapter answers too fast for that, so it is covered by the service disconnect test and the web unit tests. It is scheduled for the B9 acceptance run.

### B4 design (unified login and application shell, R1 and R8)

| Decision | Choice and reason |
|---|---|
| Login flow | OIDC authorization code with PKCE S256, completed by Project Service as a backend-for-frontend with a confidential client. No token reaches the browser, and the existing httpOnly `masd_human` session and owner checks are reused. |
| Provider exposure | Keycloak is served on the web origin at `/auth` through the nginx proxy, so cookies and the callback stay first-party. Project Service uses an internal backchannel URL, and the issuer stays public. |
| Principal | `preferred_username` (username editing is disabled), so existing `owner_id` data stays valid. Migration `0008` binds each username to its provider subject on first sign-in, so a re-created account that reuses the name is refused (`identity_conflict`) instead of inheriting projects. If the pre-B4 `MASD_LOCAL_USER_ID` differs from the SSO username, `python -m project_service.ownership --from-owner … --to-owner …` transfers the projects; it is a dry run without `--apply`. Sign-in requires `masd-user`, approval requires `masd-approver`, and the tenant comes from the `masd_tenant` claim. Project access checks both owner and tenant (migration `0007`). |
| Session | The refresh token is encrypted at rest. A sliding renewal re-checks the provider every 5 minutes: role changes apply, and a revoked account ends the session. An outage defers renewal only within the 30-minute idle expiry, with a 10-hour absolute limit. Logout also ends the provider SSO session. |
| Single entry point | Password sign-in exists only when OIDC is not configured (unit tests, `ng serve`). With SSO configured it returns 403, and existing password sessions end. |
| Contract | 0.7.0. Its only non-additive change is that workspace routes (AI Workspace) require the session; the single consumer migrates in this batch. 0.1.0–0.6.0 are byte-identical. |
| Shell | Six sections, with the project context remembered by ID only, breadcrumbs, titles, per-section help, navigation loading and error states, a responsive menu, and redirects from retired roadmap URLs. |

### B4 evidence (2026-11-25, branch heads after review round 1)

| Check | Result |
|---|---|
| contracts `scripts.check` | 91 passed; 10 OpenAPI documents; 0.1.0–0.6.0 untouched |
| project-service `scripts.check` / real PostgreSQL 17 | 231 passed / 7 skipped; **238 passed, 0 skipped** |
| web `scripts.check` (from `C:\`) | 154 Angular tests, lint, build (initial bundle 372 kB) |
| infrastructure `scripts.check` | 89 passed (+1 POSIX-only skip) |
| Chromium, rebuilt `masd-m2` stack with Keycloak 26.4.7 | 9/9. Covers: one sign-in across all six sections, reload, no credential in browser storage, an httpOnly strict cookie, deep-link return, central sign-out (provider asks again), reviewer cannot approve, outsider refused, and the M1–M3 journeys through SSO |
| `verify_m2_restart` / `verify_m3_restart` | PASS / PASS, signed in through the real Keycloak form |
| `verify_m2 runtime-secrets` | PASS. Now also scans Keycloak logs and the B4 secrets (client secret, session secret, provider admin, test accounts) |
| Shell visual check | 1280 px and 390 px; no horizontal overflow |

Review round 1 (37 Sourcery findings: contracts 5, project-service 14, web 10, infrastructure 8) was fixed with regression tests. The main changes:
- **Session renewal:** serialized and re-read under a row lock. A rotated refresh token survives a failed commit or a signing-key outage, and an outage backs off for 60 s.
- **Sign-in flow:** each attempt has its own state cookie, the issuer must match exactly, `azp` is required with multiple audiences, and usernames are bound to subjects.
- **Logout:** the local session is committed first, and an expired session can still sign out.
- **Project access:** owner and tenant are checked before the row lock.
- **Web:**
  - sign-out success is shown only when the server confirmed it;
  - a late identity lookup cannot revive a signed-out session;
  - the previous human's operations are cleared when a different human signs in;
  - a same-origin API is required;
  - recovery markers are scoped to their human;
  - the project context survives transient errors and follows renames;
  - unsaved project forms are guarded.
- **Infrastructure:** the SSO account file always derives from `.env.m2`, blank or commented settings are refused, and sign-in reads have a total deadline.
- Two findings were addressed differently from their suggestion, and the replies explain why. The callback `state` stays optional in the schema so that a provider error still ends in the friendly redirect; its rule is documented instead. The `browser.newPage()` baseURL finding did not reproduce, but `baseURL` is now passed explicitly.

Found and fixed during live verification:
- **Bootstrap dependency cycle** (Router → TitleStrategy → ProjectContext → WorkspaceApi → Auth → Router). A production-provider test now guards it.
- **Studios swallowed navigation silently** while their initial read was loading (`canLeave` refused any `busy` state). This predates B4. Reads no longer block leaving, and a real block now explains itself.
- **OIDC client deadlock.** A non-reentrant lock was held across metadata and JWKS loading.

### B5 design (providers and limits, R5 and R9)

**Providers (llm-gateway 0.3.0).** `gemini` and `openai_compatible` join `openai`, `anthropic`, `ollama` and `test`. All of them go through LiteLLM and must be configured explicitly in `MASD_MODELS`.
- **Credentials** come only from the gateway environment and travel in headers. The OpenAI-compatible endpoint has its own optional key and never receives the OpenAI key.
- **Availability is verified, not assumed.** Each catalog refresh (single-flight, `MASD_CATALOG_TTL` 30 s) lists models with the configured credential, in parallel, with a 3 s timeout. A model is `available` only when it is enabled, its provider answered, and the provider lists it. Otherwise `unavailable_reason` gives a code. An unavailable provider affects only its own models.
- **Discovered limits.** Gemini's reported token limits fill an unconfigured `context_limit` or `output_limit`.
- **Provider status.** `GET /api/v1/providers` reports each provider's status without URLs or keys.
- **Retries** (`MASD_PROVIDER_RETRIES`, default 1) happen only while opening a stream.
- **Usage and errors.** Usage is requested from OpenAI and Gemini. Error classes add `CONTENT_FILTERED`, `INVALID_REQUEST` and an HTTP-status fallback.

**Limits (Project Service 0.8.0).** `GET /api/v1/capabilities` (session) returns the enforced text limits, each available model's `prompt_max_chars`, the provider status, `catalog_available` and the long-input policy.
- **Single source.** `project_service/limits.py` holds the Pydantic ceilings (the published `maxLength`), the configured limits, which may only lower them, and `prompt_limit()`. The endpoint and chat submit both use `prompt_limit()`.
- **Per-model limit.** `min(chat limit, budget − project-context reserve (≤ 2 000) − 128)`, where `budget = min(MASD_CONTEXT_BUDGET, context − output − 256)`.
- **Enforcement.** An over-limit chat message or requirements description gets a 422 that names both numbers, before any turn or session is created.

**Long-input strategy.** Reject, never truncate.
- Each turn sends the project context (capped at 2 000 characters), then completed turns, newest first, while they fit. The turn records the IDs of the messages it included.
- Both services now count characters instead of UTF-8 bytes. Characters are a conservative token proxy, and they match the counter.
- Long documents are handled by the B7 extraction pipeline.

**Defects found during design.**
- With the default `MASD_CONTEXT_BUDGET=6000`, the UI accepted 12 000 characters, but the server rejected anything over about 3 900 bytes after the user submitted.
- Adding a new provider would have broken `/models`, because Project Service's `ModelInfo.provider` was a closed enum.

**Web.**
- A `Capabilities` service never throws, and it loads independently of the model list.
- A reusable `app-char-counter` shows the count and the limit, the remaining characters or the overflow, and an explicit alert.
- Prompt fields drop `maxlength`, because the browser silently cut pasted text. Submission is disabled over the limit instead.
- Counting uses code points, matching Python `len`.
- The AI Workspace shows the selected model's limits, and lists allowed models that are unavailable, with the reason.
- Settings shows the provider status, the limits and the policy.

### B5 evidence (2026-11-25, branch heads)

| Check | Result |
|---|---|
| contracts `scripts.check` | 95 passed; 12 OpenAPI documents; 0.1.0–0.7.0 and llm-gateway 0.2.0 untouched |
| llm-gateway `scripts.check` | 80 passed (30 new) |
| project-service `scripts.check` / real PostgreSQL 17 | 242 passed / 7 skipped; **249 passed, 0 skipped** |
| web `scripts.check` (from `C:\`) | 163 Angular tests (+9), lint, typecheck, build, audit |
| infrastructure `scripts.check` | 89 passed (+1 POSIX-only skip) |
| central | `test_m2_verifier.py` 24 passed (4 new: a provider key in gateway logs fails the scan) |
| Chromium, rebuilt `masd-m2` stack | **10/10**. The new journey checks four things: the limit read from `/capabilities` is shown; an over-limit paste stays intact, with the overflow shown and the send disabled; the server returns 422 to a client that skips the UI; and a message exactly at the limit is answered |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS (the scan now also covers the four provider keys) |
| Live-provider smoke test | Not run: no provider credentials were supplied |

#### B5 review round 1 (33 Sourcery findings: llm-gateway 15, project-service 6, contracts 4, web 4, infrastructure 2, central 2)

Fixed with regression tests:
- **Gateway: transport and retries.**
  - Plain `http` is accepted only for local or private hosts; any other host requires `https`. Invalid ports are rejected.
  - An unusable URL marks its provider unavailable instead of failing the whole catalog.
  - LiteLLM retries are off. The gateway retries only provider refusals (429 and 503), so an ambiguous failure can never run, and bill, a second generation.
- **Gateway: discovery.**
  - Listings follow Anthropic and Gemini pagination, bounded at 10 pages.
  - Gemini's HTTP 400 `API_KEY_INVALID` counts as invalid credentials, and HTTP 400 and 422 map to `INVALID_REQUEST`.
  - Ollama `/api/show` calls run concurrently, one per model, and one failed lookup no longer hides later models.
  - A configured Ollama model that cannot complete is no longer selectable, and `:latest` aliases are not discovered twice.
  - Configured counts exclude auto-discovered models, and an empty catalog is cached for the TTL.
- **Provider status.** It is closed in both services, rejects contradictory combinations, and has exactly one entry per provider.
- **Project Service.**
  - Text over the published ceiling gets the explicit length message, and other validation errors never echo input.
  - The configured chat limit is checked before the gateway, so invalid input gets a 422 even during an outage.
  - Capability schemas are closed and bounded by the request ceilings.
  - A separate `providers_available` flag is added, and failed gateway listings are logged.
  - A test now covers a project context far longer than 2,000 characters.
- **Web.**
  - A server refusal (400, 413 or 422) no longer leaves the composer locked. The text is kept, and the corrected message is sent with a new key.
  - The conversation title, studio answers and review comments use counters instead of `maxlength`.
  - Overlapping capability refreshes resolve in order, so the latest wins.
  - Capability errors are shown in both studios and in Settings, including stale values after a failed refresh.
- **Infrastructure README.** After editing `.env.m2`, containers must be recreated (`up`, not `restart`). Out-of-range limits are refused at startup.

Answered without a code change, with the reasons given in each thread:
- **Characters vs tokens.** The character budget is a deliberate trade-off. Text that tokenizes unusually densely gets the provider's classified `CONTEXT_LENGTH` error, never truncation. The gateway README now says so.
- **Rolling upgrades.** Project Service is single-replica, and the B5 deployment note already requires deploying the gateway and Project Service together.
- **Central "critical" finding.** It is incorrect: `read_credentials` never reads provider keys, which come only from the running container's environment. Real provider keys are far longer than the 12-character noise floor.

| Check after round 1 | Result |
|---|---|
| llm-gateway / contracts / infrastructure | 116 / 98 / 89 passed |
| project-service, real PostgreSQL 17 | 255 passed / 7 skipped; **262 passed, 0 skipped** |
| web | 174 Angular tests, lint, build |
| Chromium, rebuilt stack | 10/10 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS / PASS |

### B6 design (rich AI Workspace, R2)

**No artificial short-answer limits.** Before B6, a long answer was cut off in four places:
- the gateway's 60 s cap on the whole generation;
- Project Service's 90 s cap;
- a 64,000-character response cap;
- output-token defaults of 1,024 (Project Service) and 2,048 (gateway), with an 8,192 ceiling.

These limits are now:
- **Idle timeout.** `MASD_PROVIDER_TIMEOUT` is an *idle* limit: the first chunk and every later chunk must arrive within it.
- **Total time.** `MASD_GENERATION_MAX_SECONDS` (gateway) and `MASD_CHAT_MAX_SECONDS` (Project Service), both 900 s, bound a whole answer.
- **Output size.** `max_tokens` may be up to 32,768 (default 8,192), and is bounded by each model's `output_limit`. Context messages may be up to 64,000 characters, and request bodies up to 500 KB.
- **Contracts.** These widen llm-gateway to 0.4.0. Stored answers may be up to 200,000 characters.

**Response profiles.** Concise, Standard (the default) and Comprehensive are generation preferences, not separate architectures. Each profile adds a short instruction (under 400 characters) to the system message and requests a number of output tokens:

| Profile | Output tokens requested |
|---|---|
| Concise | up to 1,024 |
| Standard | up to 4,096 |
| Comprehensive | the model's full budget |

The context budget always reserves the model's full output budget, so the message limit is the same for every profile. The profile is stored on each turn, and `GET /capabilities` lists the profiles.

**Response versions.** Migration `0009_response_versions` adds four columns to `turns`: `profile`, `parent_turn_id`, `version` and `active`. Existing turns become version 1 of themselves. A regeneration is a new turn whose `parent_turn_id` is the root turn.
- **New endpoint `regenerate:stream`.** It re-answers the latest user message, optionally with another allowed model or profile, and is idempotent.
- **When a new version is shown.** A new version becomes active only when it completes, so a failed regeneration never replaces a good answer.
- **New endpoint `active-version`.** It shows another completed version. Later turns use only the active version as context; unselected versions and partial text never enter it.
- **Constraints.** Only the latest turn can be regenerated, so versions never reorder a conversation. Neither action is allowed while a response is running.
- **Contracts.** Project Service 0.9.0 is additive. `pre_b6` keeps 0.8.0 and earlier byte-identical.

**Rendering (web).**
- **Sections.** Responses are split into collapsible sections at each level-2 heading, with Expand all and Collapse all controls.
- **Tables** scroll horizontally.
- **Code.** 15 highlight languages, plus aliases.
- **Links.** External links open in a new tab with `noopener noreferrer nofollow` and are listed under Sources. Images and raw HTML stay inert.
- **Mermaid.** Version 12.3 is loaded on first use as a lazy chunk, so the initial bundle stays at 383 kB. It runs with `securityLevel: 'strict'` (no HTML labels, DOMPurify-sanitised output). The SVG is shown in an iframe with an empty `sandbox`, so it has no scripts and no same-origin access. A diagram that fails to render, is still streaming, or is over 20,000 characters is shown as source.
- **Long responses.** While streaming, rendering is throttled to once every 120 ms, and diagrams wait until the stream completes. `content-visibility: auto` lets off-screen sections of a long answer skip layout. A 100,000-character answer renders in well under a second in the unit test.

**AI Workspace actions.**
- A response-profile selector.
- A "Version n of m" navigator, and "Use this version" for an inactive completed version.
- Regenerate, on the latest turn only.
- Copy, and Save as Markdown.
- Every response carries an "AI response · not an approved artifact" badge, which distinguishes a helpful AI response from an approved engineering artifact. Promotion to a draft artifact comes in B8.

### B6 evidence (2026-11-25, branch heads)

| Check | Result |
|---|---|
| contracts `scripts.check` | 103 passed; 14 OpenAPI documents; 0.8.0 and llm-gateway 0.3.0 untouched |
| llm-gateway `scripts.check` | 120 passed (4 new: idle vs total limits, widened bounds) |
| project-service `scripts.check` / real PostgreSQL 17 | 268 passed / 7 skipped; **275 passed, 0 skipped** (13 new) |
| web `scripts.check` (from `C:\`) | 193 Angular tests (+19), lint, typecheck, build (initial bundle 384 kB; Mermaid is a lazy chunk), audit 0 |
| infrastructure `scripts.check` | 89 passed (+1 POSIX-only skip) |
| Chromium, rebuilt `masd-m2` stack | **11/11**, twice. The new journey covers six things: a Comprehensive-profile answer with collapsible sections, a table and a Mermaid diagram drawn by the lazy chunk in an empty-sandbox frame; Save as Markdown; a Concise regeneration shown as "Version 2 of 2"; browsing back to version 1; "Use this version"; and a reload that keeps that choice |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS. The stack upgraded its live PostgreSQL database from 0008 to 0009 |

Found during verification:
- **M3 Architecture journey flaked (1 in 3).** This is a pre-existing race. The command reply ("Saved. State: …") and the operation tracker's settlement ("… completed. Saved architecture is shown.") both report success, and either can arrive last. The journey now accepts either notice.
- **Back-to-back repeats fail.** Running the generation-heavy journeys several times in a row exceeds the gateway's local limit of 30 requests per minute per user, and Project Service then returns 503. This is a test-environment effect, not a defect: runs spaced by a minute pass 11/11.
- **Migration 0009 on SQLite.** Batch mode would have dropped the unnamed `turns.status` CHECK constraint. The migration now passes it explicitly, and a test asserts that it survives.

#### B6 review round 1 (39 Sourcery findings: web 13, project-service 10, llm-gateway 8, contracts 6, central 2)

Fixed with regression tests:
- **Gateway.**
  - An unauthorized POST is refused before its body is read, and a declared body over 500 KB is refused up front.
  - The context check reserves the capped output, not the raw `max_tokens`. With an unknown context window, only the input must fit 8192.
  - The total cap is a deadline checked between chunks, so a slow client still gets the `TIMEOUT` event. Cancelled provider calls are awaited before the request id is released.
  - `MASD_MAX_ACTIVE_GENERATIONS` (default 16) caps concurrent generations, whatever `user_id` the caller sends. The README's older limits text now matches 0.4.0.
- **Project Service.**
  - Regeneration without a profile keeps the original one, and the key is bound to it.
  - A key inserted concurrently elsewhere is a 409, not a 500.
  - Finalization re-reads the turn under a row lock, so a cancel that lands after the done check still wins and a cancelled version never becomes active.
  - History is filtered to shown, completed turns before its 200-row window.
  - A model without `output_limit` gets the configured budget, at most half its window.
  - `chat_result` logs record the profile.
  - Tests now check independent profile guidance, a large-output model, and the CHECK constraint with a valid foreign key.
- **Contracts (0.9.0, regenerated).** Both version routes document their conversation scope, their 404/409/422 failures (plus 429/503 for regenerate), and the idempotent replay. Regenerate shares the submit stream's `x-sse-events`. The tests pin the required headers.
- **Web.**
  - Stop cancels a regeneration on the server.
  - Version choices are serialized, block sending, and are applied in place, so loaded history stays.
  - Only the newest history snapshot applies, and a page split mid-turn is extended back to its prompt.
  - A route change clears a running regeneration, and the current version stays visible while a new one streams.
  - Regenerating with another model saves that model. The download URL is revoked later.
  - Protocol-relative links count as external sources, and headings render inline Markdown.
- **Central.** The handoff names the B6 PRs and no longer says no component PRs are open.

Answered without a code change, with the reasons given in each thread:
- **`Capabilities.profiles` is required.** Project Service is single-replica and ships with the web client of the same release, as with B5. The contracts README now says so.
- **`MASD_PROVIDER_TIMEOUT` is an idle limit.** The redefinition is the B6 design. The README and B6 deployment note 4 give the upgrade path (`MASD_GENERATION_MAX_SECONDS`).
- **Long chats and service resources.** Each conversation has one active generation, the gateway caps generations process-wide, and each user is limited to 30 requests a minute. At most 16 × 200,000 characters are buffered.

| Check after round 1 | Result |
|---|---|
| contracts / llm-gateway / infrastructure | 107 / 127 / 89 passed |
| project-service, SQLite / real PostgreSQL 17 | 276 passed, 7 skipped / **283 passed, 0 skipped** |
| web (from `C:\`) | 204 Angular tests, lint, typecheck, build, audit 0 |
| Chromium, rebuilt `masd-m2` stack | 11/11 |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS |

### B7 design (upload and import, R4 with the R5 long-input strategy)

**Inputs.** Each one creates a project source; the `Idempotency-Key` becomes the source ID, so a retry never duplicates one.

| Input | Route | Accepted |
|---|---|---|
| Upload | `POST .../sources:upload` (raw body, `filename` query) | PDF with a text layer, `.txt`, `.md`, `.markdown`, and conversation-export `.json` (ChatGPT or Claude `conversations.json`, or a `{role, content}` list) |
| Link | `POST .../sources:import` | Public web pages, text, Markdown and PDF links |
| Share link | `POST .../sources:import` | `chatgpt.com/share/…`, `chat.openai.com/share/…`, `claude.ai/share/…`, `gemini.google.com/share/…`, `g.co/gemini/share/…` |
| Paste | `POST .../sources:paste` | A transcript or other text, up to 200,000 characters: the fallback for share links that cannot be read. A link refused for safety (SSRF) gets no paste offer, but the Paste tab stays available |

**Share links are best effort.** A share page is imported only when it embeds the conversation as data (for example ChatGPT's `__NEXT_DATA__`). Pages that render in the browser fail with `SHARE_NOT_READABLE`, and the reason names the fallback. Private conversation links (`/c/…`, `/chat/…`, `/app/…`) are refused before any request, with `PRIVATE_CONVERSATION_URL`. A sign-in redirect, 401 or 403 gives `SHARE_REQUIRES_SIGN_IN`, and 404 or 410 gives `SHARE_NOT_FOUND`. MASD never signs in to a provider, calls a private API, sends cookies or stores credentials.

**Security controls.**

| Control | Implementation |
|---|---|
| Type and signature | Allow-listed extension, a compatible declared media type, and matching content: `%PDF-` in the first 1 KB for PDFs; text must decode as UTF-8 (or UTF-16 with a BOM) with no binary signature or NUL bytes |
| Size limits | `MASD_UPLOAD_MAX_BYTES` (10 MiB by default, ceiling 25 MiB), enforced in the HTTP middleware and the route; `MASD_SOURCE_MAX_CHARS` (1,000,000) and `MASD_PDF_MAX_PAGES` (500) after extraction. nginx accepts 26 MB on the upload route only |
| Safe parsing | Every parser (pypdf, HTML, JSON exports, share pages) runs in a child process (`python -m project_service.extract`), with no service environment or secrets, 1 GiB address space and CPU rlimits on POSIX, a `MASD_EXTRACT_TIMEOUT` kill (30 s), and at most two at a time. Only extracted text and the SHA-256 of the original are stored |
| Encrypted and scanned PDFs | Refused with `ENCRYPTED_PDF` and `NO_TEXT`. There is no OCR and no password prompt |
| SSRF | http(s) on ports 80 and 443 only; no credentials in the URL; every resolved address must be public (`is_global`; private, loopback, link-local metadata, CGNAT, ULA and IPv4-mapped addresses are refused); the connection is pinned to the vetted address (Host and SNI keep the name, which defeats DNS rebinding); every redirect is re-checked, up to 5; total deadline `MASD_IMPORT_TIMEOUT` (20 s); the decoded body is capped while streaming; no proxy environment, cookies or auth headers |
| Malware scanning | `MASD_MALWARE_SCANNER=clamav` streams every document to clamd `INSTREAM` before parsing, and fails closed (503 `SCAN_UNAVAILABLE`). The default `none` is shown on every source as "not malware-scanned" |
| Prompt-injection boundary | Source text never enters the privileged system message. It is sent at the start of the current user turn, after a preamble that it is untrusted data to use as information and never to obey, inside `<source-{tag}>` markers with a random per-turn tag that content cannot forge. This is defense in depth, not a guarantee: a model can still be steered by injected text, so a response that used sources stays an AI response until a human reviews and promotes it (B8). Tests assert the structure (no source text in the system message, one unforgeable block); model behaviour against adversarial sources is part of the B9 live-provider smoke test |
| Isolation | Owner and tenant are checked on the project for every route; sources are read only through their project; another project's source cannot be attached (422); archived projects refuse new sources |
| Audit | `source_events` records every upload, import, paste, delete, expiry and refusal (actor, tenant, outcome code, file name or host; never content), and the same events are logged as JSON |
| Retention | `MASD_SOURCE_RETENTION_DAYS` (90). Purged at startup and hourly. Delete and expiry remove the text and keep metadata and the hash |
| Rate limit | 20 source requests a minute per user |

**Long sources (R5): explicit, never silent.** Text is split into sections of about 1,200 characters on paragraph boundaries; PDF sections keep their page numbers. A message attaches up to five ready sources.
- **Sources that fit the remaining context budget** are sent whole.
- **Sources that do not fit:** each source's opening section is sent, then the sections most relevant to the message (BM25), in document order, with a gap marker between them.
- **Budget.** Attached sources get the room left after the system text and the message. When the conversation has earlier turns, they get at most three quarters of it, so history keeps a share.
- **No room.** If no section fits, the message is refused with 422 and the reason.
- **Traceability.** Each turn stores `source_refs`: source ID, title, hash, strategy (`full`, `excerpts` or `omitted`), the sections and pages sent, and the characters sent out of the total. `MessageView.sources` returns them, and the UI shows them under "Sources used", including after the source is deleted. Regeneration re-selects the same sources for the chosen model, or refuses if one was deleted.

**Contracts.** Project Service 0.10.0 is additive: five source routes, `SubmitMessage.source_ids`, `MessageView.sources` and the required `Capabilities.sources`. `pre_b7` keeps 0.9.0 and every earlier document byte-identical. Migration `0010_sources` is additive: three tables, plus `turns.source_refs` as a plain `ADD COLUMN`, so SQLite keeps the turn constraints.

**Web.** A Sources panel in the AI Workspace has three tabs: Upload file (real upload progress), Import link (with each provider's share-link note) and Paste transcript (with a counter).
- **Limits and formats** come from `/capabilities`. Type, size and emptiness are checked before any bytes are sent.
- **Refusals** show the server's reason and code. Share-link refusals offer "Paste transcript instead", prefilled with the provider; SSRF refusals do not.
- **Retries** of the same file, link or text reuse the idempotency key.
- **Attaching.** A new source is attached automatically while there is room; attachments stay for follow-up messages and are dropped when a source stops being ready.
- **Deleting** takes two steps and keeps the metadata.

**Not supported (documented limitations).** DOCX and other office formats, OCR for scanned PDFs, password-protected PDFs, saved HTML files as uploads, and Gemini exports (Gemini has none). Share pages that render client-side need Paste. The stack ships no ClamAV container: its daemon needs a writable signature store and privileges that the read-only, capability-dropped services forbid, so `clamd` runs separately.

### B7 evidence (2026-11-26, branch heads)

| Check | Result |
|---|---|
| contracts `scripts.check` | 114 passed (7 new); 0.10.0 validates; 0.9.0 and earlier untouched |
| project-service `scripts.check` / real PostgreSQL 17 | 341 passed / 7 skipped; **348 passed, 0 skipped** (65 new: types and signatures, encrypted, scanned and damaged PDFs, parser isolation and timeout, owner and project isolation, rate limit, CSRF, clamd scanning, 12 SSRF destinations, redirect re-checks and pinning, size caps, share-link outcomes, paste, delimiting, excerpts within budget, no-room refusal, delete, regeneration, retention, migration, contract) |
| web `scripts.check` (from `C:\`) | 233 Angular tests (+29), lint, typecheck, build (initial bundle 385.6 kB), audit 0 |
| infrastructure `scripts.check` | 90 passed (+1 POSIX-only skip) |
| Stack | Rebuilt `masd-m2`. Project Service became ready on its live PostgreSQL database after migration `0010_sources` |
| Chromium, rebuilt `masd-m2` stack | **12/12**. The new journey uploads a PDF with progress and attaches it; the message records "whole text"; a renamed non-PDF is refused (`SIGNATURE_MISMATCH`) and so is an `.exe` (in the browser); a metadata-address link is refused (`URL_BLOCKED`, with no paste offer); a private ChatGPT link is refused (`PRIVATE_CONVERSATION_URL`) and the prefilled paste fallback saves a transcript; a direct API call gets 415; after delete and reload the message still names its source |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS |
| Live share-link imports | Not run: deterministic tests use an in-memory site, and real ChatGPT, Claude and Gemini pages vary and may block automated access |

#### B7 review round 1 (48 Sourcery findings: project-service 20, web 13, contracts 10, central 4, infrastructure 1)

Fixed with regression tests:
- **Project Service:**
  - **Uploads:** the body is read only after sign-in, streamed with the cap, and refused with `TOO_LARGE`, which is audited. The file name moves to the `X-Source-Filename` header, so it stays out of URLs and logs.
  - **Parser:** its output is bounded in the service, PDF extraction stops at the text limit, and a cancelled request kills its parser before the slot is released.
  - **Model boundary:** source text is no longer in the system message; it opens the current user turn.
  - **Retries and quota:** concurrent identical retries replay. The quota is checked before validation; rate-limit and key-conflict refusals are audited; inactive users are pruned.
  - **Links:** malformed hosts get `URL_INVALID`, and stored links drop their query string.
  - **Pastes:** the exact text is kept. Pastes that are empty after cleaning or over the text limit are refused, and the body limit fits JSON escapes.
  - **Consistency:** attached sources take shared row locks and delete takes an exclusive one. Expiry events are recorded only for rows actually changed. The database constrains format and provider.
- **Contracts (0.10.0, re-exported):** excerpt `maxLength`, `uniqueItems` on `source_ids`, `date-time` timestamps, the `SourceRef` hash pattern and non-negative sections, JSON exports documented as raw bytes, and the retry and conflict rules. The additivity test now also checks that every previously required field stays required.
- **Web:**
  - Panel state is scoped to the project, and paste keys are bound to the whole payload.
  - List snapshots merge sources added meanwhile, and every page is loaded.
  - Nothing is attached automatically until the limit is known.
  - Attachments are re-checked before sending.
  - Deletes are blocked while a message is being sent and reconciled when unanswered.
  - Uploads and deletes have timeouts.
  - The source-use note names the sections and pages, and the progress display has a test.
- **Docs:** enabling scanning needs both settings. The paste fallback excludes SSRF refusals, the PR links are added, and the delimiters are described as defense in depth.

Answered without a code change, with the reasons in each thread:
- Process-local limits and exact-revision readiness: Project Service is single-replica, and upgrades are stop, migrate, start.
- `MessageView.sources` stays optional-with-default, like the B6 fields.
- Offset paging: the web client follows the pages and drops duplicates.
- Malware scanning is off by default but stays visible.
- An e2e test cannot observe server egress; the no-request guarantee is asserted in the Project Service tests.

| Check after round 1 | Result |
|---|---|
| contracts / infrastructure | 115 / 90 passed |
| project-service, SQLite / real PostgreSQL 17 | 355 passed, 7 skipped / **362 passed, 0 skipped** |
| web (from `C:\`) | 242 Angular tests, lint, typecheck, build (initial 385.6 kB), audit 0 |
| Chromium, rebuilt `masd-m2` stack | 12/12 |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS |
| Review after round 1 | All 48 threads answered and resolved. On the round-1 heads (contracts `8332dcd`, project-service `431291d`, web `dccb6c3`, infrastructure `c2d2b30`, central `2b682c6`), CI `validate` passed and Sourcery re-ran with no new findings |

Found during verification: the rebuild re-created Keycloak, and its imported test realm gave the same usernames new subject IDs. Project Service then correctly refused them (`identity_conflict`, B4). The two dev-stack bindings were cleared so the test accounts could bind again. Also, the dev database was already at `0010_sources` before round 1, so it lacks the two CHECK constraints added to that unreleased migration; fresh databases get them.
