# MASD UX artifact index — DRAFT

Status: **DRAFT — conceptual design package, not an approved baseline.** Published for M3.1A human review. The package was supplied at `C:/Projects/MASD_UX_Design_v0.1`; its root `README.md` and `CODEX_PUBLISH_PROMPT.md` authorize draft publication and audit only. Their publishing instructions do not replace the central repository README or agent instructions.

## Imported assets

All 11 source artifacts below are copied byte-for-byte into the previously absent `docs/04-ui-ux/` directory. No incoming asset collided with an existing tracked path at central base `88e98485834139eaf71efd01f9d72648e94b53fb`. SHA-256 values refer to original file bytes, including original line endings. All nine PNGs were opened for visual inspection. The written baseline and this DRAFT index govern their status; labels and approved states depicted inside the images are illustrative.

| Repository path relative to this index | Bytes | Dimensions | Original / copied SHA-256 | Status |
|---|---:|---|---|---|
| [UX_BASELINE.md](UX_BASELINE.md) | 3,506 | text | `968064ae8ed2d9ef5b4c2a2f3eaaf0a0d94040a78736f39907503230e26992ed` | DRAFT |
| [WIREFRAME_INDEX.md](WIREFRAME_INDEX.md) | 863 | text | `f41cd0bb93ced9d35e2ed87f487f7844ae24117eda283d4a7168d1ec63d72eb7` | DRAFT |
| [wireframes/00-end-to-end-flow.png](wireframes/00-end-to-end-flow.png) | 2,230,309 | 1448 × 1086 | `0b2c98381312b002814854bb8f36a99c120ff4ba4837984d67197e969a04e39a` | DRAFT |
| [wireframes/01-project-dashboard.png](wireframes/01-project-dashboard.png) | 1,722,167 | 1448 × 1086 | `2a2a86ef85b86eed248014115b71e99ffadec4c92f081756b9f43393dfe3b964` | DRAFT |
| [wireframes/02-discovery-studio.png](wireframes/02-discovery-studio.png) | 2,052,401 | 1448 × 1086 | `ba9b5b770c7b3cc28b7bbf27cc605b57a48ae6a165175cb91a4bbbee0c9365e5` | DRAFT |
| [wireframes/03-requirements-studio.png](wireframes/03-requirements-studio.png) | 1,932,999 | 1448 × 1086 | `445e95c4e51a30feed891f96ca62eb2116fa441b19def846cc1767ce9a18a322` | DRAFT |
| [wireframes/04-architecture-studio.png](wireframes/04-architecture-studio.png) | 1,891,048 | 1448 × 1086 | `deb7e9b900c9c091ebad09d5815ac62f3205267b9a81ac12364170be96319fcc` | DRAFT |
| [wireframes/05-delivery-planning.png](wireframes/05-delivery-planning.png) | 1,858,600 | 1448 × 1086 | `e36116c330b593a95f61fd4a8ceb157a18c416862462c4dc2b7512957ed99576` | DRAFT |
| [wireframes/06-code-workspace.png](wireframes/06-code-workspace.png) | 1,898,403 | 1448 × 1086 | `bf819c5d75ced3f60d5e983489bd744fc71b7d1156885701bd088e7f15e763c3` | DRAFT |
| [wireframes/07-qa-approval.png](wireframes/07-qa-approval.png) | 1,993,374 | 1448 × 1086 | `1ff0c2a97705eca9ab055ac82fa47f47f70b8bdb7aa021fda62da973bfc2fdd6` | DRAFT |
| [wireframes/08-release-operations.png](wireframes/08-release-operations.png) | 1,883,223 | 1448 × 1086 | `35da351a0a5f439fecb131ec8453e3c0ae37ee0dab195b7c68ea6266ed689fd0` | DRAFT |

## Added review artifacts

| Artifact | Purpose | Status |
|---|---|---|
| [IMPLEMENTATION_AUDIT.md](IMPLEMENTATION_AUDIT.md) | Pinned repository snapshot, existing routes/contracts, reuse, gaps, confidence and evidence | DRAFT |
| [PROPOSED_SLICES.md](PROPOSED_SLICES.md) | Candidate dependency sequence and acceptance evidence; no execution authorization | DRAFT |
| [M3.1A handoff](../milestones/M3_1A_HANDOFF.md) | Branch/base, publication, verification, reviews and human gate | DRAFT |
| This index | Provenance, hashes, reconciliation and conflicts | DRAFT |

## Reconciliation and conflicts

| Existing source / artifact | Observed conflict | Resolution for this publication |
|---|---|---|
| Root README, `docs/ROADMAP.md`, `docs/architecture/SERVICE_BOUNDARIES.md`, `repository.json` | Historical M0/M1/M2 descriptions lag current M3/M3.1 source; service-boundary table calls the now-implemented Agent future; metadata still references contract 0.2.0 | Preserve existing files. Use pinned source/contracts and current milestone evidence in the audit; do not infer absent functionality from older prose. Propose a separately reviewed status reconciliation |
| `docs/milestones/M3_DESIGN.md` cancellation section | Describes disconnect-cancels-generation, superseded for Requirements/Architecture by M3.1 operations | Audit distinguishes durable studios from still-stream-bound chat. Retain historical design and link current M3.1 evidence |
| `docs/milestones/M3_1_HANDOFF.md` / completion report | M3.1 implementation is merged but human acceptance remains pending | This PR does not accept M3.1, merge anything, or authorize future work |
| Existing six-section navigation | Draft requests Discovery, UX, Planning, Development, QA, Release, Operations and shared destinations | Record exact route mapping and compatibility aliases in audit. No route/UI change |
| PNG navigation varies between screens; flow 00 omits explicit UX approval | Written baseline requires Architecture and UX approval before delivery planning | Written baseline takes precedence; request human design decision, retain original PNGs |
| Discovery PNG shows office formats, fixed limits and named agent/models | Existing imports and model choices are capability/configuration dependent | Do not treat examples as supported formats, deployed agents or fixed limits |
| Dashboard/QA/release PNGs contain metrics, status and approvals | Illustrative counts may contradict each other; no corresponding implemented downstream domains | No simulated runtime data or inferred approvals; identify future capabilities in audit |
| Promoted architecture/plan Markdown vs canonical typed workflows | A document is not an executable plan or a canonical Architecture Studio package | Preserve existing Markdown artifact feature; require explicit validated handoff design before downstream integration |
| HRMS reference PDF | Referred to by written baseline and previous milestone but not present in supplied package | Record as unavailable reference; do not claim visual/output-quality parity |

Repository convention already uses `docs/architecture/`, `docs/adr/`, `docs/governance/` and `docs/milestones/`. Retain those owners and historical records; add UI/UX drafts in the supplied `docs/04-ui-ux/` path and milestone handoff in the existing milestone directory. The new drafts do not supersede approved requirements or ADRs. No new service/repository/framework is introduced.

Human review starts with [UX_BASELINE.md](UX_BASELINE.md), [WIREFRAME_INDEX.md](WIREFRAME_INDEX.md), then the audit and candidate slices. M3.2 and M4 remain blocked without explicit human authorization.
