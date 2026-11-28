# M3.1B.2 UI-01 detailed design handoff

**DRAFT — foundation checkpoint F1; awaiting human foundational review.** Date: 2026-11-27 (America/Chicago). No baseline approval, application changes, M3.2 implementation prompt/implementation or M4 authorization.

Base/current main at entry: `1cfe56fa37879be7e01b23185559eb9c8a7e313b`, fetched from origin, merge of M3.1B.1 PR #28. Branch: `docs/m3.1b2-ui01-foundations`. Current commit: `git rev-parse HEAD` (this handoff cannot self-pin its eventual commit). Initial working tree clean; no pre-existing changes overwritten. Existing main tree matched the preceding local wireframe branch.

## Completed work and decisions

[Foundation README](../04-ui-ux/UI-01/README.md) is the review entry point and tracks F1–F7 recommendations plus remaining deliverables. Reviewed mandatory references and all 14 screen images plus REF-01–04. Reused M3.1A seven-repository audit with targeted Angular/auth/context/operations source checks. Produced per-screen reconciliation, proposed navigation/route compatibility, design tokens/shared guidelines, shell control contracts/acceptance, and editable PlantUML architecture.

Key proposals: single Home / Projects; stable legacy paths; distinct Background operations and future Production Operations; configuration-driven sign-in; no fabricated progress/agents/approvals; read-only identity; local light/dark/system theme. All are review proposals. No human approval is recorded. All historical images/provenance/handoffs are preserved; no seven-repository audit was repeated.

## Verification

Executed at this checkpoint:

| Command / check | Result |
|---|---|
| `uv run --frozen python -m scripts.check` | PASS: governance, Ruff lint, format (84 files), mypy (6 source files), **46 passed**, secret scan 0, no known dependency vulnerabilities |
| `uv run --frozen python scripts/validate_standards.py` | PASS: pinned standards integrity |
| Temporary inline Python documentation check | PASS: six DRAFT Markdown files, 22 relative links, 14 reconciliation IDs, 18 shell control IDs, eight compatibility route/alias mentions |
| Temporary inline Python contrast arithmetic | PASS: 17 specified text pairs ≥4.5:1 (minimum 5.98:1); four control-boundary pairs ≥3:1 |
| `git diff --check` | PASS |
| Original visual reference inspection | All 14 screen PNGs and four reference PNGs opened visually |

Initial sandbox standards attempt was BLOCKED by uv cache permissions before validation; the authorized rerun passed. No failed check remains. Inline validation was executed with `python -` using pathlib/re for Markdown links/coverage and sRGB relative luminance for contrast; no runtime/test source files were added. Contrast arithmetic covers specified solid token pairs, not every composited/interactive browser state.

No runtime, Playwright, visual acceptance or live-provider test is claimed. Image review means the original PNGs were opened and inspected, not that new designs passed acceptance. PlantUML rendering is **not executed** (no PlantUML command found); editable source is provided, rendering remains a later validation item. Publication/PR review is not executed at this local foundation checkpoint; historical Sourcery budget exhaustion is not a current review result. Any future PR must inspect current findings/checks before publication completion.

## Risks, blockers and next task

Human foundation review is required by the user's explicit incremental design instruction. WF-008–014 still require seven independent full-resolution redraws; no regeneration is claimed. Complete page specifications, journeys, API/state/sequence detail, full traceability, Playwright strategy, proposed M3.2 plan and completed downloadable ZIP remain later slices. Do not package this checkpoint as the completed design. M3.1 acceptance remains separate.

Next task: obtain feedback on F1–F7; then use imagegen skill and preferred references to produce additive redraws and reconcile all 14. Continue remaining design slices incrementally. Complete design publication uses a documentation-only PR and final ZIP with README, ARTIFACT_MANIFEST, CODEX_PUBLISH_PROMPT, revisions/dependencies/SHA-256. Resolve applicable PR findings; do not merge automatically. Baseline approval precedes any implementation prompt.

Resume:

```powershell
git status --short --branch
git rev-parse HEAD
Get-Content docs/04-ui-ux/UI-01/README.md
uv run --frozen python scripts/validate_standards.py
```
