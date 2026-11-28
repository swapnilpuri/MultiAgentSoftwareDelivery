# UI-01 page inventory and functional specifications

**DRAFT — detailed design v0.2, 2026-11-28.** Foundations F1–F7 approved; these detailed specifications await baseline approval. [Shell control contracts SH01–SH18](SHELL_FUNCTIONAL_DESIGN.md) and [navigation/compatibility map](NAVIGATION.md) are normative dependencies. Written specifications govern conflicts with historical mockups.

## Inventory and common contract

| WF | Page / variant | Entry / route | Exit / scope |
|---|---|---|---|
| 001 | Login | `/signin`; guarded deep-link return | Configured authentication → safe return or Projects |
| 002 | Home / Projects | `/projects`, root redirect | Create inline, dashboard, Discovery; global list |
| 003 | Create project | Inline form on `/projects`; no new creation URL required | Successful list refresh, explicit Open dashboard; guarded cancel |
| 004 | Expanded application shell | All authenticated routes | Shared navigation; no separate shell page |
| 005 | Project Dashboard | `/projects/:projectId` | Existing studios/artifacts/activity; project settings/edit/archive |
| 006 | Collapsed shell | Same routes as expanded | Local presentation variant, not a new route |
| 007 | Background operations | Header drawer + `/operations` or project activity | Owning studio/session; followed versus project history clearly distinguished |
| 008 | Project switcher | Header overlay | Same implemented destination in target project or dashboard fallback |
| 009 | Profile / settings | User menu and `/settings` | Read-only identity; appearance; existing model/provider/project settings |
| 010 | Dark theme | Same routes, local appearance preference | No semantic/content change |
| 011 | First-time workspace | Successful authorized empty Projects response | Create project; Settings; no tour dependency |
| 012 | Session recovery | Expiry overlay/public recovery then `/signin` | Authorized safe return; no automatic command replay |
| 013 | Responsive shell | Same routes at viewport breakpoints | Drawer/rail/expanded layout; all critical functions reachable |
| 014 | Future/unavailable module | Additive project-scoped future route, if approved | Dashboard/Architecture; no execution or approval mutation |

All authenticated rows inherit C0 in the shell specification: server ownership/tenant checks, separate 401/403 handling, guards, no client-only authorization. Mutation controls require active authorized project where applicable. “R” below means existing functionality/API reuse; “U” UI-only design; “F” future; “H” human decision. No schema/backend change is required by the core UI-01 presentation. Future/gap work is listed separately in TECHNICAL_DESIGN.md.

Every table row defines purpose/action, data, authorization (Auth), navigation (Nav), loading (L), error (E), empty (Ø) and acceptance (AC). “Local” has no server loading/empty state; request/navigation errors still follow C0. Associated shell controls are incorporated by reference, including all their states. Grouped controls share the same contract except where explicitly differentiated. Significant controls depicted only in historical mockups and excluded from this baseline appear in the final table.

## WF-001 — Login

Public brand/illustration and one configuration-driven authentication region. Do not present providers from a hardcoded marketing list. Existing `Auth.config`, `Auth.load`, `safeReturn`, fixed callback error messages, password and logout behavior remain the boundary.

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| LG01 SSO sign-in (R/U) | `/auth/config` mode=oidc/login_url; public; same-origin entry with safe return | L Checking sign-in options; disable during handoff. E fixed provider/callback error, allow explicit retry. Ø missing/invalid config = unavailable, no password fallback | Only configured OIDC entry is offered; arbitrary redirect target rejected |
| LG02 Username/password (R) | mode=password only; public POST session + CSRF; return after accepted identity | Required username and password, correct autocomplete; password masked. L pending disables duplicate submit. E generic failed sign-in, preserve username, clear secret. Ø blank fields prevent submit | Never shown alongside OIDC; secret absent from logs/storage |
| LG03 Retry configuration / authentication (R) | Existing Auth config/session reads; public; stay on sign-in | Reattempt failed read/handshake only, no silent account fallback. L Checking; E retained fixed message; Ø no config unavailable | Retry cannot send a password to an unconfigured provider |
| LG04 Continue (R) | Accepted session identity; Nav safe return | Only for confirmed signed-in human; reauthorize destination. L route status; E route Retry; Ø identity absent hides Continue | Old/foreign project ID cannot bypass server checks |
| LG05 Configured help/legal links (U/H) | Verified public support/privacy/terms URLs only; normal navigation | Show only approved configured destinations; absent = omitted. L/E belong to navigation, Ø omit | No dead link, unverified security promise or invented policy |

## WF-002 and WF-011 — Home and first-time workspace

Single Home / Projects heading. Show authorized project name, description/default-model/status metadata and existing Open actions. No fabricated lifecycle summary. Empty workspace is the successful zero-project state, not a loading/error substitute. Persist current selected project only as context for future project links; Home title/list remain global.

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| HM01 Create / close form (R/U) | Local form, authenticated; stays `/projects` | Open existing form; closing dirty form asks discard. L no request; E form errors stay visible; Ø create unavailable if model requirements unsatisfied | Merely opening/closing does not create a project |
| HM02 Project name / Open dashboard (R) | Authorized paginated Projects response; `/projects/:id` | L metadata placeholder + route status; E retry list/load; Ø successful empty → WF-011 | Name/status originate in response; no stale rows from prior identity |
| HM03 Open Discovery (R/U) | Project ID; `/projects/:id/chat`; owner/tenant | Existing navigation, never auto-generates. L route status; E retry; Ø no projects omit | Existing conversation/source behavior unchanged |
| HM04 Previous/Next or Load more (R/U) | offset/limit/total (currently 30/page); same list | Announce visible range, disable invalid boundaries; generation token rejects stale page response. L pending; E retain previous page with stale/error label; Ø no next page disables action | Counts describe returned scope/total, not inferred active/completed projects |
| HM05 Filter loaded projects / clear (U) | In-memory loaded page(s), name/description only; local | Label scope, clear restores loaded rows; not global search. L disabled until data; E list error independent; Ø No matches on loaded projects | Query cannot imply server-wide results; no unsupported domain/owner filter |
| HM06 Empty-state Create / Settings (U/R) | Successful zero items and total=0; `/projects` form or `/settings` | Clear welcome/next action; no video/skip/tour. L withheld during fetch; E error with Retry, not welcome; Ø welcome is this state | A 503 or forbidden list never renders first-time success |

## WF-003 — Create project

Reuse `ProjectForm` and `ProjectInput`; preserve all existing data controls. Form is not an AI provisioning wizard. Existing UI limits below are source observations, not a new API contract; backend validation remains authoritative. Keep length helpers consistent with contract semantics; do not extend chat capability limits to project fields without evidence.

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| CR01 Name (R) | ProjectInput.name; authenticated creator; local until save | Required trimmed nonblank, current UI max 120. L form available while model catalog loads; E field message; Ø required | Whitespace-only or overlength name cannot submit; inputs retained on refusal |
| CR02 Description / goals / requirements / technology preferences (R) | Matching ProjectInput fields; same Auth; local | Optional strings; current UI ceilings 4000/8000/16000/2000 respectively. L local; E associate server/field validation; Ø empty allowed | No new domain taxonomy or required description invented |
| CR03 Default model (R) | `/models` id/provider/display/availability/streaming; same Auth | Required available streaming model; do not silently change selection. L loading catalog; E unavailable catalog with Retry; Ø no eligible model disables create | Existing projects remain accessible if catalog fails |
| CR04 Allowed models (R) | `allowed_model_ids`, catalog; same Auth; local | Explicit provider authorization; default must be included, no automatic fallback. L/E as catalog; Ø no selection prevents submit while explaining default requirement | No hidden provider consent; unavailable saved model retains identity with reason during edit |
| CR05 Create project (R/U) | POST `/projects` ProjectInput; server ownership; remain list after successful creation | One submit, busy label; on confirmed response close form and refresh list, optional explicit Open dashboard. E retain inputs; unknown network outcome → reconcile list before offering another create. Ø invalid/default not allowed disables submit | No automatic repositories, agents, pipelines or team creation; no duplicate automatic POST after timeout |
| CR06 Cancel / leave (R/U) | Form dirty state; authenticated; previous Projects view | Explicit discard confirmation for dirty edits; refusal retains all data. L no server request; E unresolved create reconciled, not erased; Ø clean closes immediately | Switch/sign-out uses same leave decision; confirm causes no delete/API call |

## WF-004 / WF-006 — Expanded and collapsed shell

All controls SH01–SH18 apply. The expanded shell is the default desktop layout. Collapse changes presentation only; the selected project, route, operation tracking and permissions remain unchanged. Every rail icon has the same accessible name, Future qualification and navigation contract as the expanded row. A separate tooltip cannot be the only accessible label. Settings remains account-level; page-specific context remains explicit. No second Home destination, additional shell-only credential prompt or generic Ask AI control is introduced.

## WF-005 — Project Dashboard

Top: project title, description, active/archived state, known metadata and existing studio/resource links. Body: project overview and a collapsible Project settings region preserving the current edit form and archive action. Optional capability overview labels availability, never lifecycle completion. Do not compute project completion from visits, number of artifacts or successful operations. No new dashboard aggregation endpoint is required by this design.

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| DB01 Open Discovery / Requirements / Architecture / Artifacts / activity (R/U) | Authorized project ID; existing routes; C0 | Navigation only; no start/approval effects. L page/read loading; E per region retry; Ø missing artifacts represented by owning library | Typed architecture and Markdown architecture artifacts remain distinct |
| DB02 Project settings disclosure (U) | Current Project + models; active owner; local expansion | Reuse all CR01–04 fields, shown read-only archived. L model fetch independent; E metadata still visible on catalog failure; Ø blank optional values = Not provided | Restyle cannot remove editable goals/requirements/allowed-model fields |
| DB03 Save project settings (R) | PUT `/projects/:id`; active project owner | Prevent parallel save/archive; use returned project to update context/name. L Saving; E keep draft and old server snapshot; Ø invalid form prevents request | Server-confirmed name updates selector/breadcrumb atomically; no privilege change |
| DB04 Archive project (R/U) | POST `/projects/:id/archive`; active owner | Explain read-only consequence and ask named confirmation; actual mutation is future implementation only. L pending disables save/archive; E keep active data and refresh on uncertainty; Ø already archived hides mutation | Only confirmed server response marks archived; history remains accessible |
| DB05 Future capability item (U/F) | Navigation availability map; project access; unavailable view | Explicit Future explanation, no generation action. L local/route; E route failure; Ø no capability hides no existing backed link | Visiting cannot claim approved milestones or initialize agents |

## WF-007 — Global background operations

Header drawer lists this tab's followed authorized Requirements/Architecture operations across projects; each row includes its owning project and studio. Header count is followed active operations only. History is separately project-scoped and bounded to the newest 100 current contract records. The scopes must not be conflated.

SH08–SH12 define Open, Cancel, Retry and history controls with full state/authorization contracts. Additional controls:

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| OP01 Drawer Close (U) | Local; C0; current route unchanged | Close observer only, restore trigger focus; Escape same. L/E/Ø N/A | Closing never cancels or retries an operation |
| OP02 History project / status filters + Refresh (R/U) | Authorized project list and four persisted status values; read project activity | L pending read, disable duplicate refresh; E stale results labeled; Ø successful no records distinct from denied/offline | No Queued/Waiting/Paused filter without a contract; switch cannot mix project histories |
| OP03 Dismiss terminal followed row (R/U) | Tracker terminal state; C0; local removal | Remove from followed list only, never server history. L local; E polling failure does not make run terminal; Ø last removal shows scope-specific empty | Running/uncertain records cannot be dismissed as completed |

## WF-008 / WF-009 / WF-010

WF-008 controls are SH02–04 plus HM04/05 for pagination and explicitly local filtering. Apply the coordinated switch transaction in TECHNICAL_DESIGN.md; old child IDs are never reused in the target project. Cancelled leave or failed target read preserves the original route/context.

WF-009 controls are SH13–15 plus existing Settings surfaces below. Account details are read-only values from the actual session, not the generic illustrative text in the image. `/settings` remains one route; in-page Account details, Appearance, Models and Project settings regions use anchors/disclosures. The mockup's “Open existing settings” refers to the existing models/provider region, not a new settings route or self-loop.

| ID / control and purpose | Data / Auth / Nav | Behavior and states | AC |
|---|---|---|---|
| ST01 Account details / models region links (U/R) | Current session and `/models`/`/capabilities`; C0; same `/settings` anchor | Scroll/focus target region, no redundant nested settings page. L independent session/model reads; E retry failed region; Ø no models explains provider setup | Preserve provider statuses, configured limits and availability/reasons; never expose credentials |
| ST02 Edit project settings (R) | Current authorized context; dashboard settings region | No project → Choose project; L context read; E safe context failure; Ø no selection guidance | No project-account permissions editor implied |
| ST03 Retry model/provider reads (R) | Existing APIs; C0; stay settings | Read retry only; L pending; E retained reason; Ø configured list empty explicit | Cannot silently reroute data to another provider |

WF-010 uses SH14 and the same page control contracts; dark theme is not another route, permission set or data snapshot. Light and dark screenshots use identical deterministic fixtures. Preference may persist locally even if storage is disabled only for the current page, with no claim of account-wide synchronization.

## WF-012 — Session recovery

Use SH16 for expiry/reauthentication. Protected page content is masked; only MASD brand and recovery UI remain readable. Copy says “Your session ended,” not a guessed cause. “Sign in again” invokes configured auth with safe return; optional “Go to sign-in” opens `/signin` without retaining a private return target. Neither issues a studio command. L configuration/handshake pending; E service unavailable offers retry; Ø no valid config shows unavailable. AC: no authenticated project metadata leaks in the recovery screenshot; after login only same-user authorized data may reappear. Runtime behavior needs new browser verification; the image is not security evidence.

## WF-013 — Responsive shell

SH02/06/08/13 apply to every viewport. Desktop collapse, tablet overlay and mobile modal are local variants of the same control contract. Menu/Close purpose is to expose/dismiss navigation, not change context; no server load/empty, navigation errors remain page-level. At mobile widths project selector and operations can occupy a second header row; identity remains accessible. In the illustrative board the four content labels represent navigation to existing destinations, not a new dashboard tab data model. Only one route has `aria-current`; cards need no redundant selected tab state in implementation.

AC: all navigation including Future explanations accessible by keyboard/touch; modal focus/inert state released on close, resize and route change; 320px reflow and zoom; no additional scroll lock remains after navigation. Collapsed Future icons include Future in accessible names even when the rail cannot display the word.

## WF-014 — Unavailable/future modules

Selected Future destination has heading, availability explanation, no executable controls/date promises. Back to dashboard uses authorized project `/projects/:id`; Open Architecture uses `/projects/:id/architecture`; L route status, E retry/denial, Ø no project → choose project instead. Both are same-app links. Prerequisites are explanatory; this view cannot approve a UX artifact. Existing shared inbox/agent aliases retain legacy targets; new unavailable project routes must be additive and reviewed.

## Explicitly excluded historical controls

| Historical control | Classification / disposition | Reason / acceptance |
|---|---|---|
| Google/Microsoft/GitHub alternatives, remember-me, forgot-password, signup | F/H, absent | No separate frontend provider/account recovery contract; configured OIDC handles identity-provider capabilities |
| Repository/CI/agent/team/sample-data setup, project auth selector, domain taxonomy | F/H, absent | Existing project creation creates metadata only; no new setup backend approved |
| Global search, notification bell/inbox, product tour video, Share/team invites | F/H, absent | Missing scoped APIs/verified destinations; not decorative functional buttons |
| Pause/resume, ETA/percent, UI generation run, all-account operation totals | F/additive API/backend, absent | Current state/action contracts cannot support claims |
| Edit identity/role/avatar/password/security | F/additive API/backend, absent | No identity/privilege mutation API; read-only account display preserved |
| New Task, Ask MASD globally, code/QA/release agents or progress metrics | F/H, absent | Requires approved execution domains; existing Discovery/studio routes remain available |

Absence is intentional baseline scope, not removal of existing backed studio functionality. Detailed Discovery/other studio design remains out of scope.
