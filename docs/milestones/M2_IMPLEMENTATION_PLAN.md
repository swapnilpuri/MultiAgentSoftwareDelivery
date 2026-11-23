Current implementation checkpoint: the authorized M2 candidate is implemented across seven repositories; local quality gates, real PostgreSQL, four Chromium workflows and actual restart recovery pass. Current required Sourcery/CI evidence is recorded in M2_HANDOFF.md. Human merges and post-merge main acceptance remain required; no M3. See M2_FINAL_VERIFICATION_REPORT.md, M2_HANDOFF.md and ADR 0005. The original design/plan below is retained for history.

# M2 implementation plan

Status: prerequisite reconciliation completed; application implementation gated.

1. Reconcile M1: preserve clean work, inspect default branches, commits, review threads, discussion and CI. Prepare missing main integrations and obtain human baseline acceptance. See M2_HANDOFF.md.
2. Publish additive requirements/session/agent/approval/error/SSE contracts and compatibility fixtures. Create the independently owned Agent Service after repository creation and writable location are available. Carry standards/CI/health into it without duplicating a service.
3. Implement Project Service domain schemas, deterministic validators, migrations, session checkpoints, idempotency, access isolation and concurrency. Verify with unit tests and real PostgreSQL before generation integration.
4. Implement PM graph and Gateway client: discovery and deferred clarification, typed PRD/revision, stories and quality findings, bounded retries and sanitized failures. Test injection fixtures and model allowlists without commercial credentials.
5. Extend Angular navigation, discovery stream/history, structured editor, stories/filtering/traceability, human finding decisions, revision comparison and approval/history. Test stale requests and project changes; never introduce a second shell.
6. Integrate independent images and execute discovery-to-approval in browser, restart and repeat access/immutability checks. Run full gates in each repository, create separate feature PRs, address actual reviews and CI, and record all AC evidence. Stop before merge and M3.

Runtime work must not silently use the three M1 candidates missing from main as an approved baseline. Prioritize existing main-integration PR review; do not recreate M1 implementation. Missing AI review is reported as NOT EXECUTED/BLOCKED, never inferred from zero threads. No automatic release, permission change or credential change.
