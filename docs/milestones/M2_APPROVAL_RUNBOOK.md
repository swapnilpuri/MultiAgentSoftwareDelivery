# M2 approval controls and acceptance

The feature candidate requires passing CI, actual Sourcery review and addressed conversations before human merge. Automated test-human decisions prove workflow behavior; they do not accept the milestone. Current results and blockers are in [M2_HANDOFF.md](M2_HANDOFF.md).

## Review and merge the coordinated PRs

1. Open each PR below. Confirm its current head has successful required `validate` checks, completed Sourcery review, and no unresolved actionable conversations. Read its `M2_REVIEW_EVIDENCE.md` for exact tested source and individual review dispositions.
2. Review the complete changes and evidence. A reviewer may request changes; those must be fixed and checked before merge. No gate or protection setting should be disabled to make a PR mergeable.
3. Approve and merge using GitHub's normal human review/merge controls, in this order:

| Order | Repository | PR |
| --- | --- | --- |
| 1 | Contracts | [masd-contracts #4](https://github.com/swapnilpuri/masd-contracts/pull/4) |
| 2 | LLM Gateway | [masd-llm-gateway #2](https://github.com/swapnilpuri/masd-llm-gateway/pull/2) |
| 3 | Agent Service | [masd-agent-service #1](https://github.com/swapnilpuri/masd-agent-service/pull/1) |
| 4 | Project Service | [masd-project-service #3](https://github.com/swapnilpuri/masd-project-service/pull/3) |
| 5 | Angular Studio | [masd-web #4](https://github.com/swapnilpuri/masd-web/pull/4) |
| 6 | Infrastructure | [masd-infrastructure #4](https://github.com/swapnilpuri/masd-infrastructure/pull/4) |
| 7 | Consolidated governance/evidence | Current feature/m2-implementation PR, linked in M2_HANDOFF.md |

The central candidate preserves the exact prior verification commits from [central #6](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/6). Review the overlapping history when merging; do not discard it or count the old verification-only report as runtime acceptance.

## Review an M2 product baseline

1. Open the isolated local Studio at http://127.0.0.1:4400 and sign in with the configured development human account. Retrieve its credentials locally from the ignored infrastructure login file; do not paste them into GitHub, chat or logs.
2. Open an owned project, start discovery with an available authorized model, and answer or explicitly defer the PM questions. Generate the structured PRD, review all 19 sections, and save any edits.
3. Generate and review epics, stories, Given/When/Then criteria, traceability, assumptions and quality findings. Accept or reject findings explicitly; preserve unresolved/deferred items visibly.
4. Compare saved revisions and export the PRD. Submit the current saved revision for review. Unsaved editor changes are excluded and must be saved first.
5. Review the submitted revision and choose Approve, Reject or Request changes with comments. The server binds the decision to the authenticated human, exact revision/hash/version, scope and time. Negative decisions require changed saved content before resubmission.
6. Confirm approval history and approved baseline. Edits create a new draft; they cannot modify the prior approved content or decisions. Stale/hash-mismatched or unauthorized approvals fail. Service/Agent credentials cannot approve.

Human product owners with approval permission may author and approve their product artifacts under M2. Independent human PR review and milestone acceptance remain separate gates. Development authentication uses the same-origin proxy, refuses non-loopback plaintext HTTP, and is not production identity authorization.

## Final acceptance after human merges

1. Tell Codex that the seven PRs are merged. Codex fetches all repositories, reconciles actual `main` content and merge SHAs, and preserves local work. A merged stacked PR alone does not prove `main` contains its implementation.
2. Run each repository's `uv run --frozen python -m scripts.check` against the merged set, plus all Project tests on actual PostgreSQL. Rebuild only the authorized isolated stack with infrastructure `uv run --frozen python -m scripts.m2_compose up --build --wait`.
3. Run all four configured Chromium workflows and infrastructure `uv run --frozen python -m scripts.verify_m2_restart --record <browser-baseline.json>`. Confirm durable history, decisions and baseline, interruption recovery, mobile rendering and absence of generated credentials in runtime logs.
4. Reconcile all 29 criteria with actual merged-source evidence, final CI and review outcomes. Record failures/skips/limits explicitly; do not substitute feature-branch evidence for unexecuted post-merge tests.
5. Review the final verification/handoff and explicitly accept M2. Only then assess M3 readiness. No M3 work or production deployment is authorized by this runbook.
