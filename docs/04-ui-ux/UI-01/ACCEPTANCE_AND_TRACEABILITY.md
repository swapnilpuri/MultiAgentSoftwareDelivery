# UI-01 acceptance, requirements traceability and Playwright strategy

**DRAFT — v0.2, 2026-11-28.** This is a validation design, not evidence that the proposed UI exists or has passed. Foundations F1–F7 were approved; full design/implementation acceptance is separate.

## Requirements and deliverable traceability

“Specified” below means a reviewable design artifact is provided. It does not mean approved or implemented. Existing audit source IDs retain their original pinned evidence meaning.

| Req | Requested deliverable | Design artifact / dependencies | Acceptance evidence after implementation |
|---|---|---|---|
| UI01-01 | Application design system | DESIGN_SYSTEM; F3; SH components | V01–V07; PW10–PW12 |
| UI01-02 | Palette and typography | DESIGN_SYSTEM token/type tables | Numeric contrast + browser state/zoom checks |
| UI01-03 | Shared component guidelines | DESIGN_SYSTEM + TECHNICAL_DESIGN component table | SH01–SH18 unit/integration + keyboard tests |
| UI01-04 | Navigation hierarchy | NAVIGATION; F1/F2 | PW01/PW03/PW09 legacy/new destinations |
| UI01-05 | Complete page inventory | PAGE_SPECIFICATIONS inventory, WF-001–014 | Each listed entry/state reachable without new credentials |
| UI01-06 | Routes/backward compatibility | NAVIGATION destination/alias table | Parameterized PW01 incl child IDs/query/fragments |
| UI01-07 | Functional specifications for 14 wireframes | PAGE_SPECIFICATIONS + SH01–SH18 | All page-control IDs have stated states and AC |
| UI01-08 | User journeys | TECHNICAL_DESIGN UJ01–UJ08 | PW02–PW09 including negative/recovery cases |
| UI01-09 | Authentication/session | TECHNICAL_DESIGN auth + auth-recovery.puml; audit E03 | PW02/PW07 config modes, expiry, identity isolation |
| UI01-10 | Project context/switching | TECHNICAL_DESIGN state/transaction + project-switch.puml | PW04 out-of-order/denied/guard/reload cases |
| UI01-11 | Background operations | TECHNICAL_DESIGN operation table + observer/state diagrams | PW05/PW06 nonterminal slow run, races, stale state |
| UI01-12 | Angular architecture | TECHNICAL_DESIGN component table + shell-foundation.puml | Lazy-load/build checks; no duplicate auth/context/poller |
| UI01-13 | State management | TECHNICAL_DESIGN persistence/invalidation table | Unit races/storage failure + PW04/PW07 |
| UI01-14 | API reuse/gaps | TECHNICAL_DESIGN existing APIs + AP01–AP08; audit E12 | No contract changes in core; gaps remain excluded |
| UI01-15 | Editable PlantUML | Five sources in diagrams/ | PlantUML render/parse + visual inspection before claiming rendered evidence |
| UI01-16 | Functional criteria | FC01–FC14 below + every control AC | Executed browser/API evidence, not mock screenshots |
| UI01-17 | Visual criteria | DESIGN_SYSTEM V01–V07 + VC01–VC06 below | Agreed deterministic screenshots + human visual review |
| UI01-18 | Requirements traceability | This matrix + screen/control matrix below | No orphan requirement/control or false completion |
| UI01-19 | Playwright strategy | PW01–PW12 below | Versioned e2e results/traces/screenshots tied to commit |
| UI01-20 | Proposed M3.2 plan | M3_2_PROPOSED_PLAN.md; baseline gate | Separately authorized slices; no implementation prompt here |
| UI01-R1 | Review/reconcile all 14 | RECONCILIATION R01–R06 + per-screen table | Written corrections govern unchanged originals |
| UI01-R2 | Regenerate seven crops | wireframes/UI-01/v0.3 index, images, prompts, manifest | Seven independent generations, real dimensions/hashes, visual review |
| UI01-P1 | Package/provenance/publication | ARTIFACT_MANIFEST, CODEX_PUBLISH_PROMPT, revision README, ZIP | SHA-256 verification, docs-only PR/checks/findings, human baseline approval separate |

## Functional acceptance and control-to-test mapping

| Criterion / WF | Controls / journey | Observable pass condition | Planned tests |
|---|---|---|---|
| FC01 / 001 | LG01–05; UJ01 | Actual config selects OIDC or dev password; safe return; clear retry; no invented auth option | PW02/PW07 |
| FC02 / 002 | HM01–05; UJ02/03 | Authorized paginated list, explicitly local filter, single Home/Projects, backed opens; list error not empty | PW03/PW04 |
| FC03 / 003 | CR01–06 | Current fields/limits/model consent retained; dirty cancel; one confirmed create; uncertainty no automatic duplicate | PW03/PW08 |
| FC04 / 004 | SH01–07/13/17/18 | Shared guarded shell/deep links and route errors; no unsupported search/bell/metrics | PW01/PW04/PW09 |
| FC05 / 005 | DB01–05 | Backed metadata/links and settings/save/archive retained; no lifecycle percent/agent/task/approval fiction | PW03/PW08 |
| FC06 / 006 | SH05/06 | Same destinations/permissions in rail; accessible names/current state; collapse changes no data | PW10/PW11 |
| FC07 / 007 | SH08–12 + OP01–03; UJ05 | Followed scope versus bounded history explicit; real status/actions; disconnect ≠ cancel; no false durability for chat | PW05/PW06 |
| FC08 / 008 | SH02–04 + HM04/05; UJ04 | Guarded authorized switch, no old child IDs or mixed project rendering; stale responses ignored | PW04 |
| FC09 / 009 | SH13–15 + ST01–03 | Read-only session data; theme + existing model/provider/project settings; truthful sign-out outcome | PW07/PW08/PW12 |
| FC10 / 010 | SH14; UJ07 | Light/dark/system alter only presentation; invalid/unavailable storage safe fallback | PW11/PW12 |
| FC11 / 011 | HM06; UJ02 | Successful zero projects shows welcome/create; no tour/provisioning claim; failures not first-time success | PW03 |
| FC12 / 012 | SH16, LG01/03; UJ06 | Private view masked, safe reauth, permission refreshed, no mutation replay or cross-identity data | PW02/PW07 |
| FC13 / 013 | SH02/06/08/13; UJ07 | Critical controls reachable at narrow/zoomed layouts; modal focus/inert/scroll state correctly released | PW10/PW11 |
| FC14 / 014 | DB05, unavailable links; UJ08 | Future explanation and safe return only; no execution, approval mutation or release promise | PW09 |

## Visual acceptance

VC01: Use selected violet direction and consistent network brand treatment from approved F3/F6. Generated raster glyphs are illustrative; existing editable assets/icon system remain implementation source. Text/status vocabulary follows the written design, including active/archived project status and Future labels.

VC02: Screenshots compare identical fixture data in light/dark, expanded/collapsed and responsive variants. Mask only nondeterministic actual IDs/timestamps when justified and recorded; never mask incorrect project identity, permission UI or operation state to make a test pass.

VC03: At 320/768/1280/1600 CSS px and 200% text/400% page zoom checks where applicable, no page-level horizontal overflow, hidden critical actions, clipped form labels, overlapping menus or inaccessible scroll regions. Responsive board pixels are not proof of CSS viewport conformance.

VC04: Verify all solid/composited text, error, selected, disabled, hover and focus states against contrast targets; forced-colors and reduced-motion remain usable. Earlier arithmetic (17 specified text pairs, minimum 5.98:1) does not certify these browser states.

VC05: Desktop/tablet/mobile navigation has exactly one current destination; Future accessible names retained; user/theme/operations reachable; dialog closes restore focus. Same-app links have no external-link indicator. Generated responsive board's content labels are route links, not an instruction to invent dashboard tabs.

VC06: Human visual review checks readable text/brand/spacing and every regenerated image's restrictions. WF-001–007 remain preserved historical drafts with written corrections; no claim that their pixels were revised. Baseline review must explicitly accept the written corrections over those images or request additive redraws before pixel-level acceptance. Generated v0.3 remains DRAFT, not application/browser evidence.

## Playwright validation strategy (planned, not executed)

Retain existing web e2e organization/auth helpers; add targeted UI-01 scenarios after implementation authorization. Use a deterministic configured test provider and dedicated test-only fixtures, separate from product runtime data. Seed two distinct authorized projects A/B, an archived project, a second identity/tenant, a paginated list >30 and an empty account. Authentication-mode tests use separate test environments/config fixtures, not production config changes.

| Test | Scenario and required assertions | Evidence |
|---|---|---|
| PW01 | Parameterize every existing canonical route and six historical aliases; include project conversation/session/artifact IDs, operation query, supported fragment; root/wildcard behavior | Destination/ID assertions; no lost resource ID on same-project deep link; legacy `/planning` still Requirements |
| PW02 | Public sign-in config pending/failure, OIDC versus development password, callback refusal, safe-return external/API/protocol-relative rejection | Request/route assertions + screen states; no social alternatives or secret persistence |
| PW03 | Home loaded/empty/error, page boundaries/filter scope, create valid/invalid/no eligible model, success refresh without auto-generation | POST count/body, rendered list scope, explicit empty/error distinction |
| PW04 | Select A→B and A→B→A with deferred responses; dirty guard decline; target 403/404/503; direct link overrides storage; storage unavailable | Assert route, header, breadcrumbs and body agree at each observation; no foreign IDs |
| PW05 | Start deliberately blocked/slow Requirements then Architecture operation, confirm server running, navigate/reload/open drawer, verify same operation ID | Actual nonterminal server record before navigation; release deterministic execution latch then observe result; no duplicate start |
| PW06 | Cancel-complete race, interrupted failure, known retry versus unknown-start reconciliation, read outage, dismiss terminal versus running | Actual allowed actions/status; original versus new key counts; no pause/resume/percent, close never cancel |
| PW07 | Expire session during read/uncertain command, mask private view, same-user reauth, different-user return, logout refused/pending/confirmed/unconfirmed | Cookie/session boundary and storage isolation; no auto-replay; no saved-draft guarantee |
| PW08 | Dashboard edit/save/model consent/archive/read-only, settings models/capabilities failure, existing studio/artifact navigation | Existing fields/actions retained, only actual outcome changes state, no browser provider credential |
| PW09 | Every future module explanation, old alias behavior, no project and denied project handling; absent global search/bell | Network asserts zero generation/approval calls; safe navigation only |
| PW10 | Keyboard-only menus/selector/drawers, focus containment/return/skip link/current page, screen-reader name review | DOM/ARIA assertions + manual assistive-technology review; accessibility scanner alone insufficient |
| PW11 | 320/768/1280/1600 layout, collapsed rail, overlay resize/route cleanup, text zoom, reduced motion, forced colors | Overflow/focus assertions + screenshots; desktop screenshot does not prove mobile |
| PW12 | Light/Dark/System, OS preference change, reload, disabled/invalid storage; matched-data screenshots | Theme/state assertions and deterministic visual diffs |

Use explicit web-first assertions and deterministic server events; no arbitrary sleeps to “prove” durability. Unit tests should cover request epochs, preference parsing, navigation mapping and race rollback; contract/backend tests are required only if a separately authorized gap changes those owners. Chromium is the proposed blocking e2e lane; Firefox/WebKit core auth/navigation/focus/appearance smoke lanes are proposed before acceptance and must be agreed with supported-platform policy. Do not claim them passed until run.

Visual regression: establish human-approved implementation screenshots as baselines; generated images are references only. Proposed initial `maxDiffPixelRatio=0.005` for deterministic scenes, with animation disabled and stable fonts; require human review of any changed baseline and investigate every meaningful difference even within tolerance. Threshold/platform adjustments require recorded evidence; do not auto-update snapshots to silence regressions.

Record command, commit, fixture/config mode, browser/version, viewport/theme, results, failure trace/screenshots and skipped limitations in the implementation handoff. Required full checks per affected repository follow focused slices; integration smoke uses actual services for authorization/cancellation behavior. Mocked browser tests alone cannot prove backend access control or run survival.
