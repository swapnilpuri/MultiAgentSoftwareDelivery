# UI-01 standalone wireframes — v0.3

**DRAFT — generated after F1–F7 foundation approval; full visual/baseline approval pending.** Work date: 2026-11-27–28 (America/Chicago).

Seven independent built-in image_gen generations replace the need to read seven small storyboard crops. Original v0.2 files remain unchanged in the parent directory. These are newly generated screen compositions, not upscaled crops. [Exact prompts and correction passes](PROMPTS.md) record the imagegen workflow and reference roles. Preferred REF-01–03 were supplied to each initial generation. The reference image content is style guidance; the written approved foundations override unsupported functions depicted there.

| Screen | Actual pixels | Bytes | SHA-256 |
|---|---|---:|---|
| [WF-008-project-switcher.png](WF-008-project-switcher.png) | 1585 × 992 | 1,669,762 | `942ef1cd2ba18bff51648ed833c91670dd30e83ff5a9d52f41bddca429a9857e` |
| [WF-009-profile-settings.png](WF-009-profile-settings.png) | 1585 × 992 | 1,635,996 | `f95ff7306ca46624230121d0a750300e4d79eb7ce6d78bee2862193586ed686c` |
| [WF-010-dark-mode.png](WF-010-dark-mode.png) | 1585 × 992 | 1,582,073 | `aad75888d157ecc398bb8b7020a5bf06078e752bc497a37608c2010fd9f82be1` |
| [WF-011-first-time-workspace.png](WF-011-first-time-workspace.png) | 1585 × 992 | 1,566,221 | `25b77ff7e5f19bdb30813b32430932003ab017955587fc16b95a0255497a0c8e` |
| [WF-012-session-recovery.png](WF-012-session-recovery.png) | 1585 × 992 | 1,343,981 | `34779ccb550737ad2f99402bab13bc6f701b84386230f7572c6aa182339955ae` |
| [WF-013-responsive-shell.png](WF-013-responsive-shell.png) | 1920 × 819 | 1,741,125 | `7301215221f8fae3d46cba80af8bcfbdbcb40e929dc57bba19fbdab632a255cd` |
| [WF-014-future-module.png](WF-014-future-module.png) | 1585 × 992 | 1,645,064 | `1b244d87c8b3b24c4206431040cba468159f6175cc0f70504e934131c2dab97c` |

## Visual QA and reconciliation

All seven selected outputs were displayed and inspected at generation. WF-008 was corrected for a single Home / Projects entry, generic identity and sole Dashboard active state. WF-009 was corrected to make Settings the sole active item and remove an external-link glyph from an internal destination. WF-012 was corrected to remove all project data and authenticated shell navigation. WF-014 was corrected for neutral identity and internal-link indicators. No rejected intermediate output is published.

WF-010 applies the same backed project context and Future labels in dark colors, with no metrics. WF-011 depicts a successful empty workspace, not a simulated runtime snapshot. WF-013 is a standalone large responsive design board with independently readable desktop/tablet/mobile layouts, not the old storyboard crop; pixel dimensions are board dimensions, not browser viewport evidence. The board's content label emphasis is illustrative; implementation uses navigation cards rather than a new dashboard tab data model.

Checked visually: consistent MASD network motif/violet direction, HRMS Platform sample where a project exists, generic user, explicit Future modules, DRAFT/illustrative labels, no runtime percentages/ETAs, fabricated activity, approval records or agent execution results. Recovery has no private project content. Exact spacing/glyphs/token rendering remain subject to human visual review and later browser tests; AI-generated pixels are not an editable logo/icon implementation source. Appearance copy describes the intended preference behavior; storage failure must still be handled per the functional spec.

The [written reconciliation](../../../UI-01/RECONCILIATION.md), [page specifications](../../../UI-01/PAGE_SPECIFICATIONS.md) and [design system](../../../UI-01/DESIGN_SYSTEM.md) govern all 14 screens, including preserved WF-001–007. No pixel changes to those historical seven are claimed. This index resolves standalone-regeneration provenance only; it does not approve the complete design or start implementation.
