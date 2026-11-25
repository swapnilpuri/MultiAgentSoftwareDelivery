# M3.1 handoff

Milestone: M3.1 (UX, rich AI responses, unified auth, multi-provider models, workflow reliability). Status: **IN PROGRESS**. B1–B3 are merged. B4 is implemented, verified on a live stack and open for review. B5–B9 have not started. M4 is blocked until M3.1 is accepted.

Requirements: [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md). Plan, gap analysis, root cause, lifecycle design, and the B4 design and evidence: [M3_1_IMPLEMENTATION_PLAN.md](M3_1_IMPLEMENTATION_PLAN.md).

## PR status (2026-11-25)

**Merged on the owner's instruction**, each pinned to its verified head commit:

| Batch | contracts | project-service | web | infrastructure | central |
|---|---|---|---|---|---|
| B1/B2 | #6 `9029150` | #6 `ead2c0f` | #7 `fdfbc13` | #7 `7fba040` | plan #13 `4846b29` |
| B3 | #7 `2b428bd` | #7 `2665234` | #8 `4d334c6` | #8 `b7bab9b` | #14 `c4b1fa6` |

**B4 is open** on branch `feature/m3.1-shell-auth` in all five repositories. Merge in this order: contracts → project-service → infrastructure → web → central. Agents merge only on an explicit owner instruction, pinned with `--match-head-commit`.

Deployment notes for B4:
1. **Existing `.env.m2`.** Run `python -m scripts.configure_m2 add-sso` once in infrastructure. It only appends keys, and the developer keeps the M2 password, now entered on the Keycloak page.
2. **Migrations `0007_unified_auth` and `0008_principal_subjects`.** Both are additive; upgrade in the usual order: stop, migrate, start. If the pre-B4 `MASD_LOCAL_USER_ID` was not the SSO username, transfer the projects with `python -m project_service.ownership` (dry run first).
3. **Breaking API change.** Workspace routes now require the session. masd-web migrates in the same batch, so deploy the web and Project Service changes together.

## Human actions

1. Review and merge the B4 PRs, or tell the agent to merge them.
2. Optionally, supply live-provider credentials for the smoke test.

## Decisions

- **OIDC provider:** Keycloak in the dev stack (owner, 2026-11-24). B4 serves it on the web origin at `/auth`, and Project Service completes the flow as a backend-for-frontend (plan §6, B4 design).
- **Deployment:** Project Service is single-replica, so upgrades are stop → migrate → start (plan §2a).
- **Contracts:** 0.5.0 (B1) and 0.6.0 (B3) are additive. 0.7.0 (B4) adds SSO and requires the session on workspace routes, its one non-additive change. Earlier versions stay byte-identical.

## Next task: B5 (providers and limits)

Scope: Requirements R5 and R9. Add the Gemini and OpenAI-compatible providers to the gateway, plus a capability and limits endpoint (`GET /api/v1/capabilities`) that drives the UI character counters and server-side enforcement. Credentials come only from server configuration.

After B5: B6 (rich AI Workspace), B7 (upload and import), B8 (promotion), B9 (acceptance).

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

## Last verified results (B4 heads)

| Check | Result |
|---|---|
| project-service | 231 passed / 7 skipped; real PostgreSQL 17: 238 passed, 0 skipped |
| web | 154 Angular tests and build |
| contracts | 91 passed |
| infrastructure | 89 passed |
| Chromium (with Keycloak) | 9/9 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS / PASS |

## Working notes

- Sourcery reviews every head and raises many findings. Fix each one with a test, reply with the commit, then resolve the thread.
- Never pass `--no-verify`. Project Service's pre-commit hook runs the full suite and takes about 90 s, so commit in the background.
- Python `write_text` on Windows writes cp1252 and CRLF. Always pass `encoding="utf-8", newline="\n"`.
