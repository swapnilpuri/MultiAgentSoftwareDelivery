# UI-01 v0.2 publication record — DRAFT

Status: **DRAFT — interim archive for human review; not approved for implementation.** M3.1B is not completed or approved. This publication neither starts M3.2/M4 nor accepts M3.1. All screen, alternative and reference PNGs inherit DRAFT status, regardless of labels depicted inside them.

## Source and baseline

The requested extracted directory `C:/Projects/MASD_UI_01_Wireframes_v0.2/` was absent. The supplied ZIP `C:/Users/Owner/Downloads/MASD_UI_01_Wireframes_v0.2.zip` was extracted into a temporary directory. Its nested `MASD_UI_01_Wireframes_v0.2/` is the package root. Only the wireframe subtree and three provenance documents were imported; no root repository instructions or README were replaced.

Remote `main` and merged [M3.1A PR #27](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/27) both identify baseline `59aa92981e658d507c4295a1d6d0c72c79916fc3`. The active checkout initially had `88e98485834139eaf71efd01f9d72648e94b53fb`; it was clean, and the new branch starts at current remote main. No drift from PR #27 was found. Existing historical artifacts remain in place; the two existing indexes receive additive links only. Historical manifest hashes describe original imported bytes, before these index additions.

## Navigation and provenance

- [Screen index and dimensions](WIREFRAME_INDEX.md): WF-001 through WF-014.
- [References](references/): four original preferred boards, including REF-04 complete storyboard.
- [Alternatives](alternatives/): six additional violet concepts.
- [Original package manifest](provenance/ARTIFACT_MANIFEST.md): 27 SHA-256/byte records.
- [Original package README](provenance/README.md) and [publishing instructions](provenance/CODEX_PUBLISH_PROMPT.md).
- [Parent artifact index](../../ARTIFACT_INDEX.md), [historical wireframe index](../../WIREFRAME_INDEX.md), [M3.1B handoff](../../../milestones/M3_1B_HANDOFF.md).

Manifest paths are relative to the **source package root**, not to its archived location in `provenance/`. Map `CODEX_PUBLISH_PROMPT.md` and `README.md` to their copies in `provenance/`; map `docs/04-ui-ux/wireframes/UI-01/...` directly from the repository root. The manifest itself is not self-hashed. Source subtree bytes, including its screen index, are preserved exactly.

## Review constraints and regeneration

**WF-008 through WF-014 are storyboard-derived images requiring standalone full-resolution regeneration.** They are native-resolution crops of REF-04, sized 350–559 pixels wide and 206–264 pixels tall, rather than standalone screen renders. The supplied screen index records each exact dimension. WF-001 through WF-007 are standalone drafts, still subject to reconciliation and review. This archive is not the complete UI-01 specification package.

All data, metrics, agent activity, provider buttons, progress percentages and repository controls are illustrative. Branding, navigation, stage labels and sample data vary between drafts. Reconcile these against the written baseline and verified capabilities before approval; the images are not runtime evidence. No application code, service boundary, backend capability or implementation authorization changes here.

Validation and PR review outcomes are recorded in the [handoff](../../../milestones/M3_1B_HANDOFF.md). Human design review, standalone regeneration and reconciliation remain open.
