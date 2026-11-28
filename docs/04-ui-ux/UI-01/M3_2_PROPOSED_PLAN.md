# Proposed M3.2 implementation plan

**DRAFT — design proposal only, 2026-11-28.** This is a dependency/acceptance plan, **not a Codex implementation prompt**. F1–F7 approval does not approve the whole UI-01 baseline or authorize implementation. M3.2 and M4 remain blocked until the relevant explicit human gates are satisfied.

## Proposed bounded core scope

The core proposal is an Angular presentation/usability slice using current Project Service contracts: coherent navigation/shell, configuration-driven sign-in, authorized per-tab context/picker, truthful project dashboard and preserved edit/archive, followed operations/project activity, read-only account/settings, themes, responsive/empty/recovery/future states. No new framework/microservice, execution domain, durable Discovery promise, account editor, global search/inbox or invented summary metrics.

| Slice | Proposed repository scope / dependency | Independently reviewable outcome | Verification after authorization |
|---|---|---|---|
| M32-0 Baseline review | Central design package and visual corrections | Explicit whole UI-01 approval record, accepted open choices and scope; M3.1 acceptance separate | Package integrity, design review; no code |
| M32-1 Design tokens/shared primitives | masd-web; approved F3 and visual baseline | Light/dark/system tokens, accessible controls/status/dialog foundations; retain standalone components and current icon assets | Focused preference/contrast/component checks, browser theme/zoom; no speculative snapshot-only unit tests |
| M32-2 Shell/navigation/context | masd-web; M32-1 + route map | Same deep links and one session; selector with guard-safe switching, stable project identity, expanded/collapsed/mobile nav, unavailable routes | PW01/04/09/10/11; request-race/guard tests |
| M32-3 Home/create/dashboard/settings | masd-web; M32-2 + existing APIs | Paginated projects, actual empty/error state, current create/edit/archive retained, truthful backed dashboard, read-only identity | PW03/08; API-level authorization regression reused |
| M32-4 Operations and recovery | masd-web; M32-2 + actual operation contracts | Followed drawer versus bounded history; server actions; expiry mask/safe return; no mutation replay | PW02/05/06/07 using slow deterministic live service runs |
| M32-5 Acceptance and handoff | All affected repository gates; independently built deployment artifacts unchanged | Matched light/dark/responsive screenshots, accessibility and compatibility evidence, unresolved gaps explicit | Focused PW01–12 then appropriate full web/service/infrastructure integration; human functional/visual review |

Order may be narrowed further during separately authorized execution. Shared docs/code/Git writes must not race. Contract changes are not expected for this core; if new evidence requires them, stop that dependent slice for reviewed additive design rather than hiding a backend change in a CSS task. Existing repositories keep independent CI/build/deploy paths.

## Optional future work excluded from core commitment

AP01 cross-account activity, AP02 durable Discovery, AP03 measured progress/queue/resume, AP04 account edits, AP05 search/inbox/share/team, AP06 aggregates/shared approvals, AP07 downstream workflows and AP08 create-idempotency/draft persistence are not implied M3.2 tasks. Each needs domain scope, ownership and versioned contract decisions. For an authorized additive feature: contracts → owning service tests → web consumer → integration/acceptance; consequential migrations/config/security/deployment retain explicit approval.

Detailed Discovery or other engineering studio redesign is not part of UI-01. Existing studio functions and approval/provenance constraints are regression obligations, not design permission to rework them. M4 remains outside this plan.

## Baseline review choices remaining

| Choice | Proposed design resolution | Human review scope |
|---|---|---|
| Historical WF-001–007 mismatch | Preserve original bytes; written control/navigation corrections govern | Accept annotated reconciliation or request additive corrected renders |
| New v0.3 visual drafts | Seven independent renders; semantic specs govern exact controls/spacing | Human visual approval still required |
| Core versus API gaps | Core UI-only/API reuse; AP01–08 deferred | Confirm scope when approving entire baseline |
| Local appearance / support links | System default; local persistence; support/legal links only if verified | Confirm destinations before enabling links; no fabricated defaults |
| Browser/visual lane | Chromium blocking; Firefox/WebKit smoke proposed; 0.5% initial deterministic diff tolerance | Align supported-platform policy before implementation acceptance |
| Unsaved auth redirect | Existing guards/recovery only; no durable-draft promise | Approve limitation or separately design content persistence |

No implementation prompt is generated in this package. After explicit full UI-01 baseline approval, an implementation prompt may reference the accepted revision, scope, compatibility/test gates and remaining decisions. Baseline approval itself still does not authorize deployment, migrations, permission changes, merge or M4.
