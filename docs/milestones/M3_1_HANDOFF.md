# M3.1 handoff

Milestone: M3.1 (UX, rich AI responses, unified auth, multi-provider models, workflow reliability). Status: **IN PROGRESS**. Batches B1–B3 are implemented, reviewed and green. B4–B9 have not started. M4 is blocked until M3.1 is accepted.

Requirements: [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md). Plan, gap analysis, root cause and lifecycle design: [M3_1_IMPLEMENTATION_PLAN.md](M3_1_IMPLEMENTATION_PLAN.md).

## Open PRs (as of 2026-11-25)

All PRs below pass CI and Sourcery, with every review thread resolved. **None is merged.** `main` in every repository still equals the M3 merge.

| Batch | Repository | Branch | PR | Base |
|---|---|---|---|---|
| B1 | masd-contracts | feature/m3.1-durable-operations | #6 | main |
| B1 | masd-project-service | feature/m3.1-durable-operations | #6 | main |
| B2 | masd-web | feature/m3.1-durable-operations | #7 | main |
| B1/B2 | masd-infrastructure | feature/m3.1-durable-operations | #7 | main |
| plan | MultiAgentSoftwareDelivery | feature/m3.1-plan | #13 | main |
| B3 | masd-contracts | feature/m3.1-architecture-operations | #7 | B1 branch |
| B3 | masd-project-service | feature/m3.1-architecture-operations | #7 | B1 branch |
| B3 | masd-web | feature/m3.1-architecture-operations | #8 | B2 branch |
| B3 | masd-infrastructure | feature/m3.1-architecture-operations | #8 | B1 branch |

Merge order inside each batch: contracts → project-service → web → infrastructure → central. Merge B1/B2 first. Then retarget each B3 PR to `main` (`gh pr edit <n> --base main`) and merge B3. Agents never merge.

## Human actions

1. Merge the B1/B2 PRs. The owner reported doing this on 2026-11-25, but GitHub still showed them open, so check on GitHub.
2. After step 1, retarget the B3 PRs to `main`, review, and merge.
3. Live-provider credentials (optional smoke test only) are still open.

## Decisions

- **OIDC provider:** Keycloak in the dev stack (owner, 2026-11-24).
- **Deployment:** Project Service is single-replica, so upgrades are stop → migrate → start (plan §2a).
- **Contracts:** 0.5.0 (B1) and 0.6.0 (B3) are additive. Earlier versions stay byte-identical.

## Next task: B4 (shell and unified login)

Scope: Requirements R1 and R8.
- Add Keycloak to the `masd-m2` compose stack (infrastructure).
- Project Service OIDC (authorization code + PKCE through a server-side session/BFF). Keep the existing httpOnly cookie session and the per-project owner authorization. No tokens in browser storage.
- One app-level login and an authenticated route guard. Remove the separate studio login forms (masd-web `requirements-studio`, `architecture-studio`). Move AI Chat (`workspace.py`, which uses `local_user_id`) onto the human principal.
- Application shell with the six sections from R1 (AI Workspace, Requirements Studio, Architecture Studio, Delivery/Milestones, Operations/Activity, Administration/Settings), plus breadcrumbs, project context, page titles, help text, and loading/empty/error states.
- Known gap from B3: the sidebar highlights "Projects" on `/projects/:id/...` pages.

After B4: B5 (Gemini and OpenAI-compatible providers, capability/limits endpoint), B6 (rich AI Workspace), B7 (upload/import), B8 (promotion), B9 (acceptance).

## Reproduce the evidence

Run on Windows, from each repository root:
- **Gates:** `uv run --frozen python -m scripts.check`. Run masd-web from an uppercase `C:\` path, because of a Vitest quirk.
- **Real PostgreSQL** (project-service):
  1. Generate a one-off password, for example with `PW=$(python -c "import secrets;print(secrets.token_hex(12))")`.
  2. Start a throwaway `postgres:17` container on `127.0.0.1:55432` with `POSTGRES_PASSWORD=$PW` and `POSTGRES_DB=masd`.
  3. Point `MASD_TEST_DATABASE_URL` at it with the `postgresql+psycopg` driver, built from `$PW` at run time and never written to a file.
  4. Run `uv run --frozen pytest -q`, then stop the container.
- **Stack:** in infrastructure, `uv run --frozen python -m scripts.m2_compose up --build --wait`. The stack builds the sibling checkouts as they are.
- **Browser:** in masd-web, set `INTEGRATION_BASE_URL=http://127.0.0.1:4400`, `M2_HUMAN_LOGIN_FILE=<infra>/artifacts/m2-human-login.json`, `M2_ACCEPTANCE_RECORD` and `M3_ACCEPTANCE_RECORD`. Then run `npx playwright test`.
- **Restart and secrets:** `scripts.verify_m2_restart --record …` and `scripts.verify_m3_restart --record …` (infrastructure), then `scripts.verify_m2 runtime-secrets` (central).

## Last verified results (B3 heads)

| Check | Result |
|---|---|
| project-service | 190 passed / 7 skipped; real PostgreSQL 17: 197 passed, 0 skipped |
| web | 126 Angular tests and build |
| contracts | 85 passed |
| infrastructure | 74 passed |
| Chromium | 5/5 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS / PASS |

## Working notes

- Sourcery reviews every head and raises many findings. Fix each one with a test, reply with the commit, then resolve the thread.
- Never pass `--no-verify`. Project Service's pre-commit hook runs the full suite and takes about 90 s, so commit in the background.
- Python `write_text` on Windows writes cp1252 and CRLF. Always pass `encoding="utf-8", newline="\n"`.
