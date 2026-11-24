# M3 handoff

Milestone: M3 Architect Agent & Solution Architecture Studio. Status: **READY_FOR_HUMAN_APPROVAL** (42/44 PASS; 2 human governance gates). M2 baseline VERIFIED_ACCEPTED. No merges performed; M4 not started.

| Repository | Branch | Evidence head | PR |
|---|---|---|---|
| masd-contracts | feature/m3-architect-agent-solution-studio | `074f39e` | [#5](https://github.com/swapnilpuri/masd-contracts/pull/5) |
| masd-project-service | feature/m3-architect-agent-solution-studio | `103d963` | [#5](https://github.com/swapnilpuri/masd-project-service/pull/5) |
| masd-agent-service | feature/m3-architect-agent-solution-studio | `72bf7e2` | [#3](https://github.com/swapnilpuri/masd-agent-service/pull/3) |
| masd-web | feature/m3-architect-agent-solution-studio | `54b97ef` | [#6](https://github.com/swapnilpuri/masd-web/pull/6) |
| masd-infrastructure | feature/m3-architect-agent-solution-studio | `9fbc13e` | [#6](https://github.com/swapnilpuri/masd-infrastructure/pull/6) |
| MultiAgentSoftwareDelivery | feature/m3-architect-agent-solution-studio | this commit | [#11](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/11) |

## Human actions

1. Decide the disputed thread on contracts #5 ("Focus target is not displayed").
2. Review, then merge with `--match-head-commit`, in this order: contracts → project-service → agent-service → web → infrastructure → central.
3. Accept M3.

## Reproduce the evidence

Run these on Windows, from each repository root, with frozen uv environments and Docker running:
- **Gates:** `uv run --frozen python -m scripts.check`. Run masd-web from an uppercase `C:\` path, because of a Vitest runner quirk on this machine.
- **Stack:** in masd-infrastructure, `uv run --frozen python -m scripts.m2_compose up --build --wait`. This is the isolated masd-m2 stack; Project Service applies migration `0004`.
- **PostgreSQL:** from central, `uv run --frozen python -m scripts.verify_m2 postgres`.
- **Browser:** in masd-web, set `INTEGRATION_BASE_URL=http://127.0.0.1:4400`, `M2_HUMAN_LOGIN_FILE`, `M3_ACCEPTANCE_RECORD=<central>/artifacts/m3-implementation/architecture-baseline.json` and optionally `M3_SCREENSHOT_DIR`, then run `npx playwright test --reporter=json`. The result must be 5 expected and 0 skipped.
- **Restart:** from infrastructure, `uv run --frozen python -m scripts.verify_m3_restart --record <M3_ACCEPTANCE_RECORD>`.
- **Secrets:** from central, `uv run --frozen python -m scripts.verify_m2 runtime-secrets`.

## Risks

- Deterministic adapter only; no live-model quality claim.
- Development-only identity.
- Single Project Service replica.
- The isolated database is at migration `0004`.

Details are in [M3_COMPLETION_REPORT.md](M3_COMPLETION_REPORT.md).
