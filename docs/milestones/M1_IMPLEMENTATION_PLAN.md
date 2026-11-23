# M1 implementation plan

1. Reconcile M0, preserve its open PRs and branch M1 from compatible M0 commits; define additive REST/SSE contracts and document local identity/trust boundaries.
2. Add Project Service-owned PostgreSQL schema, Alembic migrations, scoped projects/conversations/messages and idempotent turn records.
3. Add independently deployable LiteLLM gateway with catalog/discovery, authenticated backend access, bounded streaming and deterministic test adapter.
4. Extend the existing Angular shell with project forms/details and safe Markdown chat, scoped conversation navigation and cancellation/recovery.
5. Integrate PostgreSQL, gateway and services through Compose with optional commercial credentials and generated local-only secrets.
6. Run focused/regression/contract/browser/restart/independence tests, record exact evidence and prepare six independent PRs without merging.

Baseline: all five M0 PRs remain open; main contains empty baselines. M1 branches stack on feature/m0-microservices-foundation; gateway targets its new main. M0 compliance and 79 Python tests passed before edits. No uncommitted user changes existed. Public central history retention remains a previously recorded issue; no history rewrite is authorized by M1.
