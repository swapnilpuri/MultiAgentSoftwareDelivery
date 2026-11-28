# UI-01 detailed functional and technical design — v0.2

**DRAFT — foundations F1–F7 approved; complete design baseline not approved.** M3.1B.2, draft package revision v0.2, 2026-11-28 (America/Chicago).

This package continues the approved foundations into a full UI-01 design proposal: all 14 screen specifications, seven independently regenerated wireframes, technical state/API design, editable diagrams, acceptance/traceability and a proposed implementation plan. All detailed artifacts and images remain DRAFT pending explicit whole-baseline approval. No application code, M3.2 implementation prompt, M3.2 implementation or M4 work is included.

Review in order:

1. [Reference and wireframe reconciliation](RECONCILIATION.md): reviewed evidence and corrections for all 14 screens.
2. [Proposed final navigation](NAVIGATION.md): destination hierarchy, availability and compatibility.
3. [Application design system foundation](DESIGN_SYSTEM.md): light/dark tokens, typography, layout and shared interaction rules.
4. [Shared shell functional design](SHELL_FUNCTIONAL_DESIGN.md): control behavior, authorization, data, failure states and acceptance.
5. [Editable shell architecture](diagrams/shell-foundation.puml).
6. [All 14 page specifications](PAGE_SPECIFICATIONS.md).
7. [Technical design and journeys](TECHNICAL_DESIGN.md).
8. [Acceptance, traceability and Playwright strategy](ACCEPTANCE_AND_TRACEABILITY.md).
9. [Proposed M3.2 plan](M3_2_PROPOSED_PLAN.md) — not an implementation prompt.
10. [Seven standalone redraws v0.3](../wireframes/UI-01/v0.3/WIREFRAME_INDEX.md), with exact prompts and checksums.
11. [Artifact manifest](ARTIFACT_MANIFEST.md) and [documentation publication prompt](CODEX_PUBLISH_PROMPT.md).
12. [Milestone handoff](../../milestones/M3_1B_2_HANDOFF.md): verification, blockers and resume commands.

## Foundation decision record

| ID | Recommendation | Approval status |
|---|---|---|
| F1 | One Home / Projects destination; project dashboard and lifecycle/shared groups; use the exact vocabulary in NAVIGATION.md | Approved 2026-11-27 |
| F2 | Separate Background operations (AI execution activity) from future Production Operations; preserve legacy route meanings | Approved 2026-11-27 |
| F3 | Violet shell, neutral working canvas, semantic light/dark tokens and system font stack; retain preferred reference composition | Approved 2026-11-27 |
| F4 | Keep existing configuration-driven sign-in, per-tab authorized project context, guarded navigation and server operation actions | Approved 2026-11-27; existing behavior remains authoritative |
| F5 | Hide unsupported global search/notifications and speculative dashboard metrics; label future modules explicitly | Approved 2026-11-27 |
| F6 | Use a single HRMS Platform sample fixture for later renders, marked illustrative; no fictional execution/approval evidence | Approved 2026-11-27 |
| F7 | Preserve original images; generate seven independent redraws in an additive revision after foundation review | Approved 2026-11-27; seven standalone redraws produced |

The user explicitly approved F1–F7 on 2026-11-27 with “Approve F1-F7.” This approves the foundation recommendations recorded in commit `865659e0bb56808af1138a0221670b7f267b183f`, including additive redraws. It satisfies the initial foundational review gate. It does not approve the complete UI-01 baseline, accept M3.1, or authorize application implementation, M3.2 or M4. Remaining detailed artifacts stay DRAFT pending review.

## Revision and review status

| Revision | Status / change | Dependencies |
|---|---|---|
| v0.1 foundation (`865659e`) | F1–F7 explicitly approved by user; review checkpoint satisfied | Main `1cfe56f`; mandatory references and targeted source reads |
| v0.2 detailed design | DRAFT; page/control/API/state/journey/acceptance/plan proposal, five editable diagrams | Approved F1–F7; no new seven-repository audit |
| Wireframes v0.3 | DRAFT; WF-008–014 independent full-resolution generations, original images preserved | REF-01–03 and written foundations; built-in imagegen, per-screen corrections |

All twenty requested design deliverables are mapped in the [traceability matrix](ACCEPTANCE_AND_TRACEABILITY.md). Human functional/visual baseline review is outstanding. Historical WF-001–007 remain unchanged; written reconciliation governs their conflicting controls/data. Accept that precedence or request additive corrected renders during baseline review. No browser implementation acceptance is claimed. The downloadable archive is a design distribution artifact; its SHA-256 sidecar is supplied separately. Merging a documentation PR is not design approval.

After explicit whole UI-01 baseline approval, preparation of an M3.2 implementation prompt becomes eligible; none is included here. Actual implementation, deployment/migration/permission changes and M4 retain their separate authorizations.

## Evidence and preservation

Central main was fetched on 2026-11-27 at `1cfe56fa37879be7e01b23185559eb9c8a7e313b` (merge of PR #28). Its tree matches the previous local wireframe branch. The existing [audit](../IMPLEMENTATION_AUDIT.md) remains the seven-repository evidence register; it was not repeated. Targeted local Angular and Project Service reads supplement it; see RECONCILIATION.md. Historical indexes, images, provenance and milestone records are preserved.
