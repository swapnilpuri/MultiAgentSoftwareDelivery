# M2 implementation acceptance candidate

Status: implementation and local acceptance complete; review/final CI reconciliation pending. **M3 NOT READY.**

27 PASS / 0 FAIL / 2 BLOCKED / 0 NOT_EXECUTED, out of 29. The blocked gates are AC-26 (required review completion) and AC-27 (all final-head CI). Approval/merge and post-merge main verification are still human-gated.

Evidence keys, exact source matrix and limitations: [current report](M2_FINAL_VERIFICATION_REPORT.md). Automated browser approval uses an isolated password-authenticated test-human principal; it is not a human milestone acceptance.

| ID | Requirement (unchanged) | Implementation | Actual verification | Status | Evidence / limit |
| --- | --- | --- | --- | --- | --- |
| AC-01 | Existing M0/M1 architecture and standards are preserved. | ADR 0001–0005; seven manifests; independent Dockerfiles | T1/T7, M1 contract and browser regression | PASS | Standards/service boundaries preserved; existing M0/M1 environment and history retained. |
| AC-02 | PM Agent is implemented in its approved service boundary. | Agent Service agent_service/main.py, LangGraph StateGraph | tests/test_pm.py::test_graph_discovery_prd_stories_quality_and_no_tools; T3 | PASS | Executable authenticated prepare → Gateway → validate/retry graph; no tools or approval API. |
| AC-03 | PM Agent uses the existing LLM Gateway. | Agent Service agent_service/gateway.py; Gateway llm_gateway/main.py | T3 actual service chain; Gateway test_litellm_adapter_routing and test_structured_fixture_is_explicitly_enabled_and_labeled | PASS | PM calls existing Gateway; commercial/Ollama SDK tests mocked; integrated route explicitly test/structured. |
| AC-04 | Requirements discovery is available through Angular. | web navigation.ts, app.routes.ts, project-detail.ts, requirements-studio.* | T3 foundation and m2-requirements.spec.ts | PASS | Normal navigation and project link reach the same Angular shell. |
| AC-05 | Users can respond to clarification questions. | Project requirements.py answer handler; web requirements-studio.html | T2 test_discovery_revisions_review_and_immutable_baseline; T3 | PASS | Answered/deferred questions are persisted; missing decisions remain visible. |
| AC-06 | Discovery state persists across application restarts. | requirements_sessions, requirement_operations and requirement_history; migrations 0002/0003 | T2 test_checkpoint_and_approval_recovery_after_application_restart, test_all_conversation_activity_survives_bounded_agent_context; T4 | PASS | Actual container/database restart and interrupted operation recovery; complete history stored apart from last-30 context. |
| AC-07 | Structured PRD generation works. | Agent schema.py/fixtures.py/main.py; Project requirements_schema.py | Agent test_graph_discovery_prd_stories_quality_and_no_tools, test_bounded_invalid_output_retries; T3 | PASS | All 19 typed sections; output validated twice; bounded parsing retries. |
| AC-08 | PRD sections are editable. | web requirements-studio.html; Project save command | Angular requirements-studio.spec.ts; T3 editor/save/reload | PASS | Structured section/requirement/story/criterion edits create saved revisions; Markdown derived one-way. |
| AC-09 | PRD revisions are persisted and distinguishable. | requirement_revisions; append_revision; immutable database triggers | T2 test_discovery_revisions_review_and_immutable_baseline; T3/T4 | PASS | Revision number/parent/hash/author/time persisted; unique session sequence. |
| AC-10 | Epics and user stories can be generated. | Agent PM stories workflow; Document epic/story models; Angular hierarchy | Agent test_graph_discovery_prd_stories_quality_and_no_tools; T3 | PASS | Epics/stories generated through Gateway and shown with criteria and links. |
| AC-11 | Stories trace to requirements. | Document.consistent; stable requirement/epic/story IDs and references | T2 test_structured_document_rejects_invalid_graphs; T3 | PASS | Broken references/hierarchy and duplicate IDs rejected; revisions preserve requirement IDs. |
| AC-12 | Acceptance criteria are structured and testable. | Criterion Given/When/Then models; story criteria min length | T2 test_structured_document_rejects_invalid_graphs; T3 criteria rendering | PASS | Structured nonempty criteria; human review remains necessary for business adequacy. |
| AC-13 | Requirements quality validation executes. | requirements_schema.py quality; Agent quality instructions; findings dispositions | T2 test_quality_findings_are_visible_and_rejectable, test_post_draft_questions_do_not_change_review_state_and_findings_keep_human_disposition; T3 | PASS | Deterministic missing/ambiguity/duplicate/coverage/open-question findings plus validated AI proposals; dispositions stay human-controlled. |
| AC-14 | Unresolved assumptions and questions remain visible. | Question/deferred/provenance/assumptions fields and Studio panels | T2 discovery/deferral; T3 visible unresolved questions and assumptions | PASS | No inferred business decisions or automatic human confirmation from agent output. |
| AC-15 | The approval workflow supports approved/rejected/changes-requested decisions. | Project submit/decide handlers; human_auth.py; approval history UI | T2 test_negative_review_decisions_are_audited; T3 changes requested → revise → resubmit → approve | PASS | All three decisions persist identity/revision/hash/scope/comments/time. |
| AC-16 | Approved artifact versions are immutable. | PostgreSQL and SQLite history triggers; revision/baseline endpoints | T2 raw UPDATE/DELETE rejection; T3 PUT revision=405 and new-draft baseline preservation; T4 | PASS | No update endpoint; approved content/history remain unchanged after edits and restarts. |
| AC-17 | Stale approval attempts are rejected. | Session version lock, revision binding and expected content hash | T2 test_stale_hash_invalid_document_and_no_self_approval, test_postgres_serializes_competing_mutations; T3 stale decision=409 | PASS | Stale/hash-mismatched decisions rejected transactionally. |
| AC-18 | PM Agent cannot approve its own output. | Human cookies, reviewer permission, agent-only backend token; independent provenance enforcement | T2 test_human_security_boundaries, test_agent_cannot_self_confirm_new_requirements_or_findings; Agent no-approval route test | PASS | Service account login rejected; agent credentials cannot decide; new agent facts/findings remain proposals. |
| AC-19 | Project access boundaries are enforced to the extent supported by the authenticated runtime. | human_auth.py; requirements.py project_access on every nested route | T2 ownership/cross-project/logout/CSRF/expiry tests; T3 unauthorized baseline=401 | PASS | M2 requires password-verified human owner. Development only; production startup refused. |
| AC-20 | Version comparison works. | ComparisonView, compare endpoint; Angular before/after tables | T2 revision comparison assertions; T3 | PASS | Adds/removes/changes and before/after all stored PRD fields plus changed/removed/impacted story IDs. |
| AC-21 | API contracts are published and validated. | contracts 0.3.0 OpenAPI/JSON/SSE candidates and consumer snapshots | T1 contracts/test_m2_contracts.py; Project test_m1_contract.py and test_m2_contract.py | PASS | Five OpenAPI documents validate; immutable M1 paths/DTOs unchanged; actual M2 SSE envelopes validate. |
| AC-22 | Unit, integration, and applicable frontend tests pass. | Seven independently configured test suites; Angular and browser specs | T1/T2/T3/T4 | PASS | 258 distinct Python tests covered, 24 Angular tests, four integrated Chromium scenarios; no live-provider claim. |
| AC-23 | The full deterministic end-to-end discovery-to-approval workflow is verified. | Full e2e/m2-requirements.spec.ts plus scripts.verify_m2_restart | T3/T4 and twenty-step matrix below | PASS | Actual discovery-to-human-test-principal approval, stale/mutation/access negatives and container recovery executed. |
| AC-24 | Services remain independently buildable and deployable. | Four independent runtime Dockerfiles, optional m2 Compose profile and isolated volume | T7 CI image builds; actual compose up --build --wait | PASS | All five isolated services healthy; Agent has no database/human-account environment or database network. |
| AC-25 | CI and AIEngineeringStandards validation pass. | Seven standards manifests and scripts.check entry points | T1; exact-head CI matrix | PASS | All local gates pass; final central documentation checks tracked on its PR. |
| AC-26 | PR review comments and required conversations are appropriately resolved. | M2_REQUIREMENTS.md §18; configured Sourcery reviewer replacing removed CodeRabbit | Current submitted reviews, inline threads and reviewer checks | BLOCKED | Actual Sourcery reviews produced 71 individually assessed findings across six PRs. Fixes and evidence are pushed; individual responses/closure and re-review are being reconciled, including central PR. Human merge/acceptance remain pending. |
| AC-27 | Required CI checks pass on all affected PRs. | Independent .github/workflows/ci.yml and final PR heads | T7 exact-head validate checks | BLOCKED | Reviewed implementation heads are pushed; exact-head validate/Sourcery checks and the central evidence PR are being reconciled. |
| AC-28 | M2 handoff and completion evidence are accurate. | Current handoff/completion/final-verification records with retained history | Documentation consistency, source-SHA and test-count review; central gates | PASS | Fresh implementation evidence supersedes historical missing-runtime verdict without erasing it; human acceptance remains pending. |
| AC-29 | No autonomous coding or deployment activity is introduced in M2. | PM graph has no tools/approval API; no M3/runtime coding/deployment agent added | Agent no-tools regression; source inspection; isolated local testing only | PASS | No autonomous development or cloud deployment feature. Human explicitly authorized repository and isolated test environment creation. |


Review remediation adds explicit replay/CSRF/SSE/semantic contracts, PostgreSQL lifetime recovery ownership and policy locking, stricter review/discovery state guards, complete comparison/export and cursor history, bounded auth cleanup, Agent transport/cancellation/readiness/action schemas/provenance, robust Angular retry/unsaved-edit/routing/catalog/SSE controls, and isolated configuration/recovery hardening. All six full configured runtime gates pass. Raw refreshed logs: artifacts/m2-implementation/*-review-check.log, review-postgres.log, review-browser.log, review-compose.log and review-restart.log (ignored locally). Test count is 258 distinct Python tests including central 22; repeated PostgreSQL execution is not double-counted.

## Historical independent verification (retained verbatim)

# M2 acceptance criteria

Final verification: 2026-11-22 (America/Chicago). **PARTIAL; M3 NOT READY.**

6 PASS / 22 FAIL / 1 BLOCKED / 0 NOT_EXECUTED, out of 29. A FAIL based on missing implementation does not imply that its nonexistent runtime scenario executed. Individual unexecuted scenarios are explicitly identified.

Evidence IDs, exact commits, commands, PR governance and limitations: [final verification report](M2_FINAL_VERIFICATION_REPORT.md). PASS applies only to the stated scope; existing M1 tests do not establish M2 functionality. Documentation PR review/merge remains pending.

| ID | Requirement (unchanged) | Source implementation / absence | Test or verification method | Status | Execution evidence / gap |
| --- | --- | --- | --- | --- | --- |
| AC-01 | Existing M0/M1 architecture and standards are preserved. | ADR 0001–0004; all six repository manifests and independent build contexts | T1–T9; Git ancestry inspection | PASS | M1 implementation heads reachable from main; standards and independent existing images pass. |
| AC-02 | PM Agent is implemented in its approved service boundary. | Agent Service absent locally and from accessible GitHub inventory | S1; repository/API discovery | FAIL | No executable PM Agent or approved service implementation. |
| AC-03 | PM Agent uses the existing LLM Gateway. | Project Service gateway.py is an M1 chat client; Agent Service absent | S1; source inspection | FAIL | Gateway works in M1; no PM-to-Gateway integration exists. |
| AC-04 | Requirements discovery is available through Angular. | web src/app/app.routes.ts, navigation.ts, future.ts | T8; actual Chromium navigation | FAIL | No Requirements Studio link; Planning Studio is a future placeholder. |
| AC-05 | Users can respond to clarification questions. | web src/app and Project Service workspace.py | T8; source and runtime OpenAPI inspection | FAIL | No clarification model, endpoint or answer control. |
| AC-06 | Discovery state persists across application restarts. | Project Service database.py; migrations/versions/0001_project_workspace.py | S2; T7 baseline persistence tests | FAIL | Only projects/conversations/turns/messages persist. M2 discovery and restart recovery are absent; service restart NOT_EXECUTED. |
| AC-07 | Structured PRD generation works. | Agent Service absent; Project Service schemas.py | S1–S2; T8 runtime API inspection | FAIL | No typed 19-section PRD generation or structured-output validation. |
| AC-08 | PRD sections are editable. | web project-form.ts and app.routes.ts | S3; T8 | FAIL | M1 high-level requirements text field is not a structured PRD editor. |
| AC-09 | PRD revisions are persisted and distinguishable. | Project Service database.py and sole 0001 migration | S2; model/migration inspection | FAIL | No document/revision tables, content hashes or revision API. |
| AC-10 | Epics and user stories can be generated. | Agent Service absent; Project Service schemas.py | S1–S2; T8 | FAIL | No epic/story generation or storage. |
| AC-11 | Stories trace to requirements. | Project Service database.py and schemas.py | S2; complete domain-model inspection | FAIL | No stable requirement/story identifiers or traceability relations. |
| AC-12 | Acceptance criteria are structured and testable. | Project Service schemas.py; contracts openapi/*.json | S2/S4; contract inspection | FAIL | No structured requirement acceptance-criterion DTO or validation. |
| AC-13 | Requirements quality validation executes. | Agent Service absent; Project Service workspace.py | S1–S2; T8 | FAIL | No deterministic requirements validators or AI quality workflow. |
| AC-14 | Unresolved assumptions and questions remain visible. | web chat-studio.ts, future.ts; Project Service database.py | S2–S3; T8 | FAIL | Ordinary chat does not provide typed unresolved assumptions/questions or findings. |
| AC-15 | The approval workflow supports approved/rejected/changes-requested decisions. | web future.ts; Project Service workspace.py and database.py | T8; actual Approvals navigation and API inspection | FAIL | Approvals is a placeholder; no submit/approve/reject/request-changes operation or audit record. |
| AC-16 | Approved artifact versions are immutable. | Project Service database.py and sole migration | S2; storage/API inspection | FAIL | No approved revision or transactional immutability enforcement; mutation scenario NOT_EXECUTED. |
| AC-17 | Stale approval attempts are rejected. | Project Service workspace.py and schemas.py | S2; runtime OpenAPI inspection | FAIL | No revision-bound approval/hash/concurrency check; stale approval scenario NOT_EXECUTED. |
| AC-18 | PM Agent cannot approve its own output. | Agent Service absent; Project Service approval API absent | S1–S2; identity and endpoint inspection | FAIL | No agent/human approval separation exists to verify. Absence of an agent is not a passing self-approval control. |
| AC-19 | Project access boundaries are enforced to the extent supported by the authenticated runtime. | Project Service workspace.py:project_access; tests/test_workspace.py | T1/T7: test_owner_and_cross_project_isolation; test_production_local_identity_refused | PASS | M1 owner/nested-resource boundaries pass on SQLite and real PostgreSQL; limited server-configured developer identity only. No M2 artifact access claim. |
| AC-20 | Version comparison works. | web app.routes.ts; Project Service workspace.py | S2–S3; T8 | FAIL | No revisions or version-comparison API/UI. |
| AC-21 | API contracts are published and validated. | contracts openapi/project-service-0.1.0.json, project-service-0.2.0.json, llm-gateway-0.2.0.json | T1/T8; S4 | FAIL | Existing three M0/M1 contracts and SSE pass; no M2 APIs/DTOs are published. M1 compatibility is retained. |
| AC-22 | Unit, integration, and applicable frontend tests pass. | All six tests directories; web src/app/*.spec.ts | T1/T7/T8 | FAIL | 174 existing Python and 13 Angular tests pass, plus 35 PostgreSQL reruns and 3 existing browser tests; required M2 and LangGraph tests do not exist. |
| AC-23 | The full deterministic end-to-end discovery-to-approval workflow is verified. | web app.routes.ts/future.ts; runtime OpenAPI | T8; 20-step scenario below | FAIL | Real browser opens a project but cannot start discovery. Steps 3–20 NOT_EXECUTED. |
| AC-24 | Services remain independently buildable and deployable. | infrastructure compose.yaml; three existing Dockerfiles; Agent Service absent | T1/T9; S5 | FAIL | Existing three images build separately, but required Agent Service image/configuration/health and M2 local integration are absent. |
| AC-25 | CI and AIEngineeringStandards validation pass. | All six scripts/check.py, manifests and .github/workflows/ci.yml | T1/T2; GitHub exact-main runs | PASS | Six configured local gates and six exact-main validate runs pass; reviewer gates are assessed separately in AC-26. |
| AC-26 | PR review comments and required conversations are appropriately resolved. | M2_REQUIREMENTS.md section 18; 12 PR review records and thread collections | G1 governance matrix below | BLOCKED | Zero submitted reviews or inline threads. Required AI review absent/skipped/limited/summary-only; independent human acceptance not recorded. No actionable inline finding to resolve. |
| AC-27 | Required CI checks pass on all affected PRs. | 12 existing relevant M1/M2 PR statusCheckRollup records | G1; exact candidate and merged-main CI URLs | PASS | All existing relevant validate checks passed; skipped/neutral AI statuses are not counted as passed review. Verification PR gates tracked separately. |
| AC-28 | M2 handoff and completion evidence are accurate. | M2_FINAL_VERIFICATION_REPORT.md, M2_HANDOFF.md, M2_COMPLETION_REPORT.md | Fresh code/test/PR reconciliation and documentation diff review | PASS | Current evidence distinguishes merged M1 from documentation-only M2; historical checkpoints retained. This is evidence accuracy, not milestone approval. |
| AC-29 | No autonomous coding or deployment activity is introduced in M2. | Central M2 PR #4 changed only six milestone documents; all runtime trees inspected | git show b128d85 --stat; S1–S5 | PASS | No M2 tool execution, autonomous coding agent or cloud deployment introduced. Verification changed documentation only. |

## Historical prerequisite checkpoint (retained verbatim)

# M2 acceptance criteria

Status: no M2 runtime implementation or acceptance execution. Baseline gate in M2_HANDOFF.md remains open.

| Criterion | Requirement | Status | Evidence / gap |
| --- | --- | --- | --- |
| AC-01 | Existing M0/M1 architecture and standards are preserved. | BLOCKED | M1 main integration and baseline approval/review prerequisites outstanding |
| AC-02 | PM Agent is implemented in its approved service boundary. | NOT EXECUTED | M2 implementation and verification pending |
| AC-03 | PM Agent uses the existing LLM Gateway. | NOT EXECUTED | M2 implementation and verification pending |
| AC-04 | Requirements discovery is available through Angular. | NOT EXECUTED | M2 implementation and verification pending |
| AC-05 | Users can respond to clarification questions. | NOT EXECUTED | M2 implementation and verification pending |
| AC-06 | Discovery state persists across application restarts. | NOT EXECUTED | M2 implementation and verification pending |
| AC-07 | Structured PRD generation works. | NOT EXECUTED | M2 implementation and verification pending |
| AC-08 | PRD sections are editable. | NOT EXECUTED | M2 implementation and verification pending |
| AC-09 | PRD revisions are persisted and distinguishable. | NOT EXECUTED | M2 implementation and verification pending |
| AC-10 | Epics and user stories can be generated. | NOT EXECUTED | M2 implementation and verification pending |
| AC-11 | Stories trace to requirements. | NOT EXECUTED | M2 implementation and verification pending |
| AC-12 | Acceptance criteria are structured and testable. | NOT EXECUTED | M2 implementation and verification pending |
| AC-13 | Requirements quality validation executes. | NOT EXECUTED | M2 implementation and verification pending |
| AC-14 | Unresolved assumptions and questions remain visible. | NOT EXECUTED | M2 implementation and verification pending |
| AC-15 | The approval workflow supports approved/rejected/changes-requested decisions. | NOT EXECUTED | M2 implementation and verification pending |
| AC-16 | Approved artifact versions are immutable. | NOT EXECUTED | M2 implementation and verification pending |
| AC-17 | Stale approval attempts are rejected. | NOT EXECUTED | M2 implementation and verification pending |
| AC-18 | PM Agent cannot approve its own output. | NOT EXECUTED | M2 implementation and verification pending |
| AC-19 | Project access boundaries are enforced to the extent supported by the authenticated runtime. | NOT EXECUTED | M2 implementation and verification pending |
| AC-20 | Version comparison works. | NOT EXECUTED | M2 implementation and verification pending |
| AC-21 | API contracts are published and validated. | NOT EXECUTED | M2 implementation and verification pending |
| AC-22 | Unit, integration, and applicable frontend tests pass. | NOT EXECUTED | M2 implementation and verification pending |
| AC-23 | The full deterministic end-to-end discovery-to-approval workflow is verified. | NOT EXECUTED | M2 implementation and verification pending |
| AC-24 | Services remain independently buildable and deployable. | NOT EXECUTED | M2 implementation and verification pending |
| AC-25 | CI and AIEngineeringStandards validation pass. | BLOCKED | M1 main integration and baseline approval/review prerequisites outstanding |
| AC-26 | PR review comments and required conversations are appropriately resolved. | BLOCKED | M1 main integration and baseline approval/review prerequisites outstanding |
| AC-27 | Required CI checks pass on all affected PRs. | BLOCKED | M1 main integration and baseline approval/review prerequisites outstanding |
| AC-28 | M2 handoff and completion evidence are accurate. | NOT EXECUTED | M2 implementation and verification pending |
| AC-29 | No autonomous coding or deployment activity is introduced in M2. | NOT EXECUTED | M2 implementation and verification pending |

No criterion is inferred passed from a design document or historical M1 test. A mandatory BLOCKED or NOT EXECUTED criterion prevents full M2 acceptance.
