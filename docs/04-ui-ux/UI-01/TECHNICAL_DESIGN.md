# UI-01 technical design and API boundary

**DRAFT — v0.2, 2026-11-28.** Foundations approved; detailed baseline pending. Uses the existing [implementation audit](../IMPLEMENTATION_AUDIT.md) and targeted source evidence in RECONCILIATION.md. No application/API/migration/configuration change is performed here.

## Angular shared component architecture

Retain independently deployable masd-web, standalone lazy routed pages and existing Angular signal services. New names below are proposed presentation boundaries, not a new framework or committed implementation. Keep existing imports/dependency direction; avoid Auth ↔ Router ↔ context injection cycles (Auth currently resolves Router lazily).

| Proposed boundary | Responsibility / inputs / output intents | Reuse / state owner |
|---|---|---|
| ApplicationShell | Session gating, page layout, route-load failure, recovery masking; orchestrate guard-safe intents | Existing App and Router; no API duplication |
| ShellHeader | Project trigger, followed-operation trigger, user trigger | Inputs from context/auth/tracker; emits overlay intent |
| ShellSidebar | One navigation definition, current route, collapsed/modal variants, Future explanations | Extend existing sections metadata; Router remains navigation owner |
| ShellBreadcrumbs | Derived ancestors with authorized project name, current destination | Existing title/breadcrumb behavior |
| ProjectSelector | Authorized page results/filter/paging, pending selection | WorkspaceApi for reads, ProjectContext commits selection only through coordinated navigation |
| BackgroundOperationsDrawer | Render followed rows grouped/labeled by project and actual state; close/open/cancel/retry intent | OperationsTracker and existing studio APIs; no second poller |
| UserMenu / ThemePreference | Read-only identity, region links, sign-out; Light/Dark/System | Auth plus small local preference service |
| ProjectDashboard | Metadata, backed destinations, preserved edit/archive flow | Existing ProjectDetail + ProjectForm; reuse form validators and WorkspaceApi |
| UnavailableView | Static availability explanation plus safe backed navigation | Same navigation definition; no mutation adapter |
| Shared presentation primitives | Status, empty/error/loading, named dialog, project row and button styling | Existing HTML/CSS patterns first; no new UI library |

A single typed navigation definition drives sidebar, breadcrumbs/help, routes' section labels and capability availability. Distinguish `available`, `future`, `requires-project` from server authorization. It must not derive capability state from a mock project's lifecycle. Reuse existing sectionLink semantics and explicitly retain compatibility aliases. Lazy load future placeholder bodies if necessary; the shell cannot import every studio merely to render a menu.

## Application state and persistence

| State | Owner / persistence | Invalidation / races / failure |
|---|---|---|
| Session identity/config/state | Existing Auth; HTTP-only cookie, in-memory identity; no browser credential storage | Session epoch fences old reads; sign-out/expiry/identity change invalidate user data. Config not a list of social providers |
| Selected project | URL is active identity; ProjectContext stores per-tab project ID only and authorized snapshot | URL wins; request generation fences stale reads; 403/404 clear invalid reference; transient failure preserves last context with stale/error indicator |
| Project list/page/filter | Selector or Projects view; local signals, shared adapter, optional short-lived per-user cache | Cache keyed identity/tenant and cleared on logout; no persistence of project contents; scope filter to loaded page(s); race fence queries/pages |
| Followed operations | Existing tracker, existing sessionStorage recovery records and API-backed snapshots | Continue existing authorized tracking across project change; pause on expiry; clear on identity change; poll failures separate from outcome |
| Project operation history | Operations page server read; selected project+status query state | Bounded history is not all-account completeness; request generations prevent wrong-project rows |
| Overlay/focus/menu state | Shell local signals; not persisted | One modal at a time; route/viewport change closes/reconciles overlay and focus; cancel only on explicit user command |
| Theme/collapse preference | Local nonsecret preference; versioned, allowlisted values; memory fallback | Theme initial System; prepaint best effort; storage failure tolerable. Collapse constrained by viewport, never alters route |
| Project form / studio draft / uncertain-start key | Existing owning page/services; existing recovery policy | Preserve dirty guard and exact unknown-outcome/idempotency records; no incidental new localStorage draft store |

Do not treat browser state as authority. A stale response must pass both request-generation and identity/project checks before application. Clear private view data when session changes; a theme preference may remain because it is not user content. Existing command recovery keys must not be removed before outcome reconciliation just to make logout easier.

### Coordinated project switching

1. Capture route/project and target intent under a new navigation generation; disable duplicate selection while pending.
2. Consult the owning page's existing leave guard before replacing context. A rejected leave keeps selection, form and route. Use the same guard through a navigation coordinator; do not invoke two discard dialogs for one action.
3. Read target project through authorized API. A 403/404 reports unavailable without exposing metadata; transient failure permits retry and leaves current selection intact.
4. Build equivalent implemented target route from destination key. Drop source conversation/session/artifact IDs and operation query. Do not carry private/old-resource query state across projects. Preserve only explicitly allowlisted UI query/fragment state that remains meaningful; default to no cross-project child state.
5. Navigate and publish committed target context only for the latest successful navigation. Existing route activation calls to ProjectContext need a coordinated pending state so old page content never renders under a new project name. On guard cancellation, route-load failure or raced intent, restore the prior committed snapshot and expose error.
6. Direct deep links use the same authorization/context reconciliation without rewriting resource IDs. Generic Home retains context but renders global data. All followed operations retain their own project/session IDs independently.

Cross-tab synchronization is deliberately not added: current persistence is per-tab. Closed-tab/device restoration of selected project would require a separate product decision. Opened archived projects remain readable; mutation restrictions remain server-owned.

## Authentication and session design

Preserve existing same-origin BFF approach: Project Service owns OIDC exchange, session cookie and human authorization; browser calls configured same-origin login entry with sanitized return. Keep cookie/CSRF headers and existing callback error-code mapping. Session unknown → loading; signed-out → configured sign-in; unavailable → service retry; expired → protected-content mask and reauthentication; signed-in → authorize and render destination. Do not classify every 403 as expiry. Do not change session lifetime, cookie attributes, provider setup or permissions in a UI design slice.

Return destinations must be app-local and pass the existing safe-return boundary (reject protocol-relative/backslash/API/sign-in targets); server and route authorization still apply. No auto-replay of a mutation after login. Same identity may reconcile known operation IDs/keys; different identity clears project/tracker/draft recovery state according to current owner-reset semantics before rendering. No cross-identity promise to restore unsaved input.

Logout first respects leave/uncertain-start guards, then calls existing logout with CSRF and reports only confirmed session/provider result. Timeout yields unconfirmed, not “signed out everywhere.” Do not replace central logout with local-only menu dismissal. Existing settings' sign-out label should use this truthful outcome.

Recovery should preserve existing safe in-memory inputs until redirect, but a full OIDC redirect can discard unsaved forms. Do not promise durable draft preservation. A future draft store would require content/retention/privacy design; it is excluded from UI-01 core. Discovery remains stream-bound: recovery copy explicitly differs from durable Requirements/Architecture operations.

## Background operations state machine

| Server/local observation | Display | Permitted behavior |
|---|---|---|
| Local start awaiting record | Starting / reconciling | Look up original key; unknown outcome is neither queued nor failed; no automatic new key |
| running + stage | Running, real stage and timestamps | Cancel only when allowed; never percent/ETA |
| running + cancel_requested | Cancellation requested (server record may race to completion) | Disable repeat cancel until authoritative refresh; close/navigation only detach observer |
| completed | Completed; open result if allowed | Run completion is not approval; result revision can be absent for some actions |
| failed | Failed + safe reason/code | Explicit studio retry with new key when allowed and input recoverable |
| failed + INTERRUPTED | Failed — interrupted | No resume; explicit retry is a new execution after reconciliation |
| cancelled | Cancelled | Explicit retry if allowed; not automatically resumed |
| Poll failure/offline | Last known state + Status unavailable/stale | Backoff read polling; do not change server outcome |
| Forbidden/missing record | Unavailable or not found | Stop revealing row details; do not manufacture a terminal outcome; refresh authorization/context |

Operation states queued/waiting/paused/interrupted-as-distinct/resuming are not added. Waiting for clarification belongs to the owning studio's session state. Existing allowed actions are cancel/retry/open_result, and cancellation additionally enforces requesting-human rules server-side; if row metadata cannot prove requester, server denial remains authoritative and is handled safely.

Use existing tracker polling interval/backoff (healthy 2 seconds, up to 30 seconds with jitter on errors); no new drawer-specific timer. Cancel/retry/open actions route to the owning project/studio, not whatever project is selected in the header. Activity remains Requirements/Architecture only, newest ≤100 records. No logs panel is promised by stage fields alone. Startup/shutdown interruption marks failed; the existing in-process execution model is not redesigned here.

## Existing API reuse and gap analysis

Paths below are relative to existing same-origin `/api/v1`. Contract snapshot is Project Service `0.11.0` from audit E12; endpoint schemas remain version-owned by masd-contracts. No new contract version is published by a design PR.

| API / adapter | Existing reuse in UI-01 | Authorization / failure concerns | Classification |
|---|---|---|---|
| `GET /auth/config`; configured login URL; `GET/POST /auth/session`; `POST /auth/logout` | Login/session/recovery/logout | Config mode controls UI; cookie/CSRF; same-origin safe return; no social provider inference | Existing/API reuse |
| `GET /projects?offset=&limit=`; `GET /projects/:p` | Home, picker, context, dashboard | Authorized pagination; project status active/archived; 401/403/404 distinct | Existing/API reuse + UI-only picker |
| `POST /projects`; `PUT /projects/:p`; `POST /projects/:p/archive` | Preserve create/edit/archive | Owner/tenant and model consent; no idempotent-create claim; uncertainty reconciled before retry | Existing/API reuse |
| `GET /models`; `GET /capabilities` | Create/edit model choices, settings/provider limits | No browser credentials; no automatic fallback; availability failure preserves metadata access | Existing/API reuse |
| `GET /projects/:p/operations` | Project history | Currently bounded, not all-account complete; status filter four actual states | Existing/API reuse |
| `GET /projects/:p/{requirements|architecture}/sessions/:s/operations[/:id]`; POST `.../:id/cancel` | Follow/query/cancel | Request-key reconciliation; requester restriction; allowed actions; conflict races | Existing/API reuse |
| Existing studio command APIs (RequirementsApi/ArchitectureApi) | Retry via owning studio | Original outcome resolved, new key explicit retry; expected versions/provenance preserved | Existing/API reuse; no generic retry endpoint invented |
| Existing project conversations, typed studios and artifact routes | Dashboard links only | Preserve approved PRD/canonical architecture constraints, artifact kind boundaries and existing imports/exports | Existing; detailed studio design out of scope |

| Gap ID | Capability absent from current boundary | Design disposition / owner / dependencies |
|---|---|---|
| AP01 | Cross-project/all-account operation feed with pagination | Excluded core; optional additive contract → Project Service authorization/query → web; no fan-out claiming completeness |
| AP02 | Durable Discovery/background chat activity | Separate contract/backend design with Project Service execution ownership, cancellation/partial-output/idempotency/reconnect tests; no new service assumed |
| AP03 | Measured percentage/ETA, logs, persisted queue or generic resume | Excluded; require measurable backend semantics, redaction/retention and versioned contract before any display |
| AP04 | Editable profile, avatar, roles, account security | Excluded; identity-provider/domain ownership and consequential permission/security decisions first |
| AP05 | Search/inbox/share/team/favorites/server filter | Excluded; scoped product/authorization/query contracts required. UI local filtering explicitly names loaded scope |
| AP06 | Dashboard lifecycle/agent/repo/task/defect metrics or approvals inbox | Excluded; canonical owner, evidence source, pagination, permission and aggregation semantics required; unavailable never zero |
| AP07 | UX artifacts/approvals, executable plan, Development/QA/Release/production workflows | Future modules only; separately approved domain design and baseline dependencies; no API/framework/service implied |
| AP08 | Guaranteed creation retry/draft restoration across redirects | Excluded guarantee; project create idempotency or draft retention would require reviewed contract/backend/content policy changes |

If optional gaps are later authorized, publish immutable additive contract versions before service and web consumers; retain old endpoints and tolerate optional fields. Existing independently built/deployed repositories remain intact. No database migration is necessary for proposed core shell UI; any later migration/config/deployment uses its own approval gate.

## Detailed journeys

| ID | Trigger → actions → outcome | Recovery / acceptance |
|---|---|---|
| UJ01 First arrival | Guarded deep link → session check → configured SSO/development login → safe authorized return | Provider unavailable offers retry; denied project falls back to safe Projects choice, never data leakage |
| UJ02 First project | Successful empty Projects → Create → fill current context/model fields → explicit provider allowlist → confirmed create → refreshed list → Open dashboard → Discovery | Missing model blocks creation with explanation; failed/unknown POST retains input and reconciles list; no automatic provisioning |
| UJ03 Existing project | Home page/filter → open project → dashboard → edit context/save → studio navigation | Server response updates name everywhere; dirty leave can cancel; archive stays read-only/history retained |
| UJ04 Switch while working | Open picker → select B → leave guard → authorize B → equivalent destination without A child IDs | Decline or failure retains A; raced reads ignored; A's server-owned operations remain followed under A |
| UJ05 Background run | Existing studio starts durable run → navigate to B/reload → followed drawer → open A's session/result | Read-only reconnect; cancellation race authoritative; explicit new-key retry only after known failure, no fake percentage |
| UJ06 Expiry/identity change | API 401 → masked recovery → configured sign-in → authorize safe return → refresh context/operations | Same identity reconciles; different identity clears old state; uncertain mutations not replayed; Discovery limitation disclosed |
| UJ07 Appearance/mobile | Choose System/Dark → resize/open drawer → choose destination → close overlay | Theme does not modify data; denied storage works in memory; keyboard/focus retained, no stuck inert background |
| UJ08 Future module | Future label → unavailable explanation → Back to dashboard/Open Architecture | No generation/approval request; no milestone date promise; preserved legacy aliases still resolve |

## Editable diagrams

- [Shell architecture](diagrams/shell-foundation.puml).
- [Authentication/recovery sequence](diagrams/auth-recovery.puml).
- [Project switching sequence](diagrams/project-switch.puml).
- [Durable operation observer sequence](diagrams/operation-observer.puml).
- [Operation state diagram](diagrams/operation-state.puml).

Sources are editable PlantUML; diagram rendering evidence is tracked separately from the design's future runtime/browser acceptance.

All five sources were rendered and visually inspected with the existing local PlantUML extension jar. [Rendered previews](diagrams/rendered/) accompany the editable sources; render evidence and tool version are in the handoff. No new runtime dependency was installed.
