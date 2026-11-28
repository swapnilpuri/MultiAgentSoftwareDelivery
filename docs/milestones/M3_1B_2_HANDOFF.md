# M3.1B.2 UI-01 detailed design handoff

**DRAFT — detailed design v0.2 and standalone wireframes v0.3 prepared; full baseline approval pending.** Updated 2026-11-28 (America/Chicago). F1–F7 foundations were explicitly approved by the user (“Approve F1-F7.”) against `865659e0bb56808af1138a0221670b7f267b183f`. This is not M3.1 acceptance, full UI-01 approval, M3.2 implementation/prompt authorization or M4 authorization.

## Baseline, branch and scope

- Central main/base: `1cfe56fa37879be7e01b23185559eb9c8a7e313b`; remote rechecked unchanged on 2026-11-28. Foundation commit `865659e`; current publication commit: `git rev-parse HEAD` (handoff does not self-pin its own future commit).
- Branch: `docs/m3.1b2-ui01-foundations`; active checkout `C:/Projects/msad/MultiAgentSoftwareDelivery`.
- Initial working tree was clean. A later untracked `out/docs/04-ui-ux/UI-01/diagrams/shell-foundation/` PNG/SVG preview appeared during the session; its origin is not established, so it is preserved and excluded from publication/package. No user changes were removed.
- No Angular/backend/contracts/config/permission/deployment changes. Historical images, source manifests and milestone records preserved; current UX indexes receive additive links. Existing audit reused with targeted reads; no repeated seven-repository audit.

## Completed design work and decisions

[Design README](../04-ui-ux/UI-01/README.md) is the review entry point. All twenty deliverables are mapped in [acceptance/traceability](../04-ui-ux/UI-01/ACCEPTANCE_AND_TRACEABILITY.md). Includes all 14 page/control specifications, shared shell contracts, approved navigation/token foundations, routes/compatibility, user journeys, session/context/operations/state architecture, existing API reuse and explicit AP01–AP08 gaps, five editable PlantUML sources with rendered previews, Playwright strategy and proposed M3.2 plan (not an implementation prompt).

[Wireframes v0.3](../04-ui-ux/wireframes/UI-01/v0.3/WIREFRAME_INDEX.md): seven independent built-in image_gen screen generations using preferred REF-01–03; exact prompts/correction passes, actual dimensions, bytes and SHA-256 recorded. Six are 1585×992; responsive board 1920×819. Seven outputs inspected visually; navigation/identity/internal-link and recovery-private-content errors corrected before selection. No upscaling of old crops. Original WF-001–007 remain historical pixels; written reconciliation governs their unsupported controls/data, subject to full human baseline review.

Core proposal reuses APIs; broader durability/search/metrics/account editing/execution gaps are excluded. No new microservice/framework justified. Future-module screens cannot execute or approve work. Foundation approval does not turn mockup data into runtime evidence.

## Executed verification

| Command / check | Result |
|---|---|
| `uv run --frozen python -m scripts.check` | PASS: governance, Ruff lint, format (91 files), mypy (6 source files), **46 passed**, secret scan 0, no known dependency vulnerabilities |
| `uv run --frozen python scripts/validate_standards.py` | PASS: pinned standards integrity |
| Seven PNG validation with inline Python struct/zlib/hashlib | PASS: PNG signatures/chunk CRCs/IEND/EOF and decompression; dimensions/byte counts/SHA-256 recorded in v0.3 index |
| `java -jar <existing VS Code PlantUML extension>/plantuml.jar -failfast2 -tpng -o <workspace>/artifacts/ui01-diagrams <diagram sources>` | PASS: all five rendered using PlantUML 1.2024.3 / local Java / Graphviz 2.44.1; all previews opened visually; state annotation overlap corrected and rerendered |
| Foundation token arithmetic (prior checkpoint, unchanged token values) | PASS: 17 specified text pairs ≥4.5:1, minimum 5.98:1; four boundary pairs ≥3:1. Not full browser state contrast certification |
| `git diff --check` | PASS; staging/manifest checks recorded at publication |

Application/runtime/Playwright/live-provider tests are **not executed** for this docs-only design. Rendered mockups/diagrams do not prove runtime accessibility, authorization or operation survival. Initial sandbox uv cache and remote-network attempts were blocked before execution; authorized reruns passed without changing settings or bypassing gates. The original foundation's PlantUML-not-executed limitation is superseded by the local render evidence above.

## Publication and distribution

Documentation draft PR and final package evidence are recorded after publication below. Final ZIP is a distribution of Git-backed docs, including historical context/dependencies, with root README/publication prompt/manifest and external archive SHA-256. ZIP/output tooling stays under ignored `artifacts/`; no duplicate project checkout. Do not copy distribution README over the repository README.

## Risks, review gate and next task

Full human functional/visual baseline review is required. Review detailed choices in [proposed M3.2 plan](../04-ui-ux/UI-01/M3_2_PROPOSED_PLAN.md), including written precedence over historical WF-001–007, v0.3 visuals, browser/screenshot policy and unsaved-auth-redirect limitation. A merge is not approval. Required automated review may be externally unavailable; record current PR results rather than inheriting historical status. Resolve applicable findings; no auto-merge.

Next: review complete DRAFT UI-01 baseline and record explicit approval or requested changes. Only after full baseline approval may an M3.2 implementation prompt be generated. Actual implementation/deployment/migration/permission changes and M4 retain separate gates. No code work is authorized by this handoff.

Resume:

```powershell
git status --short --branch
git rev-parse HEAD
Get-Content docs/04-ui-ux/UI-01/README.md
gh pr view docs/m3.1b2-ui01-foundations --json url,headRefOid,isDraft,state,statusCheckRollup
gh pr checks docs/m3.1b2-ui01-foundations
uv run --frozen python scripts/validate_standards.py
```
