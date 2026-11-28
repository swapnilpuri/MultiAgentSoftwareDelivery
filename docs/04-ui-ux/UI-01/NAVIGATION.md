# Proposed final application navigation

**DRAFT — v0.2; foundation navigation decisions F1/F2 approved, detailed baseline pending.** Navigation labels do not establish implemented capability.

## Hierarchy

```text
MASD → Home / Projects
Header: Project selector | Background operations | User menu
Workspace
  Home / Projects
  Project Dashboard [selected project]
Lifecycle [selected project]
  Discovery
  Requirements
  Architecture
  UX Design                  [Future]
  Planning                   [Future]
  Development                [Future]
  QA                         [Future]
  Release                    [Future]
  Production Operations      [Future]
Project resources [selected project]
  Artifacts
  Approvals                  [Future shared inbox]
  Agents                     [Future management]
  Background operations
Account
  Settings
```

Home and Projects are one destination. Create project is an action on Home and selector, not another permanent navigation item. Project Dashboard is unavailable until a project is selected; activation offers project selection rather than inventing a default project. “Workspace” and “Lifecycle” are group labels, not routes. No detailed studio layouts are designed here.

Requirements, Architecture, Discovery and Artifacts exist. UX Design, Planning, Development, QA, Release and Production Operations use an explicit future state. A future shared Approvals inbox does not replace existing human approval inside Requirements/Architecture/artifacts. Existing bounded agent proposals do not establish an Agents management module. API Contracts remain part of Architecture; Knowledge Base/Reports/Traceability do not become new global modules in UI-01. Preserve existing traceability inside its owning studios.

Future entries have a visible “Future” label and accessible explanation. On desktop/mobile activation they may open a read-only unavailable page after a corresponding additive route is approved; until then they are non-link explanatory items, not links through misleading aliases. No executable actions, fake counts or promised delivery dates.

## Destination and compatibility map

Parameters `:p`, `:c`, `:s`, `:a` below mean projectId, conversationId, sessionId, artifactId. Retain full parameter values, query parameters and fragments on supported deep links. Existing paths remain canonical for implemented destinations; a label change does not require URL churn.

| Label / destination | Existing path(s) retained | Change classification |
|---|---|---|
| Sign in | `/signin` | Existing auth; UI-only restyle |
| Home / Projects | `/`, `/projects` (`/` redirects) | Existing list/create; UI-only consolidation |
| Project Dashboard | `/projects/:p` | Existing detail → UI-only layout using available metadata; aggregate API gaps separate |
| Discovery | `/chat`, `/projects/:p/chat`, `/projects/:p/chat/:c` | Existing AI Workspace; UI-only label |
| Requirements | `/planning`, `/projects/:p/requirements`, `/projects/:p/requirements/:s` | Existing; `/planning` retains Requirements meaning |
| Architecture | `/architecture`, `/projects/:p/architecture`, `/projects/:p/architecture/:s` | Existing |
| Future Planning | `/delivery`, `/projects/:p/delivery` | Existing unavailable page can be relabeled; no new executable plan |
| Background operations | `/operations`, `/projects/:p/operations` | Existing AI activity; project required to load project history |
| Artifacts | `/projects/:p/artifacts`, `/projects/:p/artifacts/:a` | Existing Markdown artifact library; not canonical architecture packages |
| Settings / profile | `/settings` | Existing account/session/models/project links; profile read-only |
| UX Design / Development / QA / Release / Production Operations | Proposed `/projects/:p/ux`, `/development`, `/qa`, `/release`, `/production-operations` suffixes under the same project | Additive UI routes only after review; unavailable view, no new API/service |
| Future shared Approvals / Agents | Proposed `/projects/:p/approvals`, `/projects/:p/agents` | Additive unavailable views after review; no execution/management |

Historical aliases remain unchanged: `/approvals` → `/planning` (Requirements), `/milestones`, `/engineering`, `/deployments` → `/delivery`; `/agents`, `/observability` → `/operations`. Do not repurpose these globals for future inbox/agent/production modules. Preserve wildcard fallback to Projects; route ordering must put literal future segments before `/projects/:projectId` matching where relevant. No routes are changed in this checkpoint.

## Context rules

URL project identity wins over the per-tab remembered ID; every selection is checked through the authorized Project Service. On Home the title is global even if the selector retains a project for subsequent links. Breadcrumb: Home / Projects → project name → destination; the current crumb is not a link. A selector change first respects the existing unsaved-work guard, validates the target, then opens the equivalent implemented project destination without carrying old session/conversation/artifact IDs. Unsupported equivalents fall back to the target dashboard. Failure leaves the previous context/route intact. A user may still directly open an authorized deep link; lifecycle labels are not new blanket route locks.

Architecture/UX approval before future Planning is a domain handoff rule, not a sidebar completion inference. Run completion is not artifact approval, milestone acceptance or release authorization.
