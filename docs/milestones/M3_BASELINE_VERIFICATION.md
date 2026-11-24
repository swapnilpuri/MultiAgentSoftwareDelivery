# M3 baseline verification — M2 acceptance gate

Date: 2026-11-23 (America/Chicago). Verifier: Claude Code (implementation agent). Scope: M3 prompt §2 (Steps 2.1–2.4), executed before any M3 runtime/UI work.

Governing prompt (version-controlled copy of the authorized package, byte-identical to the originals supplied in `masd-infrastructure/docs/milestones/M3_PROMPT/`):

| File | SHA-256 |
|---|---|
| [M3_PROMPT/00_START_HERE.md](M3_PROMPT/00_START_HERE.md) | `34a9eb436e9d0a155f3955997398410e7a1ac716f559296739f2c3dc39ac8af5` |
| [M3_PROMPT/01_ARCHITECTURE_AND_MODEL.md](M3_PROMPT/01_ARCHITECTURE_AND_MODEL.md) (§2 baseline gate) | `007d691bf25dd2fe68c2f1cbde4af6a2369b997b6510eef17d13a38d23e3cecf` |
| [M3_PROMPT/02_AGENT_UI_AND_GOVERNANCE.md](M3_PROMPT/02_AGENT_UI_AND_GOVERNANCE.md) | `11a466f2688aaf352496181b017dc2ba2da69937ed95b370d94708f7d2e7251a` |
| [M3_PROMPT/03_DELIVERY_AND_ACCEPTANCE.md](M3_PROMPT/03_DELIVERY_AND_ACCEPTANCE.md) | `d411e6edc17f11d81b8cf18301ae63d7931eb364c46d5e42227cca695b4dae1d` |

## Post-merge update — 2026-11-24

- **G1 closed:** masd-contracts #4 was human-merged (`2f2bc3d` on `main`).
- **G2 closed:** the 37 findings were addressed in follow-up PRs (gateway #3, agent-service #2, project-service #4, web #5, infrastructure #5, central #9). These were human-merged and all 37 threads are resolved. Three disputed follow-up threads are open for owner confirmation.
- **G3 closed:** the full post-merge acceptance set passed on merged `main` (see M2_HANDOFF.md), and the human acceptance conditions below are recorded.

**Both remaining conditions were met on 2026-11-24:** the owner resolved the three disputed threads by accepting their documented dispositions (AC-26 PASS), and the owner explicitly accepted M2.

**Current classification: VERIFIED_ACCEPTED.** M3-A may start. It must fetch and branch from the then-current `main` heads; the SHAs in M2_HANDOFF.md identify the acceptance-run sources only.

---

*Everything below is the original pre-merge verification (2026-11-23), retained verbatim as history. Its gaps, evidence matrix, "not executed" notes and continuation plan are superseded by the post-merge update above.*

## Decision (historical, pre-merge)

**M2 baseline classification: PARTIAL.** Only VERIFIED_ACCEPTED is an eligible M3 baseline (M3 §2.4), so **M3 runtime and UI implementation have not started** and stop at this gate. No branch was merged, amended or rewritten; no review thread was resolved or dismissed; no settings were changed.

M2 implementation itself is substantially present on `main`: six of seven exact-tested M2 source snapshots are ancestors of `main`, and post-merge `main` CI passes in those six repositories. masd-contracts `main` CI is green only for its M1 content, because M2 is not merged there (G1). The gate fails on three governance/integration gaps, not on missing runtime features.

## Gaps blocking VERIFIED_ACCEPTED

| # | Gap | Evidence | Affected M2 criteria | Owner of fix |
|---|---|---|---|---|
| G1 | **masd-contracts PR #4 is OPEN, not merged.** M2 contracts 0.3.0 (requirements/approval OpenAPI, typed SSE/checkpoint/identity schemas) are absent from contracts `main` (`9829c8d`, the M1 merge). Exact-tested source `87c452c` is not an ancestor of `main`. Consumers on `main` (Project Service, Agent, web) were built against an unpublished contract release. | `gh pr view 4 -R swapnilpuri/masd-contracts`: state OPEN, mergeable, head `32f4487`, checks validate×2 + Sourcery SUCCESS, review APPROVED, 21/21 threads resolved. The PR's own `M2_HANDOFF.md` records it as the "remaining contracts merge gate". | AC-21 (contracts published) | Human: merge #4 (runbook `--match-head-commit 32f4487416fdb38295ae069b1c8ebfed5bd5d675`) |
| G2 | **37 unanswered Sourcery findings on the final heads of six merged PRs.** All are current (not outdated), have zero replies, were posted 2026-11-24 ~02:47–02:50Z (after the final central head `70bc0c3`, committed 01:14Z) and before the ~05:05Z merges. None is referenced by ID or title in any repository's `main` docs. | GraphQL `reviewThreads` per PR (table below). The Sourcery check reported SUCCESS; per M2_REQUIREMENTS §18 and M3 §21, a passing check does not resolve actionable conversations. | AC-26 | Implementation agent: triage, fix or disposition each; human: accept |
| G3 | **No post-merge all-`main` acceptance and no explicit human M2 milestone acceptance record.** M2_HANDOFF / M2_COMPLETION_REPORT / M2_ACCEPTANCE_CRITERIA on `main` still state "pre-push checkpoint … 27 PASS / 2 BLOCKED … M3 NOT READY" and require, after merges, a rerun of configured gates plus PostgreSQL, zero-skip Chromium, restart, visual and credential-log checks, followed by explicit human acceptance. Neither is recorded. A merge by the repository owner is not treated as milestone acceptance (consistent with the M2 report's own policy). | M2_HANDOFF.md §"Exact human actions"; `git log origin/main` in all repos shows no later reconciliation commit. | AC-26, AC-28 (accuracy now stale) | Agent: rerun and reconcile after G1/G2; human: record acceptance |

## Evidence matrix

Fetched 2026-11-23. "Tested source" = exact-tested snapshot recorded in M2_HANDOFF.md.

| Repository | `main` HEAD | M2 PR | PR state / merged by | Tested source on `main` | PR checks (final head) | `main` push CI | Review threads (total / unresolved) | Outstanding |
|---|---|---|---|---|---|---|---|---|
| MultiAgentSoftwareDelivery | `709f2e1` | [#7](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/7) (+ #6 verification) | MERGED / swapnilpuri | `d3c7887` yes | validate×2, Sourcery: SUCCESS | `709f2e1` success | 26 / **5** | G2, G3 |
| masd-contracts | `9829c8d` | [#4](https://github.com/swapnilpuri/masd-contracts/pull/4) | **OPEN** (APPROVED) | `87c452c` **no** | validate×2, Sourcery: SUCCESS | `9829c8d` success (M1 only) | 21 / 0 | **G1** |
| masd-llm-gateway | `9a3ace8` | [#2](https://github.com/swapnilpuri/masd-llm-gateway/pull/2) | MERGED / swapnilpuri | `7c30dc1` yes | validate×2, Sourcery: SUCCESS | `9a3ace8` success | 14 / **4** | G2 |
| masd-agent-service | `efacef2` | [#1](https://github.com/swapnilpuri/masd-agent-service/pull/1) | MERGED / swapnilpuri | `10b14bf` yes | validate×2, Sourcery: SUCCESS | `efacef2` success | 96 / **7** | G2 |
| masd-project-service | `712b6e0` | [#3](https://github.com/swapnilpuri/masd-project-service/pull/3) | MERGED / swapnilpuri | `63433bd` yes | validate×2, Sourcery: SUCCESS | `712b6e0` success | 52 / **6** | G2 |
| masd-web | `87d1559` | [#4](https://github.com/swapnilpuri/masd-web/pull/4) | MERGED / swapnilpuri | `17c1043` yes | validate×2, Sourcery: SUCCESS | `87d1559` success | 58 / **9** | G2 |
| masd-infrastructure | `c7c721d` | [#4](https://github.com/swapnilpuri/masd-infrastructure/pull/4) | MERGED / swapnilpuri | `ed6a3ab` yes | validate×2, Sourcery: SUCCESS | `c7c721d` success | 36 / **6** | G2 |

Step 2.1: all seven expected repositories exist locally under `C:/Projects/msad` with `origin` on `github.com/swapnilpuri`; no additional repositories found (`relocation-logs` is a log folder, not a repository). Local `masd-contracts` is checked out on `feature/m2-pm-requirements-studio` at `32f4487` (PR head); all others on clean `main` equal to `origin/main`. The M3 prompt package was supplied as untracked files in `masd-infrastructure/docs/milestones/M3_PROMPT/`. Those originals are left in place, and the four authoritative files are now versioned in this repository at `docs/milestones/M3_PROMPT/` (hashes above).

Step 2.2: the 17 M2 capabilities and 29 criteria were reconciled individually in M2_FINAL_VERIFICATION_REPORT.md at the exact tested snapshots (27 PASS / 2 BLOCKED). Per the M3 efficiency rule this investigation was not repeated; this verification confirms those snapshots are on `main` (except contracts, G1), and re-evaluates the two criteria that were BLOCKED there. AC-27 (required CI passes on affected PRs) is now satisfied by observation: all seven M2 PRs have green exact-head validate and Sourcery checks. The unmerged contracts release is tracked only under AC-21 (G1), not under AC-27. AC-26 (review conversations resolved) remains BLOCKED (G2).

Step 2.3: implementation PRs, targets, merges, checks and threads are in the matrix. Branch protection was not re-queried (the M2 report records 404/403 limits); no settings were changed.

### G2 unresolved findings (all Sourcery, unanswered, not outdated)

| Repository / PR | Findings |
|---|---|
| Central #7 (`scripts/verify_m2.py`) | Tests can target another database; Encoded leaks evade scan; Secret scan can target another daemon; Recreated services escape the log scan; Large logs exhaust verifier memory |
| masd-web #4 | Retries can discard committed operation keys; Recovery keys are lost; Uncertain starts can block future sessions; Stalled requests lock the studio; Typed descriptions are discarded; Session loading allows duplicate starts; Declined navigation leaves stale URL; Provider outage blocks saved reviews; Projects are skipped between pages |
| masd-project-service #3 | Target accounts can be locked out; Previously rejected content is resubmitted; Failed operations stay stuck; Failed operation appears active; Published PRD schema disagrees; Published validator cannot be imported |
| masd-llm-gateway #2 | Lone surrogate bypasses fixture validation; Passed checks appear pending (Low); Over-budget fixtures can leak; Legacy prompt output changes unnoticed |
| masd-infrastructure #4 | Other provider credentials remain inherited; Existing volume gets new credentials; Inherited password overrides M2 config; Pending request resumes during cleanup; Verifier hangs with Agent paused; Failed pause stops Project Service |
| masd-agent-service #1 | Production can inherit development mode; Ambiguous catalog IDs select wrong limits; Valid SSE framing fails; Approved baseline is ignored; Advertised validation cannot run; Catalog outages lack diagnostic logs; Skipped discovery still passes |

Several touch areas M3 depends on directly: approved-baseline consumption (Agent "Approved baseline is ignored"), published PRD schema/validator (Project Service), SSE framing (Agent), and retry/idempotency recovery (web, Project Service). Building M3 on these without disposition would inherit unverified behaviour.

## Not executed in this verification

The local post-merge regression (seven `scripts.check` gates, PostgreSQL suite, Chromium e2e, restart verifier) was **not executed**: it cannot change the verdict while G1 leaves contracts `main` without M2, and it must run on the final merged set anyway (G3). Post-merge GitHub `main` CI results above are observed, not local runs.

## Safe continuation plan

1. **Human:** merge masd-contracts #4 at head `32f4487` with `--match-head-commit` (G1).
2. **Agent (on authorization):** M2 follow-up branches `fix/m2-final-review-followup` in the six affected repositories. Triage the 37 findings: fix actionable ones with regression tests, reply with evidence and resolve per policy, disposition the rest. Open PRs; obtain fresh Sourcery review and green CI (G2).
3. **Human:** review and merge the follow-up PRs.
4. **Agent:** rerun the full post-merge acceptance set on all-`main` and update M2_HANDOFF / M2_COMPLETION_REPORT / M2_ACCEPTANCE_CRITERIA with actual results (G3).
5. **Human:** record explicit M2 milestone acceptance. Then rerun this verification (only the deltas) and start M3-A (Slice 0 → Slice 1) from the accepted `main` heads.

M3 status: **NOT STARTED — blocked at M3 baseline gate.** No M3 implementation is claimed.
