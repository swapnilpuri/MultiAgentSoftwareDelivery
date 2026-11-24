# M3 acceptance criteria

Statuses: PASS, FAIL, BLOCKED, NOT_EXECUTED, NOT_APPLICABLE (with justification). A criterion passes only with executed evidence, never because code or documentation exists. Current tally: **1 PASS / 43 NOT_EXECUTED** (Slice 0).

| ID | Acceptance criterion | Status | Evidence / planned verification |
|---|---|---|---|
| M3-AC-01 | M2 baseline independently verified and accepted | PASS | M3_BASELINE_VERIFICATION.md: VERIFIED_ACCEPTED 2026-11-24 (owner acceptance, 29/29 post-merge) |
| M3-AC-02 | Existing microservice boundaries preserved | NOT_EXECUTED | No new service (ADR 0006); boundary review + independent builds |
| M3-AC-03 | Architecture Studio available in Angular | NOT_EXECUTED | Angular route + Chromium e2e |
| M3-AC-04 | Approved PRD can be selected | NOT_EXECUTED | Project Service tests + e2e |
| M3-AC-05 | Unapproved PRD is rejected | NOT_EXECUTED | Project Service negative tests |
| M3-AC-06 | Architect Agent uses LLM Gateway | NOT_EXECUTED | Agent graph tests through the Gateway client; live stack e2e |
| M3-AC-07 | LangGraph architecture execution works | NOT_EXECUTED | Agent graph tests |
| M3-AC-08 | Agent state survives application restart | NOT_EXECUTED | Restart verifier on PostgreSQL |
| M3-AC-09 | Architecture clarifications can be resumed | NOT_EXECUTED | Clarification interrupt + answer tests |
| M3-AC-10 | Structured architecture proposal generated | NOT_EXECUTED | Schema-validated generation tests |
| M3-AC-11 | Architecture alternatives and tradeoffs available | NOT_EXECUTED | Package section tests + UI |
| M3-AC-12 | Technology stack and rationale generated | NOT_EXECUTED | Package section tests + UI |
| M3-AC-13 | Service boundaries and ownership generated | NOT_EXECUTED | Package + ownership validation tests |
| M3-AC-14 | API and event architecture proposals generated | NOT_EXECUTED | Package + reference validation tests |
| M3-AC-15 | Data models generated | NOT_EXECUTED | Package section tests |
| M3-AC-16 | Deployment architecture generated | NOT_EXECUTED | Package section tests |
| M3-AC-17 | Security architecture generated | NOT_EXECUTED | Package + threat/control validation tests |
| M3-AC-18 | C4 System Context diagram generated and rendered | NOT_EXECUTED | View generation + SVG render tests + e2e |
| M3-AC-19 | C4 Container diagram generated and rendered | NOT_EXECUTED | As above |
| M3-AC-20 | C4 Component diagram supported | NOT_EXECUTED | As above |
| M3-AC-21 | ADR proposals generated | NOT_EXECUTED | ADR schema + status tests |
| M3-AC-22 | Architecture revisions persisted | NOT_EXECUTED | PostgreSQL immutability tests |
| M3-AC-23 | Architecture revision comparison works | NOT_EXECUTED | ID-based diff tests + UI |
| M3-AC-24 | Requirement traceability available | NOT_EXECUTED | Traceability calculation tests + UI matrix |
| M3-AC-25 | Architecture quality validation detects material issues | NOT_EXECUTED | Deterministic rule tests (each rule) |
| M3-AC-26 | Source PRD drift is detected | NOT_EXECUTED | Drift API tests + e2e |
| M3-AC-27 | Architecture review and change requests work | NOT_EXECUTED | Transition tests + e2e |
| M3-AC-28 | Authorized human approval works | NOT_EXECUTED | Approval tests + e2e |
| M3-AC-29 | Stale or unauthorized approval is rejected | NOT_EXECUTED | Negative approval tests |
| M3-AC-30 | Approved architecture revision is immutable | NOT_EXECUTED | PostgreSQL trigger tests |
| M3-AC-31 | Architecture exports are consistent with canonical data | NOT_EXECUTED | Export round-trip/consistency tests |
| M3-AC-32 | Versioned platform API contracts validated | NOT_EXECUTED | Contracts 0.4.0 validation + consumer snapshot tests |
| M3-AC-33 | No direct cross-service database access | NOT_EXECUTED | Agent has no DB configuration (runtime check) + review |
| M3-AC-34 | All applicable unit and integration tests pass | NOT_EXECUTED | All repo gates + PostgreSQL suite |
| M3-AC-35 | Frontend tests and build pass | NOT_EXECUTED | Web gate |
| M3-AC-36 | Deterministic end-to-end architecture workflow passes | NOT_EXECUTED | Chromium e2e |
| M3-AC-37 | Security, standards and regression checks pass | NOT_EXECUTED | Gates, secret scans, audits, M0–M2 regression |
| M3-AC-38 | Independent service build/deployment boundaries preserved | NOT_EXECUTED | Independent image builds |
| M3-AC-39 | Configured AI PR reviews completed | NOT_EXECUTED | Sourcery on each PR head |
| M3-AC-40 | Actionable PR feedback addressed and required threads resolved | NOT_EXECUTED | Thread audit |
| M3-AC-41 | Required PR CI checks pass | NOT_EXECUTED | Exact-head CI |
| M3-AC-42 | M3 documentation, completion evidence and handoff are accurate | NOT_EXECUTED | Final reconciliation |
| M3-AC-43 | Human merge approval remains mandatory | NOT_EXECUTED | Merge records (human) |
| M3-AC-44 | M3 does not perform autonomous target-application coding or deployment | NOT_EXECUTED | No-tools regression + prohibited-behaviour tests |
