# M3.1 handoff

Milestone: M3.1 (UX, rich AI responses, unified auth, multi-provider models, workflow reliability). Status: **IN PROGRESS**. B1–B4 are merged into `main`. B5 is implemented and verified on `feature/m3.1-providers-limits`, and awaits review. B6–B9 have not started. M4 is blocked until M3.1 is accepted. The owner will do manual verification once all of M3.1 is complete.

Requirements: [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md). Plan, gap analysis, root cause, lifecycle design, and the B4 and B5 designs and evidence: [M3_1_IMPLEMENTATION_PLAN.md](M3_1_IMPLEMENTATION_PLAN.md).

## PR status (2026-11-25)

**Merged on the owner's instruction**, each pinned to its verified head commit:

| Batch | contracts | project-service | web | infrastructure | central |
|---|---|---|---|---|---|
| B1/B2 | #6 `9029150` | #6 `ead2c0f` | #7 `fdfbc13` | #7 `7fba040` | plan #13 `4846b29` |
| B3 | #7 `2b428bd` | #7 `2665234` | #8 `4d334c6` | #8 `b7bab9b` | #14 `c4b1fa6` |
| B4 | #8 `0bb590f` | #8 `586e7a6` | #9 `5aaefaa` | #9 `9faad49` | #15 `4acd6d0` |

**B5 is open for review.** Every repository has the branch `feature/m3.1-providers-limits`, pushed at these verified heads:

| contracts | llm-gateway | project-service | web | infrastructure | central |
|---|---|---|---|---|---|
| #9 `717f794` | #4 `6fc025a` | #9 `ab05843` | #10 `633188b` | #10 `7cef8d5` | #17 |

All six PRs are open, awaiting CI and review.
- **Merge order:** contracts, llm-gateway, project-service, web, then infrastructure.
- **Deploy** the gateway and Project Service together.
- **Central:** the B5 branch is stacked on #16, so merge #16 first.

Agents merge only on an explicit owner instruction, pinned with `--match-head-commit`.

Deployment notes for B4:
1. **Existing `.env.m2`.** Run `python -m scripts.configure_m2 add-sso` once in infrastructure. It only appends keys, and the developer keeps the M2 password, now entered on the Keycloak page.
2. **Migrations `0007_unified_auth` and `0008_principal_subjects`.** Both are additive; upgrade in the usual order: stop, migrate, start. If the pre-B4 `MASD_LOCAL_USER_ID` was not the SSO username, transfer the projects with `python -m project_service.ownership` (dry run first).
3. **Breaking API change.** Workspace routes now require the session. masd-web migrates in the same batch, so deploy the web and Project Service changes together.

## Human actions

1. Review and merge each batch's PRs, or tell the agent to merge them.
2. Optionally, supply live-provider credentials for the smoke test.

## Decisions

- **OIDC provider:** Keycloak in the dev stack (owner, 2026-11-24). B4 serves it on the web origin at `/auth`, and Project Service completes the flow as a backend-for-frontend (plan §6, B4 design).
- **Deployment:** Project Service is single-replica, so upgrades are stop → migrate → start (plan §2a).
- **Contracts:** 0.5.0 (B1) and 0.6.0 (B3) are additive. 0.7.0 (B4) adds SSO and requires the session on workspace routes, its one non-additive change. Earlier versions stay byte-identical.

Deployment notes for B5:
1. **No migration.** The Project Service 0.8.0 and llm-gateway 0.3.0 contracts are additive.
2. **Deploy llm-gateway and Project Service together.** Project Service 0.8.0 tolerates a gateway without `/providers`, but an older Project Service rejects the new provider values.
3. **Behaviour change.** A commercial model is available only when its provider answers and lists it. Before, it was available whenever a key was set.
4. **Provider keys are optional** and go in `.env.m2`; see the infrastructure README. Nothing is generated.

## Next task: B5 review, then B6 (rich AI Workspace)

1. Work through the CI results and review findings on the six B5 PRs.
2. B6: rich AI Workspace and profiles (R2). Then B7 (upload and import), B8 (promotion) and B9 (acceptance).

Two items remain open after B5. Upload size and format limits arrive with B7, and the live-provider smoke test still needs credentials.

Known minor gap from B4: on narrow screens, a breadcrumb separator can start a wrapped line.

## Reproduce the evidence

Run on Windows, from each repository root:
- **Gates:** `uv run --frozen python -m scripts.check`. Run masd-web from an uppercase `C:\` path, because of a Vitest quirk.
- **Real PostgreSQL** (project-service):
  1. Generate a one-off password, for example with `PW=$(python -c "import secrets;print(secrets.token_hex(12))")`.
  2. Start a throwaway `postgres:17` container on `127.0.0.1:55432` with `POSTGRES_PASSWORD=$PW` and `POSTGRES_DB=masd`.
  3. Point `MASD_TEST_DATABASE_URL` at it with the `postgresql+psycopg` driver, built from `$PW` at run time and never written to a file.
  4. Run `uv run --frozen pytest -q`, then stop the container.
- **Stack:** in infrastructure, `uv run --frozen python -m scripts.m2_compose up --build --wait`. The stack builds the sibling checkouts as they are.
- **Browser:** in masd-web, set `INTEGRATION_BASE_URL=http://127.0.0.1:4400`, `M2_HUMAN_LOGIN_FILE=<infra>/artifacts/m2-human-login.json`, `M31_SSO_USERS_FILE=<infra>/artifacts/m31-sso-users.json`, `M2_ACCEPTANCE_RECORD` and `M3_ACCEPTANCE_RECORD`. Then run `npx playwright test`; every journey signs in once through Keycloak.
- **Restart and secrets:** `scripts.verify_m2_restart --record …` and `scripts.verify_m3_restart --record …` (infrastructure), then `scripts.verify_m2 runtime-secrets` (central).

## Last verified results (B5 branch heads)

| Check | Result |
|---|---|
| project-service | 242 passed / 7 skipped; real PostgreSQL 17: 249 passed, 0 skipped |
| llm-gateway | 80 passed |
| web | 163 Angular tests and build |
| contracts | 95 passed |
| infrastructure | 89 passed |
| Chromium (with Keycloak) | 10/10 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS / PASS |

## Working notes

- Sourcery reviews every head and raises many findings. Fix each one with a test, reply with the commit, then resolve the thread.
- Never pass `--no-verify`. Project Service's pre-commit hook runs the full suite and takes about 90 s, so commit in the background.
- Python `write_text` on Windows writes cp1252 and CRLF. Always pass `encoding="utf-8", newline="\n"`.
