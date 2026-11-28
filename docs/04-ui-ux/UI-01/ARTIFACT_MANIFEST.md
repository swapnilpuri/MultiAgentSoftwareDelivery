# UI-01 artifact manifest — design v0.2 / wireframes v0.3

**DRAFT — detailed baseline approval pending.** Foundations F1–F7 approved against `865659e`. Date: 2026-11-28 (America/Chicago).

Paths are relative to the central repository root. Hashes describe canonical Git payload bytes, including the preserved historical UX archive, new design documents, generated images/previews and current milestone handoff. This manifest excludes itself to avoid self-reference. Historical nested manifests retain their original source-package meanings; they are not recalculated. Final ZIP has a separate root distribution manifest covering all included context docs and an external SHA-256 sidecar for the archive.

Dependencies: central base `1cfe56fa37879be7e01b23185559eb9c8a7e313b`; foundation `865659e`; existing M3.1A audit/source register; preferred REF-01–03; original v0.2 archive; approved F1–F7. See README, RECONCILIATION and ACCEPTANCE_AND_TRACEABILITY for provenance, scope, requirement mapping and remaining approval gates. This is documentation/artifact distribution, not implementation or execution evidence.

| Repository path | Bytes | SHA-256 |
|---|---:|---|
| `docs/04-ui-ux/ARTIFACT_INDEX.md` | 8547 | `4165c3ad4bf3f6c0f5aa3bf5fae51215beacd0dce345b77bfc149a60dd727d41` |
| `docs/04-ui-ux/IMPLEMENTATION_AUDIT.md` | 28907 | `f9e6b34c606863d04a3027a5146643b59f003777a5959a076417a4b213e3f587` |
| `docs/04-ui-ux/PROPOSED_SLICES.md` | 4458 | `ca8a525fb5e0a20bab2d47190922f182206a69facb1b6726d035f1c64fb21b2a` |
| `docs/04-ui-ux/UI-01/ACCEPTANCE_AND_TRACEABILITY.md` | 12760 | `a79b4907505874abec6d0cf3e896ae000506928ef8fe4a578f6b9fd344925b0f` |
| `docs/04-ui-ux/UI-01/CODEX_PUBLISH_PROMPT.md` | 2005 | `7aee173037fdbb04855a8b25cbdfd0c39ecf9da3c8ebc48437ef548d6d353a59` |
| `docs/04-ui-ux/UI-01/DESIGN_SYSTEM.md` | 7254 | `78b8774cd782070dbf2d78454cac03be1a7f79b57c24ee5c5cf02a1837f182ce` |
| `docs/04-ui-ux/UI-01/M3_2_PROPOSED_PLAN.md` | 5231 | `aca1c83a70e2157a259bc2102c09fd3668c12479a018c2852921dfb17e525345` |
| `docs/04-ui-ux/UI-01/NAVIGATION.md` | 5532 | `3dacc8eaf4955f5ce82a738c22791ab4320fa5df5f1629a7bcc05677507298d3` |
| `docs/04-ui-ux/UI-01/PAGE_SPECIFICATIONS.md` | 19867 | `8a4965fb92a462ae38de680c61ac0f87f45be07f2195a3ee54d4d9f65b88ccb4` |
| `docs/04-ui-ux/UI-01/README.md` | 5387 | `655fa63cedd71d7f1eb802b237e162ccd68ae8140916080529428adbb5331f4f` |
| `docs/04-ui-ux/UI-01/RECONCILIATION.md` | 10123 | `3eb81bedf820a30c6c63a0700a1c79da2f1786efda38491e0decbdd6afec50c4` |
| `docs/04-ui-ux/UI-01/SHELL_FUNCTIONAL_DESIGN.md` | 13445 | `43c5c29d901cd34b3b83262ce64c5c5c32c1654a6e814d56c051b6838f1b62d3` |
| `docs/04-ui-ux/UI-01/TECHNICAL_DESIGN.md` | 17893 | `7d74ab9a3e5e5a6ae143204eac1d50ed6bd1cee26dad4942bab1f4c94c5dcd7b` |
| `docs/04-ui-ux/UI-01/diagrams/auth-recovery.puml` | 1192 | `e8f3587e5173a82e825075cdd316fdb7066c1785a129bfef1507b14e51a81c69` |
| `docs/04-ui-ux/UI-01/diagrams/operation-observer.puml` | 1192 | `21f53014e3dcb39f8b2d200d287136465f31ffe8cf9d9f89f33acad053be1ee5` |
| `docs/04-ui-ux/UI-01/diagrams/operation-state.puml` | 1114 | `6daef4fde13cb5cd789a49060d3320ede16895fb43ee2a74f3ad5895726b0419` |
| `docs/04-ui-ux/UI-01/diagrams/project-switch.puml` | 1152 | `443205e51e2e4f0981514770e823c06f45923c9b143655afa0ad5f84fb279355` |
| `docs/04-ui-ux/UI-01/diagrams/rendered/auth-recovery.png` | 59658 | `789865c29d8bb9ee84935a8c8733727fa23792489c5a8d5fee2a83b0252d4d6b` |
| `docs/04-ui-ux/UI-01/diagrams/rendered/operation-observer.png` | 57260 | `53e2593350d96cd282bd641275ca45e3d073f168065e1097e8d3ddd22632d531` |
| `docs/04-ui-ux/UI-01/diagrams/rendered/operation-state.png` | 60769 | `e901374e92972a863c8fcb8b5fdec56288979a7c343ea535ed2b991f58e4ca9c` |
| `docs/04-ui-ux/UI-01/diagrams/rendered/project-switch.png` | 53854 | `05d216a933af69523b90234f2e64599d8f5399cdc227c903bbe7835a8ecf6900` |
| `docs/04-ui-ux/UI-01/diagrams/rendered/shell-foundation.png` | 80506 | `16f94ee1aaca7a5e3b247da3fa41811c04bc8f7c21191fac3362697a51ee7d1d` |
| `docs/04-ui-ux/UI-01/diagrams/shell-foundation.puml` | 1293 | `5982bd2c7877d8aaa1463bfa6b904a8c89bb7aa9fb0a5b8a1e7098d71dd9c95b` |
| `docs/04-ui-ux/UX_BASELINE.md` | 3506 | `968064ae8ed2d9ef5b4c2a2f3eaaf0a0d94040a78736f39907503230e26992ed` |
| `docs/04-ui-ux/WIREFRAME_INDEX.md` | 1883 | `0e4d3c8e078ed6e53cb642a5f954457e2449f890b6f395a2e514fd4bd7068e00` |
| `docs/04-ui-ux/wireframes/00-end-to-end-flow.png` | 2230309 | `0b2c98381312b002814854bb8f36a99c120ff4ba4837984d67197e969a04e39a` |
| `docs/04-ui-ux/wireframes/01-project-dashboard.png` | 1722167 | `2a2a86ef85b86eed248014115b71e99ffadec4c92f081756b9f43393dfe3b964` |
| `docs/04-ui-ux/wireframes/02-discovery-studio.png` | 2052401 | `ba9b5b770c7b3cc28b7bbf27cc605b57a48ae6a165175cb91a4bbbee0c9365e5` |
| `docs/04-ui-ux/wireframes/03-requirements-studio.png` | 1932999 | `445e95c4e51a30feed891f96ca62eb2116fa441b19def846cc1767ce9a18a322` |
| `docs/04-ui-ux/wireframes/04-architecture-studio.png` | 1891048 | `deb7e9b900c9c091ebad09d5815ac62f3205267b9a81ac12364170be96319fcc` |
| `docs/04-ui-ux/wireframes/05-delivery-planning.png` | 1858600 | `e36116c330b593a95f61fd4a8ceb157a18c416862462c4dc2b7512957ed99576` |
| `docs/04-ui-ux/wireframes/06-code-workspace.png` | 1898403 | `bf819c5d75ced3f60d5e983489bd744fc71b7d1156885701bd088e7f15e763c3` |
| `docs/04-ui-ux/wireframes/07-qa-approval.png` | 1993374 | `1ff0c2a97705eca9ab055ac82fa47f47f70b8bdb7aa021fda62da973bfc2fdd6` |
| `docs/04-ui-ux/wireframes/08-release-operations.png` | 1883223 | `35da351a0a5f439fecb131ec8453e3c0ae37ee0dab195b7c68ea6266ed689fd0` |
| `docs/04-ui-ux/wireframes/UI-01/PUBLICATION.md` | 3406 | `ffb6c34425e626a40a66dd103fbb526b197d9b8d0dd89df4cfaf42252c680a3f` |
| `docs/04-ui-ux/wireframes/UI-01/WF-001-login.png` | 1680238 | `84218a4f080140a7812eaf3626f17a1190e7a3dbeec46c8aacc761613ca1f42c` |
| `docs/04-ui-ux/wireframes/UI-01/WF-002-home-projects.png` | 1675048 | `4190be90322a88b8e6e675b49d5569aa7e380d29443f10e7bccc1bf968f85f6a` |
| `docs/04-ui-ux/wireframes/UI-01/WF-003-create-project.png` | 1702527 | `a7d7fa0d674d2cf04188e38c7f0e7d47ea97b6143c4fd3d64918eb58e3da5dbc` |
| `docs/04-ui-ux/wireframes/UI-01/WF-004-application-shell.png` | 1550791 | `c2d637d24f95964c8ccde4beea750568ebd5fc7b594d9441b4abe9eb128bfc28` |
| `docs/04-ui-ux/wireframes/UI-01/WF-005-project-dashboard.png` | 1714724 | `068ab1ab661b960cbb1df757a44b0d9d3800b6122ec72e9c62cf7274c1314046` |
| `docs/04-ui-ux/wireframes/UI-01/WF-006-collapsed-sidebar.png` | 1552583 | `28568fec91b0246055204839aa808df6975c0da9c5644ed30529b23a613649dc` |
| `docs/04-ui-ux/wireframes/UI-01/WF-007-background-operations.png` | 1674002 | `afdae3786dcb110db7cb5bb7e0f2186bc1298b36a4474625020ac128dadaa7ec` |
| `docs/04-ui-ux/wireframes/UI-01/WF-008-project-switcher.png` | 96047 | `c8ce968d33945a9fd550ad53d7c80d88d19afd24beceb2bbdf76cb4a2bcafc03` |
| `docs/04-ui-ux/wireframes/UI-01/WF-009-profile-settings.png` | 98153 | `f89459b400a21bf53bb5444e662ede7fdc1db2a418f0c7d5667fc978bfa58a1a` |
| `docs/04-ui-ux/wireframes/UI-01/WF-010-dark-mode.png` | 112133 | `f1997dcbed8e7dd97e7d2401638b5c066497d686928ea04f1aff40a897e5f384` |
| `docs/04-ui-ux/wireframes/UI-01/WF-011-first-time-workspace.png` | 98155 | `e3d29da8c2784c87abbd46b601d23ab4448ac9c998818ddb06665107066b033d` |
| `docs/04-ui-ux/wireframes/UI-01/WF-012-session-recovery.png` | 79078 | `282611ee29b981d1469f0454c1a7270eab0422678f2b4c3cff9dfc8ddafa3dd0` |
| `docs/04-ui-ux/wireframes/UI-01/WF-013-responsive-shell.png` | 120431 | `4b0f6b77718aabc77ee77fa2365c77f7f9d8685c3728f189716213a91d16742a` |
| `docs/04-ui-ux/wireframes/UI-01/WF-014-future-module.png` | 124022 | `81939575f7c6f1a0a92c38211215bfb36ae9af9d125c6bf54c38f0055079c790` |
| `docs/04-ui-ux/wireframes/UI-01/WIREFRAME_INDEX.md` | 2577 | `d895cfa3ca75e89db6a237f3446b782174609c3f334b945d7e8cdfcf0b590059` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-collapsed-sidebar.png` | 1710314 | `9f93a229d1636c88f2ed26c0c58fa1f34a82550c30729422cb88b1ddcd757446` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-create-project.png` | 1721725 | `9f9a60d85ae01bf447004118aabbb904f06ea103658505a6cad0ec5d442613db` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-dashboard-dark-sidebar.png` | 1605003 | `8d0230e258269e4d458df5a22ffbac7b34e7529567e115b050a4af185baae145` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-dashboard-operations.png` | 1640767 | `d99df2e69e0c07b8f3ff6c18740f390994af59c7d72668deb95ab5a1f682642d` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-dashboard-overview.png` | 1639554 | `a5c1720fc5599eddff5c79e26ac230da0654ca91bbccdc3335bac85bdd05ba69` |
| `docs/04-ui-ux/wireframes/UI-01/alternatives/ALT-home-projects.png` | 1736322 | `52e45c57f08245ea611c16663fd44c9634424393279ccf9324a3da8e9a8dbdf9` |
| `docs/04-ui-ux/wireframes/UI-01/provenance/ARTIFACT_MANIFEST.md` | 3961 | `f7e7c0d2479782fa9561a2081767f86854a7536106b0ba83e3207440155dd7f1` |
| `docs/04-ui-ux/wireframes/UI-01/provenance/CODEX_PUBLISH_PROMPT.md` | 1318 | `484689f0e5b9f9e56847a8faee1d3a4f144d2bd34748f939f252dd5adbec95c5` |
| `docs/04-ui-ux/wireframes/UI-01/provenance/README.md` | 607 | `68ea62f96bb71b9ae2be77ffbdcf4176b32af677e4815f66b9e4057ae0eca01a` |
| `docs/04-ui-ux/wireframes/UI-01/references/REF-01-original-login.png` | 1544314 | `2ccfdb9937d615e7f544fc34fbf1a1193a400f64f6f93f2c10cdb7b1646f529f` |
| `docs/04-ui-ux/wireframes/UI-01/references/REF-02-original-design-board.png` | 1722795 | `62d1ef0269e4d17b4bd207824a1aa888b168fafe7b7250b59e78681469e2d7c0` |
| `docs/04-ui-ux/wireframes/UI-01/references/REF-03-original-design-board.png` | 1850873 | `a7f1803f47d7dcbbab3079dadeda04b819244aa5f2291344b62a90f36341f805` |
| `docs/04-ui-ux/wireframes/UI-01/references/REF-04-complete-storyboard.png` | 1873132 | `09510a17633bcb1d66c84ca5b446d07bfae76fa099c92449ad0f37ba529f5aee` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/PROMPTS.md` | 18685 | `789bf96d7c92baf84aa0f09b400c605aa8c4ab93c52dea7193918a84ad5b8461` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-008-project-switcher.png` | 1669762 | `942ef1cd2ba18bff51648ed833c91670dd30e83ff5a9d52f41bddca429a9857e` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-009-profile-settings.png` | 1635996 | `f95ff7306ca46624230121d0a750300e4d79eb7ce6d78bee2862193586ed686c` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-010-dark-mode.png` | 1582073 | `aad75888d157ecc398bb8b7020a5bf06078e752bc497a37608c2010fd9f82be1` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-011-first-time-workspace.png` | 1566221 | `25b77ff7e5f19bdb30813b32430932003ab017955587fc16b95a0255497a0c8e` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-012-session-recovery.png` | 1343981 | `34779ccb550737ad2f99402bab13bc6f701b84386230f7572c6aa182339955ae` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-013-responsive-shell.png` | 1741125 | `7301215221f8fae3d46cba80af8bcfbdbcb40e929dc57bba19fbdab632a255cd` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WF-014-future-module.png` | 1645064 | `1b244d87c8b3b24c4206431040cba468159f6175cc0f70504e934131c2dab97c` |
| `docs/04-ui-ux/wireframes/UI-01/v0.3/WIREFRAME_INDEX.md` | 3955 | `2e4ed96b69f76cb97a3a0925de0edf6c4bd9a25a0fab0e1079a0327349dd0a40` |
| `docs/milestones/M3_1B_2_HANDOFF.md` | 5945 | `29ceb6c53def7aa742426caf00f850f238e18aaf3329f795329dcbaa3e3449eb` |
