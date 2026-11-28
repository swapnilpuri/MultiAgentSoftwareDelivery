# UI-01 detailed design — foundation checkpoint v0.1

**DRAFT — human review required.** M3.1B.2, checkpoint F1, 2026-11-27 (America/Chicago).

This is the first reviewable slice of the requested UI-01 detailed functional and technical design. It proposes foundational decisions, rather than an approved design baseline. Violet is the selected direction; exact tokens, navigation and behavior below are proposals. No application code, M3.2 implementation prompt, M3.2 implementation or M4 work is included.

Review in order:

1. [Reference and wireframe reconciliation](RECONCILIATION.md): reviewed evidence and corrections for all 14 screens.
2. [Proposed final navigation](NAVIGATION.md): destination hierarchy, availability and compatibility.
3. [Application design system foundation](DESIGN_SYSTEM.md): light/dark tokens, typography, layout and shared interaction rules.
4. [Shared shell functional design](SHELL_FUNCTIONAL_DESIGN.md): control behavior, authorization, data, failure states and acceptance.
5. [Editable shell architecture](diagrams/shell-foundation.puml).
6. [Milestone handoff](../../milestones/M3_1B_2_HANDOFF.md): verification, blockers and resume commands.

## Foundation decisions submitted for review

| ID | Recommendation | Approval status |
|---|---|---|
| F1 | One Home / Projects destination; project dashboard and lifecycle/shared groups; use the exact vocabulary in NAVIGATION.md | Proposed |
| F2 | Separate Background operations (AI execution activity) from future Production Operations; preserve legacy route meanings | Proposed |
| F3 | Violet shell, neutral working canvas, semantic light/dark tokens and system font stack; retain preferred reference composition | Proposed |
| F4 | Keep existing configuration-driven sign-in, per-tab authorized project context, guarded navigation and server operation actions | Proposed; existing behavior remains authoritative |
| F5 | Hide unsupported global search/notifications and speculative dashboard metrics; label future modules explicitly | Proposed |
| F6 | Use a single HRMS Platform sample fixture for later renders, marked illustrative; no fictional execution/approval evidence | Proposed |
| F7 | Preserve original images; generate seven independent redraws in an additive revision after foundation review | Proposed sequencing; regeneration remains required |

The user's instruction is: “Do not generate the entire design package before reviewing the foundational decisions.” This checkpoint intentionally stops at that gate. Explicit feedback on F1–F7 is needed before dependent page specifications and redraws. Approving these foundations alone does not approve the entire UI-01 baseline or authorize implementation. No approval has been inferred from the request, prior publication or a Git merge.

## Remaining deliverables and dependencies

| Next slice | Required output | Depends on |
|---|---|---|
| F2 wireframes | WF-008–014 standalone full-resolution images using REF-01–03; reconcile all 14 against approved foundations; record prompts, dimensions, hashes and visual QA | Foundation review |
| F3 page specifications | Complete page inventory, all 14 control specifications, detailed journeys, auth/session recovery, creation/dashboard/profile/empty/future behavior | Foundations and reconciled images |
| F4 technical design | Angular component ownership/state, API reuse/gaps and changes by repository, auth/context/operation sequences and state diagrams | F3; contract decisions |
| F5 acceptance/package | Functional/visual criteria, full traceability matrix, Playwright strategy, proposed M3.2 plan; README, manifest, publication prompt, revision and SHA-256 in downloadable ZIP | Reviewed design slices |
| Separate gate | Explicit human UI-01 baseline approval; only then may an M3.2 implementation prompt be generated | Full package review |

All twenty requested deliverables remain tracked by these slices. Current files cover the foundation portions of design system, palette/type, shared guidelines, navigation, compatibility, shell specifications, architecture and acceptance. They do **not** constitute completion of the twenty deliverables. Final ZIP packaging and documentation-only publication must preserve this hierarchy, historical assets and review findings; do not label a partial checkpoint the completed package.

## Evidence and preservation

Central main was fetched on 2026-11-27 at `1cfe56fa37879be7e01b23185559eb9c8a7e313b` (merge of PR #28). Its tree matches the previous local wireframe branch. The existing [audit](../IMPLEMENTATION_AUDIT.md) remains the seven-repository evidence register; it was not repeated. Targeted local Angular and Project Service reads supplement it; see RECONCILIATION.md. Historical indexes, images, provenance and milestone records are preserved.
