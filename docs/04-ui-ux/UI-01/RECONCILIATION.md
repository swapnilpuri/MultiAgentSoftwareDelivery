# UI-01 reference and wireframe reconciliation

**DRAFT — v0.1 foundation checkpoint; no baseline approval.** Reviewed 2026-11-27.

## Evidence reviewed

Central main: `1cfe56fa37879be7e01b23185559eb9c8a7e313b`, fetched from origin. Read root AGENTS.md, local operating model and standards manifest, ARTIFACT_INDEX, UX_BASELINE, IMPLEMENTATION_AUDIT, PROPOSED_SLICES, both wireframe indexes, M3.1A and M3.1B handoffs, UI-01 PUBLICATION and original artifact manifest. M3.1B handoff describes its publication-time open PR; current Git history proves PR #28 was subsequently merged. A merge is not design approval.

Visually opened all 14 published UI-01 PNGs and REF-01–04 individually. REF-01 contributes login composition/brand treatment; REF-02 contributes violet shell, cards and selector; REF-03 contributes lifecycle navigation, dark mode and density. REF-04 is the storyboard provenance for seven crops. Blue in REF-01 does not override the selected violet theme. Historical image bytes must remain unchanged. The original manifest remains the byte-level provenance source, not a specification of current capabilities.

Targeted source reads (no new seven-repository audit):

| Source | Evidence |
|---|---|
| masd-web at `85a0d22a6aa1f128e1cef98bf74dfa699179dee6`: `src/app/app.routes.ts`, `sections.ts`, `app.html` | Guarded routes, existing labels, aliases, shared status/context, current navigation |
| Same web revision: `auth.ts`, `sign-in.ts`, `project-context.ts` | Configuration-driven OIDC or development password sign-in; cookie/CSRF; safe return; identity reset; per-tab project IDs and stale-request protection |
| Same web revision: `workspace-api.ts`, `requirements-api.ts`, `operations.ts`, `operation-panel.ts`, `operations-page.ts`, `settings.ts` | Actual project fields, paginated listing, model configuration, operation schema/actions, followed versus project activity scope, account/session information |
| Project Service local `project_service/operations.py` | Requesting-human cancellation check; four persisted statuses; allowed actions; interruption as failure |
| Existing audit E03/E05/E10/E12 and G01/G02/G15/G16 | Pinned backend/auth/contracts evidence reused; no new claim of remote sibling freshness or runtime verification |

Source observations are static evidence. Local web HEAD matches the audit pin. Other sibling remote heads and runtime behavior were not revalidated. No current product capability is inferred from a mockup.

## Cross-screen reconciliation rules

R01: Brand text is **MASD**, expanded **MultiAgentSoftwareDelivery**. Use a single supplied logo treatment consistently after human selection; propose the violet network motif from WF-001–007. The cube in REF-02/03 and crops is a conflicting alternative, not a second product mark. Do not trace or replace repository brand assets in this documentation phase.

R02: Canonical illustrative project name is **HRMS Platform**, description “Human Resource Management System.” Optional comparison project: “E-Commerce Platform.” No real person's name/email or manually invented project ID is required. Watermark renderings “DRAFT · illustrative data.” Persisted project status is active/archived, distinct from lifecycle stage and operation state.

R03: Navigation and lifecycle names follow NAVIGATION.md. Preserve Requirements and Architecture as separate destinations. UX approval and Architecture approval are both prerequisites to future Planning; drawings must not bypass either. Availability and completion are distinct: an implemented studio is not a completed project stage.

R04: Authentication choices come from `/auth/config`. OIDC shows one SSO entry; password form is development-only when configured. No independent Google/Microsoft/GitHub/password alternatives, self-registration, remember-me, reset-password or account security editor without supporting contracts and explicit scope.

R05: Real operation states are running/completed/failed/cancelled. Interrupted is failed with an interruption reason, not resumable. Queued, waiting for input, pause and resume are future operation capabilities; clarification is session state. Use stage text and timestamps; omit percentage/ETA. Discovery is currently stream-bound and absent from global studio activity.

R06: Reuse existing authorized data. No agent/task/repository/defect counts, aggregate lifecycle percentages, simulated approvals, generated wireframe jobs, notification badge counts or automatic setup promises. An unavailable value is not zero. Counts over paginated or bounded results must state scope.

## Review of all 14 published screens

Each row is a reconciliation instruction for subsequent specifications/redraws, not a claim that the original image has been corrected.

| Screen | Observed issue | Proposed resolution / dependency |
|---|---|---|
| [WF-001 Login](../wireframes/UI-01/WF-001-login.png) | SSO plus Google/Microsoft/password; privacy/security promises and external links lack verified destinations | Keep split illustration/card composition in violet; apply R04; use configured support/legal destinations only; remove unsubstantiated security claim |
| [WF-002 Home](../wireframes/UI-01/WF-002-home-projects.png) | Selected project on all-projects view; overlapping Home/Projects/Workspace; progress and agents/repositories metrics; unsupported statuses/filters | Single Home / Projects; selected project remains visibly scoped to project links; list real metadata/status, local filters only over explicitly loaded data; no fictional insights |
| [WF-003 Creation](../wireframes/UI-01/WF-003-create-project.png) | Project auth selector, repository/CI/agent/team setup and sample-data options; domain taxonomy; hardcoded limits | Existing ProjectInput fields and configured models; preserve current required fields/validation; create project only; no setup side effects. Detailed form design pending |
| [WF-004 Shell](../wireframes/UI-01/WF-004-application-shell.png) | Search/bell/share/agent controls; inconsistent sidebar and 42% progress | Use shell control matrix; retain backed studio and artifact navigation; remove invented summaries; availability labels instead of inferred completion |
| [WF-005 Dashboard](../wireframes/UI-01/WF-005-project-dashboard.png) | 52% conflicts with other screens; 24 artifacts but eight key artifacts; code/QA agents and approvals presented as real | Metadata and backed links first; actual canonical decisions only from owning workflow; no overall percentage; complete dashboard spec after foundation review |
| [WF-006 Collapsed](../wireframes/UI-01/WF-006-collapsed-sidebar.png) | Different lifecycle and 42%; extra Ask AI/New Task; icon meanings unclear | Same destinations/content as expanded; accessible names/tooltips/focus; no New Task or global AI launch without backed destination |
| [WF-007 Operations](../wireframes/UI-01/WF-007-background-operations.png) | Pause, percentage/ETA, UI generation and Discovery runs; completed history implies global completeness | Followed-operation drawer plus explicitly project-scoped history; R05; only server-permitted actions; explain scope and bounded history |
| [WF-008 Switcher](../wireframes/UI-01/WF-008-project-switcher.png) | 350×264 crop; progress and “Planning” project status; no loading/permission behavior | Independent redraw after review; authorized paginated project list, selection checkmark and active/archived status; no lifecycle percentages |
| [WF-009 Profile](../wireframes/UI-01/WF-009-profile-settings.png) | 382×232 crop; editable role/name/email/avatar; notifications/security tabs imply APIs | Independent redraw; read-only identity/role from session, theme preference and existing settings link; no identity/privilege mutation |
| [WF-010 Dark](../wireframes/UI-01/WF-010-dark-mode.png) | 384×232 crop; different navigation and unsupported metrics | Independent redraw using the same shell/data as light, semantic token substitution only; contrast QA in both themes |
| [WF-011 First-time](../wireframes/UI-01/WF-011-first-time-workspace.png) | 376×232 crop; product tour video/settings/notifications and skip imply unavailable flows | Independent redraw; real empty-project state with Create project and existing Settings; omit unimplemented tour; distinguish fetch error from empty |
| [WF-012 Recovery](../wireframes/UI-01/WF-012-session-recovery.png) | 366×232 crop; asserts inactivity cause and signed-out state without server evidence | Independent redraw; neutral “Your session ended”; one configured reauthentication action, safe return; no promise of durable Discovery or automatic command replay |
| [WF-013 Responsive](../wireframes/UI-01/WF-013-responsive-shell.png) | 559×206 composite crop; metrics/cards too small; collapsed/overlay behavior ambiguous | Independent full-resolution responsive presentation, readable individual viewports; 1280/768 boundaries and 320px reflow; no permanently hidden critical controls |
| [WF-014 Future](../wireframes/UI-01/WF-014-future-module.png) | 503×206 crop; “coming” feature checklist can look executable; API Contracts treated as separate studio | Independent redraw; explicit unavailable explanation, no generation CTA, no promised release date; API contracts remain Architecture-owned content |

## Regeneration and review gate

Seven original crops remain unresolved visual deliverables. Do not upscale them and call that regeneration. After F1–F7 feedback, generate WF-008–014 separately using the three preferred references, at readable full-screen resolution (proposed desktop target 1600×1000; responsive states individually readable). Preserve the old revision; place new images in an additive revision with prompt/provenance/dimensions/SHA-256 and a per-screen visual check against R01–R06. Image generation must use the imagegen skill/tool. This checkpoint performs visual review and documents redraw instructions only; no new bitmap has been generated.
