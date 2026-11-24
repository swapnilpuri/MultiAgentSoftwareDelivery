# M3 acceptance criteria

Statuses: PASS, FAIL, BLOCKED, NOT_EXECUTED, NOT_APPLICABLE. A criterion passes only on executed evidence. Evidence was produced at the PR heads below, on 2026-11-24, on the isolated local stack built from those branches.

**Tally: 44 PASS / 0 FAIL / 0 BLOCKED / 0 NOT_EXECUTED.** The PRs are merged on the owner's instruction and re-verified on `main` (see the end of this file). M3 acceptance remains with the owner.

| Repository | PR | Evidence head | CI | Sourcery (final head) |
|---|---|---|---|---|
| masd-contracts | [#5](https://github.com/swapnilpuri/masd-contracts/pull/5) | `e98ecf6` | success | skipped by Sourcery for the one-line schema follow-up; success on the prior head `074f39e` |
| masd-project-service | [#5](https://github.com/swapnilpuri/masd-project-service/pull/5) | `1af95a7` | success | success |
| masd-agent-service | [#3](https://github.com/swapnilpuri/masd-agent-service/pull/3) | `249b922` | success | success |
| masd-web | [#6](https://github.com/swapnilpuri/masd-web/pull/6) | `3cbff8e` | success | success |
| masd-infrastructure | [#6](https://github.com/swapnilpuri/masd-infrastructure/pull/6) | `9fbc13e` | success | success |
| MultiAgentSoftwareDelivery | [#11](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/11) | `52d275d` | success | success |
| masd-llm-gateway | none | `687db1b` (main) | success | not applicable: no change required |

Evidence keys:
- **G** = repository gates (`uv run --frozen python -m scripts.check`): contracts 78, Project Service 165 (+6 PostgreSQL-only skips), agent 103, web 22 Python + 91 Angular + production build, infrastructure 74 (+1 POSIX-only skip).
- **PG** = Project Service suite on real PostgreSQL 17: 171 passed, 0 skipped.
- **E2E** = Chromium suite: 5 expected, 0 skipped, 0 unexpected, 0 flaky. That is M0, M1×2, M2 and the M3 workflow `e2e/m3-architecture.spec.ts`.
- **RS** = `scripts.verify_m3_restart` PASS.
- **SEC** = `scripts.verify_m2 runtime-secrets` PASS (also checks that the Agent has no database or human configuration).

| ID | Acceptance criterion | Status | Evidence |
|---|---|---|---|
| M3-AC-01 | M2 baseline independently verified and accepted | PASS | M3_BASELINE_VERIFICATION.md: VERIFIED_ACCEPTED (owner, 2026-11-24) |
| M3-AC-02 | Existing microservice boundaries preserved | PASS | No new service (ADR 0006); Agent stateless with no DB (SEC); browser→Project Service only; G |
| M3-AC-03 | Architecture Studio available in Angular | PASS | E2E opens it from the main navigation and the project route |
| M3-AC-04 | Approved PRD can be selected | PASS | E2E source selection, then the source PRD evidence panel shows its requirements and a matching approval record (revision and hash); `test_only_an_approved_prd_can_be_selected` |
| M3-AC-05 | Unapproved PRD is rejected | PASS | Same test (422 for unapproved); Agent rejects a tampered PRD hash (`test_tampered_or_unapproved_prd_snapshot_is_rejected`) |
| M3-AC-06 | Architect Agent uses LLM Gateway | PASS | E2E generation through the real Gateway `test/structured` path; agent graph tests; no provider SDK in the Agent |
| M3-AC-07 | LangGraph architecture execution works | PASS | `tests/test_architect.py` (graph nodes, repair, interrupt, replay); E2E |
| M3-AC-08 | Agent state survives application restart | PASS | RS: checkpoint, baselines, earlier approved revision and snapshot-pinned history survive PostgreSQL plus four service restarts; interrupted key rejected; explicit retry |
| M3-AC-09 | Architecture clarifications can be resumed | PASS | E2E answer/defer then generate; API and agent clarification tests |
| M3-AC-10 | Structured architecture proposal generated | PASS | Schema-validated generation (agent and Project Service re-validation); E2E |
| M3-AC-11 | Architecture alternatives and tradeoffs available | PASS | Package `alternatives` (benefits, drawbacks, complexity, operational, security, cost, rationale); Studio tab |
| M3-AC-12 | Technology stack and rationale generated | PASS | `technology` section; Studio explorer |
| M3-AC-13 | Service boundaries and ownership generated | PASS | `services` plus ownership consistency rules; Studio boundary explorer with ownership conflicts |
| M3-AC-14 | API and event architecture proposals generated | PASS | `apis`/`events` labelled `proposed` (required field); cross-reference rules |
| M3-AC-15 | Data models generated | PASS | `data` entities and relationships; ownership rules |
| M3-AC-16 | Deployment architecture generated | PASS | `deployment` (`is_proposal`); Studio |
| M3-AC-17 | Security architecture generated | PASS | Trust boundaries, controls, threats→mitigations; security quality rules |
| M3-AC-18 | C4 System Context diagram generated and rendered | PASS | E2E renders the context view as SVG; PlantUML/Mermaid tests |
| M3-AC-19 | C4 Container diagram generated and rendered | PASS | E2E container view with its focus drawn as a system boundary, relationship inspection, and C4-PlantUML download (`System_Boundary`) |
| M3-AC-20 | C4 Component diagram supported | PASS | E2E component view; level-element rules |
| M3-AC-21 | ADR proposals generated | PASS | ADRs stay proposed unless set by an authorized human; E2E shows proposed, and approved shows accepted |
| M3-AC-22 | Architecture revisions persisted | PASS | PG (migration 0004, append-only triggers); E2E |
| M3-AC-23 | Architecture revision comparison works | PASS | ID-based compare across all collections (unit); E2E |
| M3-AC-24 | Requirement traceability available | PASS | Many-to-many matrix including overview statements; E2E coverage table |
| M3-AC-25 | Architecture quality validation detects material issues | PASS | One test per deterministic rule (coverage, orphans, ownership, security, communication, ADRs, contradictions, diagrams) |
| M3-AC-26 | Source PRD drift is detected | PASS | E2E drift banner, rebase, re-approval; PRD approved *during* generation is rejected |
| M3-AC-27 | Architecture review and change requests work | PASS | E2E submit → request changes → revise → resubmit |
| M3-AC-28 | Authorized human approval works | PASS | E2E approval by a password-verified human; decision record with policy version |
| M3-AC-29 | Stale or unauthorized approval is rejected | PASS | E2E stale hash returns 409, anonymous returns 401; non-approver returns 403; other human returns 404 |
| M3-AC-30 | Approved architecture revision is immutable | PASS | PG trigger and ORM tests; E2E earlier baseline unchanged after re-approval |
| M3-AC-31 | Architecture exports are consistent with canonical data | PASS | Export JSON equals the canonical package, with `X-Content-Hash` equal to the stored hash (E2E and API) |
| M3-AC-32 | Versioned platform API contracts validated | PASS | masd-contracts 0.4.0 (schema, validator, two OpenAPI documents, SSE); runtime-equality snapshot tests; 0.3.0 byte-identical |
| M3-AC-33 | No direct cross-service database access | PASS | SEC: the Agent has no DB or human configuration; Project Service is the only DB owner |
| M3-AC-34 | All applicable unit and integration tests pass | PASS | G and PG |
| M3-AC-35 | Frontend tests and build pass | PASS | Web gate: 91 Angular tests, production build, ESLint, `tsc`, Prettier, `npm audit` 0 |
| M3-AC-36 | Deterministic end-to-end architecture workflow passes | PASS | E2E (Chromium, 0 skips), with keyboard operation (canvas zoom/reset, relationship list, inspector, evidence disclosure) and a 390px no-overflow check |
| M3-AC-37 | Security, standards and regression checks pass | PASS | Governance/standards validators, secret scans, dependency audits in every gate; M0–M2 browser regressions in E2E; SEC. Limitation: no container image vulnerability scan |
| M3-AC-38 | Independent service build/deployment boundaries preserved | PASS | Each image built from its own repository context (`m2_compose up --build`); independent CI per repository |
| M3-AC-39 | Configured AI PR reviews completed | PASS | Sourcery reviewed all six PRs, including central #11, with success on every final head except contracts. There, Sourcery skipped the one-line `x-content-hash` follow-up (`e98ecf6`) after succeeding on `074f39e`; that change is the same schema text reviewed in project-service #5 |
| M3-AC-40 | Actionable PR feedback addressed and required threads resolved | PASS | Every actionable finding fixed with regressions or answered with evidence, and every thread resolved. The former focus dispute (contracts #5) was resolved by implementing the focus as a rendered C4 boundary |
| M3-AC-41 | Required PR CI checks pass | PASS | `validate` success on every PR head |
| M3-AC-42 | M3 documentation, completion evidence and handoff are accurate | PASS | This file, M3_COMPLETION_REPORT.md, M3_HANDOFF.md, M3_DESIGN.md corrections |
| M3-AC-43 | Human merge approval remains mandatory | PASS | No PR merged; all PRs await human review |
| M3-AC-44 | M3 does not perform autonomous target-application coding or deployment | PASS | Agent has no tools; no-tools prompt test; Architect returns proposals only; no deployment capability |

Limitations (not hidden as passes): generation quality was verified only with the deterministic `test/structured` adapter through the real Gateway; there was no live commercial or Ollama generation. Authentication is development-only (production startup refused). There was no container image vulnerability scan and no cloud deployment.

## Post-merge verification on `main` (2026-11-24)

All six M3 PRs were merged by the owner's instruction, in order, each pinned with `--match-head-commit` to the verified head. The full evidence was then re-run from clean `main` checkouts, on the isolated masd-m2 stack rebuilt from `main`.

| Repository | `main` | Merged PR | Post-merge CI |
|---|---|---|---|
| masd-contracts | `f8cb30c` | #5 | success |
| masd-project-service | `7798356` | #5 | success |
| masd-agent-service | `bb851aa` | #3 | success |
| masd-web | `748f308` | #6 | success |
| masd-infrastructure | `4c8c350` | #6 | success |
| MultiAgentSoftwareDelivery | `72f5d9b` | #11 | success |
| masd-llm-gateway | `687db1b` | none | unchanged |

| Check | Result on `main` |
|---|---|
| Gates (`scripts.check`) | contracts 78; Project Service 165 (+6 PostgreSQL-only skips); agent 103; Gateway 50; web 22 Python + 91 Angular + production build; infrastructure 74 (+1 POSIX-only skip); central 40. Each with secret scan 0 findings and dependency audit clean |
| Real PostgreSQL 17 | 171 passed, 0 skipped |
| Chromium | 5 expected, 0 skipped, 0 unexpected, 0 flaky (M0, M1×2, M2, M3) |
| Restart (`verify_m3_restart`) | PASS |
| Runtime secrets | PASS before and after the restart run (730 KB of logs; Agent has no DB or human configuration) |
| Visual | Desktop and 390px Studio screenshots inspected; no overflow |

The infrastructure gate first failed 3 tests when it was run concurrently with `m2_compose up`: both take the same process lock (`PermissionError` in `process_lock.py`). Run alone, it passed. This is a test-isolation limitation of running the two together, not a product defect.

Result: **all 44 criteria still PASS on `main`.** M3 acceptance is the owner's decision and is not recorded here.
