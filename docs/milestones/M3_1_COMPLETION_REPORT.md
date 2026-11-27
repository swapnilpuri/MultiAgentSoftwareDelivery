# M3.1 completion report: UX, rich AI responses, unified auth, multi-provider models and workflow reliability

## Status

**READY_FOR_HUMAN_ACCEPTANCE.** All ten requirements are implemented in batches B1–B9. The Required Acceptance Scenario passes end to end on the rebuilt stack with deterministic mock providers, and the final regression passes. Steps 10 and 11 were observed with the generation already finished; the running state is covered by tests (section 11). The owner's manual verification and M3.1 acceptance are the remaining human actions. **M4 has not started.**

Requirements: [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md). Plan, designs and per-batch evidence: [M3_1_IMPLEMENTATION_PLAN.md](M3_1_IMPLEMENTATION_PLAN.md). Merge status: [M3_1_HANDOFF.md](M3_1_HANDOFF.md).

## 1. Root cause of the Generate PRD freeze

Three defects compounded (plan §2):
1. **Execution was tied to the HTTP stream.** When the response ended, its `finally:` cancelled the generation task, and the operation was marked `failed`. The response ended on a client abort, the 250 s client timer, nginx's 240 s read timeout, a reload or a network drop.
2. **The same-key replay was a dead end.** A replay of a failed key returned "running or interrupted; reload before explicit retry" for ever, and no failure reason was stored.
3. **The client locked itself.** After a non-4xx failure, Requirements Studio kept a pending record in session storage. That record refused every action, blocked navigation, prompted on reload, and resent the dead key. It was restored after every reload.

**Fix (B1–B3).** Generation is a server-owned operation with real stages and failure reasons. Requests only observe it. A failed operation is retried explicitly with a new key. Startup and shutdown record `INTERRUPTED`. The studios never lock navigation. Section 6 describes the design.

## 2. Changes by repository

| Repository | Changes |
|---|---|
| masd-contracts | Project Service 0.5.0–0.11.0 and llm-gateway 0.3.0–0.4.0. 0.7.0 is the only non-additive version: workspace routes require the session. Every earlier document stays byte-identical. Contract tests pin each version |
| masd-project-service | Durable requirements and architecture operations, and the project operations list (B1, B3). OIDC backend-for-frontend, owner and tenant checks, and principal binding (B4). The capabilities endpoint and enforced limits (B5). Profiles and response versions (B6). Sources: upload, link import, paste, extraction and security controls (B7). Promotions and Markdown artifacts with review (B8). Migrations `0005`–`0011`, all additive. B9 adds README sections for operations, sources and promotions |
| masd-web | Non-blocking studios and the operation panel (B2). The Operations page (B3). The six-section shell and one sign-in (B4). Character counters and model limits (B5). The rich AI Workspace (B6). The Sources panel (B7). The Promote dialog, the Artifacts page and the lineage views (B8). B9 adds the acceptance journey and one fix: the Promote dialog opens a PRD on its generation |
| masd-llm-gateway | Gemini and OpenAI-compatible providers, verified availability, and provider status (B5). Idle and total timeouts instead of short caps, and larger output budgets (B6) |
| masd-infrastructure | Durable-operation wiring (B1, B3). Keycloak on the web origin, SSO accounts and configuration (B4). Provider keys (B5). Long-answer settings (B6). The upload body limit and source settings (B7) |
| MultiAgentSoftwareDelivery | Requirements, plan, designs, evidence and handoff. The runtime-secrets scan covers the B4 secrets and the provider keys. This report |

## 3. Updated UI workflows

- **Shell.** Six sections: AI Workspace, Requirements Studio, Architecture Studio, Delivery / Milestones, Operations / Activity, and Administration / Settings. The shell also has a remembered project context, breadcrumbs, per-section help, loading and error states, a responsive menu, and a running-operations status in the header.
- **AI Workspace.**
  - Model and response-profile pickers, with the selected model's limits shown and a live counter of characters used and remaining.
  - Rich answers: sections, tables, code and sandboxed Mermaid diagrams.
  - Copy, Save as Markdown, Regenerate (as a new version), and a version navigator.
  - A Sources panel, and Promote.
- **Promotion.** A response, or chosen sections of it, becomes a draft PRD (Requirements Studio) or a Markdown artifact (Artifacts page) that is revised, reviewed and approved. Lineage is shown in Requirements Studio, Architecture Studio and on each artifact.
- **Operations.** Generation keeps running while the user navigates. Operations / Activity lists each operation's status, stage, reason, cancel and retry. A studio re-attaches after a reload.

The component READMEs document each workflow: masd-web "M3.1 user workflows", and the project-service M3.1 sections.

## 4. Provider integrations and configuration

The providers are `openai`, `anthropic`, `gemini`, `openai_compatible`, `ollama`, and `test` (deterministic, for verification only), all through LiteLLM in llm-gateway.
- **Configuration.** Models are configured explicitly in `MASD_MODELS`.
- **Credentials.** Provider keys come only from the gateway environment (`.env.m2`; see the infrastructure README). They are sent only in request headers and never reach the browser or Project Service. The OpenAI-compatible endpoint has its own key.
- **Availability is verified, not assumed.** A model is available only when its provider answers and lists it. Otherwise it shows a reason code.
- **Where status is shown.** `GET /api/v1/providers` and `GET /api/v1/capabilities` report provider status without URLs or keys. Settings and the AI Workspace show it.
- Details: llm-gateway README (B5, B6) and the plan's "B5 design".

## 5. Supported import methods and limitations

| Method | Supported |
|---|---|
| Upload | PDF with a text layer, `.txt`, `.md`, `.markdown`, ChatGPT and Claude `conversations.json`, or a `{role, content}` list. Up to 10 MiB by default (`MASD_UPLOAD_MAX_BYTES`, at most 25 MiB), 500 PDF pages, and 1,000,000 extracted characters |
| Link | Public web pages, text, Markdown and PDF links |
| Share link | ChatGPT, Claude and Gemini share links, best effort: only pages that embed the conversation as data |
| Paste | A transcript or other text, up to 200,000 characters. This is the fallback for unreadable share links |

**Limitations.**
- **Formats.** No DOCX or other office formats, no OCR for scanned PDFs, no password-protected PDFs, and no Gemini exports (Gemini offers none). Share pages that render only in the browser need Paste.
- **Malware scanning** is off by default, and each source is labelled "not malware-scanned". `clamd` runs outside the stack.
- **Long sources** are never cut silently. A source that does not fit is sent as its opening section plus the most relevant sections, and the turn records exactly what it sent.
- **Text limits** come from `GET /api/v1/capabilities`. Over-limit text is refused with a 422 that names both numbers, never truncated.

## 6. Operation persistence and recovery design

The design is in plan §2a and the project-service README.
- **States.** `running`, then exactly one of `completed`, `failed` or `cancelled`. The `stage` field shows real progress (`queued`, `generating`, `validating`), never a percentage.
- **Failure reasons.** Every failure records an `error_code` and a `failure_reason`, such as `INTERRUPTED`, `CANCELLED`, `COMMIT_FAILED` or a provider code.
- **Ownership.** An app-owned task runs the operation with its own database session, so losing an observer never cancels the work.
- **Replays.** A same-key replay attaches to the operation or returns its stored result. Retrying needs a new key.
- **Exclusive outcome.** Completion and cancellation cannot both win: each takes the session row under a lock and checks `active_operation_id`.
- **Restarts.** Startup and shutdown mark running operations `INTERRUPTED`. Upgrades follow stop → migrate → start, because Project Service is single-replica.
- **Promoted PRDs.** The PRD's generation key derives from the promotion key, so a retried promotion never starts a second generation.

## 7. Authentication changes

There is one application login: OIDC authorization code with PKCE, through Keycloak served on the web origin at `/auth`. Project Service completes the flow as a backend-for-frontend, so no token reaches the browser, only an httpOnly session cookie.
- **Studio logins removed.** The studios' own login forms are gone, and the AI Workspace now runs as the human principal.
- **Roles and tenant.** Sign-in requires `masd-user` and approval requires `masd-approver`. Project access checks both the owner and the tenant (`masd_tenant`). Each username is bound to its provider subject on first sign-in.
- **Session.** Renewal is sliding and re-checks roles every 5 minutes. A session expires after 30 minutes idle, with a 10-hour absolute limit. Sign-out is central and also ends the Keycloak session.
- **Password sign-in** exists only without OIDC (unit tests and `ng serve`).

## 8. Automated test results (final regression, B9)

Tested revisions:

| Repository | Revision |
|---|---|
| masd-web | `97a5459` (B9 PR head) |
| masd-project-service | `9982e26` (B9 PR head) |
| MultiAgentSoftwareDelivery | `docs/m3.1-acceptance` (the B9 PR) |
| masd-contracts | `main` `ccbe920` |
| masd-llm-gateway | `main` `4704e39` |
| masd-agent-service | `main` `bb851aa` |
| masd-infrastructure | `main` `9d93152` |

Review round 1 then changed only the acceptance spec's assertions (web `910d78d`, where both acceptance tests passed again on the same stack) and documentation (project-service `0ac72d6`, central).

The commands, run on Windows from each repository root, are:
- **Gates:** `uv run --frozen python -m scripts.check`, with masd-web run from an uppercase `C:\` path.
- **Real PostgreSQL 17:** `uv run --frozen pytest -q` in masd-project-service, with `MASD_TEST_DATABASE_URL` pointing at a throwaway `postgres:17` container that has a one-off password.
- **Stack:** `uv run --frozen python -m scripts.m2_compose up --build --wait` in masd-infrastructure.
- **Chromium:** `npx playwright test` in masd-web. Set `INTEGRATION_BASE_URL=http://127.0.0.1:4400`, set `M2_HUMAN_LOGIN_FILE` and `M31_SSO_USERS_FILE` to the files in infrastructure `artifacts/`, and set `M2_ACCEPTANCE_RECORD`, `M3_ACCEPTANCE_RECORD` and `M31_ACCEPTANCE_RECORD`.
- **Restart verifiers:** `uv run --frozen python -m scripts.verify_m2_restart --record artifacts/m2-acceptance-record.json` and `uv run --frozen python -m scripts.verify_m3_restart --record artifacts/m3-acceptance-record.json`, both in masd-infrastructure.
- **Runtime secrets:** `uv run --frozen python -m scripts.verify_m2 runtime-secrets` in the central repository.

| Check | Result |
|---|---|
| masd-contracts `scripts.check` | 122 passed |
| masd-llm-gateway `scripts.check` | 127 passed |
| masd-project-service `scripts.check` / real PostgreSQL 17 | 379 passed, 7 skipped (PostgreSQL-only) / **386 passed, 0 skipped** |
| masd-agent-service `scripts.check` | 103 passed |
| masd-infrastructure `scripts.check` | 90 passed (+1 POSIX-only skip) |
| masd-web `scripts.check` (from `C:\`) | 274 Angular tests, lint, typecheck, build (initial 386.8 kB), audit 0 |
| central `scripts.check` | 46 passed |
| Chromium, `masd-m2` stack rebuilt from the B9 heads | **15/15**: the M1–M3 journeys, the M3.1 unified-auth, rich-workspace, sources and promotion journeys, and the two B9 acceptance tests |
| `verify_m2_restart` / `verify_m3_restart` / `verify_m2 runtime-secrets` | PASS / PASS / PASS |

R10 coverage, by area:
- **Navigation and login:** B4 unit tests, plus the unified-auth journey.
- **Role and tenant checks:** reviewer, outsider and tenant tests.
- **Counters and upload limits:** B5 and B7.
- **PDF ingestion:** B7.
- **Conversation URLs:** B7 share-link outcomes and SSRF tests.
- **Providers:** gateway B5 tests.
- **Rich rendering:** B6.
- **Promotion:** B8.
- **PRD generation success and failure:** B1, and the B9 recovery test.
- **Duplicate submissions:** idempotency tests in every batch.
- **Interrupted recovery:** B1/B3, `verify_m2_restart` and `verify_m3_restart`.
- **Refresh during generation:** B2 and B9.
- **Cancel and retry:** B1–B3.
- **Long responses and documents:** the B6 100,000-character render test and the B7 excerpt budget.
- **Security controls:** B4, B5 and B7.
- **Contract tests:** every independently deployed service.

## 9. Security and review results

- **Reviews.** Sourcery reviewed every head of every PR. Every finding was answered, and fixed with a regression test where it applied. The B1–B2 round had 34 findings, B4 37, B5 33, B6 39, B7 48 and B8 28. A few were answered without a code change, with the reason in the thread (plan, each batch's review section). **No review thread is left unresolved, and no high-severity finding is open.**
- **Upload and link import.** Type and signature checks, isolated parsing, size caps, an SSRF guard with address pinning and redirect re-checks, untrusted-content delimiting, an audit trail and retention.
- **Credentials.** Provider keys stay in the gateway environment, and no token reaches the browser. `verify_m2 runtime-secrets` scans every service log, including Keycloak's, for the B4 secrets and the provider keys.
- **Dependency audits** are clean (`npm audit` 0, and the Python audits in each `scripts.check`).

## 10. PR and merge links

| Batch | contracts | project-service | web | infrastructure | llm-gateway | central |
|---|---|---|---|---|---|---|
| Plan | — | — | — | — | — | [#13](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/13) `4846b29` |
| B1/B2 | [#6](https://github.com/swapnilpuri/masd-contracts/pull/6) `9029150` | [#6](https://github.com/swapnilpuri/masd-project-service/pull/6) `ead2c0f` | [#7](https://github.com/swapnilpuri/masd-web/pull/7) `fdfbc13` | [#7](https://github.com/swapnilpuri/masd-infrastructure/pull/7) `7fba040` | — | — |
| B3 | [#7](https://github.com/swapnilpuri/masd-contracts/pull/7) `2b428bd` | [#7](https://github.com/swapnilpuri/masd-project-service/pull/7) `2665234` | [#8](https://github.com/swapnilpuri/masd-web/pull/8) `4d334c6` | [#8](https://github.com/swapnilpuri/masd-infrastructure/pull/8) `b7bab9b` | — | [#14](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/14) `c4b1fa6` |
| B4 | [#8](https://github.com/swapnilpuri/masd-contracts/pull/8) `0bb590f` | [#8](https://github.com/swapnilpuri/masd-project-service/pull/8) `586e7a6` | [#9](https://github.com/swapnilpuri/masd-web/pull/9) `5aaefaa` | [#9](https://github.com/swapnilpuri/masd-infrastructure/pull/9) `9faad49` | — | [#15](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/15) `4acd6d0` |
| B5 | [#9](https://github.com/swapnilpuri/masd-contracts/pull/9) `96dfd00` | [#9](https://github.com/swapnilpuri/masd-project-service/pull/9) `c2985b5` | [#10](https://github.com/swapnilpuri/masd-web/pull/10) `0570e3a` | [#10](https://github.com/swapnilpuri/masd-infrastructure/pull/10) `8db43be` | [#4](https://github.com/swapnilpuri/masd-llm-gateway/pull/4) `8801f16` | [#17](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/17) `d596db6` |
| B6 | [#10](https://github.com/swapnilpuri/masd-contracts/pull/10) `4dcbdcd` | [#10](https://github.com/swapnilpuri/masd-project-service/pull/10) `2dcc88d` | [#11](https://github.com/swapnilpuri/masd-web/pull/11) `1c31f5a` | [#11](https://github.com/swapnilpuri/masd-infrastructure/pull/11) `20f5b77` | [#5](https://github.com/swapnilpuri/masd-llm-gateway/pull/5) `4704e39` | [#19](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/19) `d486376` |
| B7 | [#11](https://github.com/swapnilpuri/masd-contracts/pull/11) `1ebe098` | [#11](https://github.com/swapnilpuri/masd-project-service/pull/11) `e500d59` | [#12](https://github.com/swapnilpuri/masd-web/pull/12) `842a531` | [#12](https://github.com/swapnilpuri/masd-infrastructure/pull/12) `9d93152` | — | [#21](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/21) `ee7afa2` |
| B8 | [#12](https://github.com/swapnilpuri/masd-contracts/pull/12) `ccbe920` | [#12](https://github.com/swapnilpuri/masd-project-service/pull/12) `97c3192` | [#13](https://github.com/swapnilpuri/masd-web/pull/13) `4367bdb` | — | — | [#23](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/23) `0763029` |
| B9 | — | [#13](https://github.com/swapnilpuri/masd-project-service/pull/13) | [#14](https://github.com/swapnilpuri/masd-web/pull/14) | — | — | [#25](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/25) |

Merged rows give each PR and its merge commit; the B9 row lists open PRs only. Central #16, #18, #20, #22 and #24 recorded the merges. Every merge was made on the owner's explicit instruction, pinned to the verified head commit. The B9 PRs are open for review.

## 11. Acceptance scenario results

The Required Acceptance Scenario is automated as `masd-web/e2e/m31-acceptance.spec.ts`. It ran in Chromium against the `masd-m2` stack rebuilt from the B9 heads, with real Keycloak, PostgreSQL 17, Project Service, Agent service and llm-gateway, and with deterministic mock models. The owner's `HRMSSystem.pdf` is not in Git, so the test builds a comparable four-page HRMS design PDF. It sends that PDF together with a detailed, structured HRMS design prompt; step 3 allows either.

| Step | Result | Evidence |
|---|---|---|
| 1. Sign in once | PASS | Keycloak form, then the shell |
| 2. Create an HRMS project | PASS | "HRMS acceptance …" project |
| 3. Upload `HRMSSystem.pdf` and a detailed prompt | PASS | "PDF upload · 4 pages", attached; "Sources used: HRMSSystem.pdf: whole text" |
| 4. Select a configured model | PASS | `test/deterministic`, with its limits shown |
| 5. Input limits and remaining characters | PASS | Counter: "661 / 3,398 characters · 2,737 remaining". The model's limits are shown next to the picker |
| 6. Comprehensive structured response | PASS | Comprehensive profile, saved |
| 7. Rich content renders | PASS | Four collapsible sections, a three-row table, and a Mermaid SVG in an empty-sandbox frame |
| 8. Save the response | PASS | Stored on the server; Save as Markdown downloads `…-v1.md` |
| 9. Promote selected content into a draft PRD | PASS | Sections Vision and Requirements become a Requirements Studio session, with its lineage shown |
| 10. Progress visible while navigating | PASS for the finished state | The operation panel shows the generation at once, and Operations / Activity lists it after navigating away. With the deterministic model the generation had already completed, so no running stage was observed. The running state is covered by the B1–B3 service and unit tests (section 12) |
| 11. Refresh and still inspect the operation | PASS for the finished state | Operations / Activity after a reload, and the studio's operation panel after a second reload. Re-attaching to a still-running operation after a reload is covered by B2's web unit tests and the B1 disconnect test, not by this run |
| 12. Completes, or a recoverable error without freezing | PASS (both) | It completes. A second test fails a PRD generation on purpose: the reason and "Retry with a new request" are shown, navigation works, and the failure survives a reload |
| 13. Open, review and approve the PRD | PASS | Stories generated, submitted, approved; "Approved requirements baseline" |
| 14. Approved PRD traceably feeds Architecture Studio | PASS | The architecture session is bound to the approved PRD and shows "Source PRD traceability: promoted from the AI Workspace", with the conversation, response version and hash, sections and source. "Approved revision and hash match this session's source" |
| 15. One application login | PASS | Exactly one identity-provider credential submission in the whole journey; no studio sign-in |

**Found and fixed by the acceptance run.** When a promoted PRD's generation failed before Requirements Studio opened, the studio showed the session without the failure: no reason and no retry. The Promote dialog now opens the session with `?operation=<id>`, the same mechanism the Operations page uses. The studio then follows that exact operation, including one that has already finished. The fix has a unit test, and the B8 promotion journey is updated for the new URL.

**Live-provider smoke test:** not run. No provider credentials were supplied; it remains optional and owner-triggered.

## 12. Remaining limitations

- **Running state not observed live.** With the deterministic fixture, PRD generation finishes in about a second, so the running state is usually over before the user navigates; the journey saw the operation already `completed`. The panel and the Operations listing are the same for a running operation. Running-state behaviour is covered by the B1–B3 service and unit tests, and by `verify_m2_restart` and `verify_m3_restart`, which interrupt a running operation. A live provider would show the stages for longer.
- **Live checks not run.** The live-provider smoke test was not run, and neither were live share-link imports, which depend on third-party pages.
- **Formats.** DOCX and other office formats, OCR for scanned PDFs, password-protected PDFs and Gemini exports are not supported. Share pages that render only in the browser need Paste.
- **Malware scanning** is off by default.
- **Artifact studios.** Promoted artifacts other than PRDs have no downstream studio yet.
- **Single-replica Project Service.** Rolling upgrades are not supported.
- **Cosmetic issues:**
  - The lineage list runs its labels into its values ("SourcesHRMSSystem.pdf").
  - A promoted PRD's description shows its raw Markdown heading in pickers.
  - On narrow screens, a breadcrumb separator can start a wrapped line (since B4).
- **Stack rebuilds.** The web container's nginx resolves Project Service only at startup. A rebuild that recreates Project Service without the web container gives 502s until the web container restarts. This happened once during the B9 run: the first browser pass failed 15/15 with 502s, and passed 15/15 after `docker restart masd-m2-web-1`.
- **Rate limit in repeated runs.** Back-to-back repeated generation-heavy browser runs can hit the gateway's local limit of 30 requests per minute (test environment only).
