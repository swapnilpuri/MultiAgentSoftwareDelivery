# M3.1 handoff

Milestone: M3.1 (UX, rich AI responses, unified auth, multi-provider models, workflow reliability). Status: **IN PROGRESS**. B1–B6 are merged into `main`. B7 (upload and import) is implemented on `feature/m3.1-upload-import` and its PRs are open for review. B8–B9 have not started. M4 is blocked until M3.1 is accepted. The owner will do manual verification once all of M3.1 is complete.

Requirements: [M3_1_REQUIREMENTS.md](M3_1_REQUIREMENTS.md). Plan, gap analysis, root cause, lifecycle design, and the B4–B6 designs and evidence: [M3_1_IMPLEMENTATION_PLAN.md](M3_1_IMPLEMENTATION_PLAN.md).

## PR status (2026-11-25)

**Merged on the owner's instruction**, each pinned to its verified head commit:

| Batch | contracts | project-service | web | infrastructure | central |
|---|---|---|---|---|---|
| B1/B2 | #6 `9029150` | #6 `ead2c0f` | #7 `fdfbc13` | #7 `7fba040` | plan #13 `4846b29` |
| B3 | #7 `2b428bd` | #7 `2665234` | #8 `4d334c6` | #8 `b7bab9b` | #14 `c4b1fa6` |
| B4 | #8 `0bb590f` | #8 `586e7a6` | #9 `5aaefaa` | #9 `9faad49` | #15 `4acd6d0` |
| B5 | #9 `96dfd00` | #9 `c2985b5` | #10 `0570e3a` | #10 `8db43be` | #17 `d596db6` |
| B6 | #10 `4dcbdcd` | #10 `2dcc88d` | #11 `1c31f5a` | #11 `20f5b77` | #19 `d486376` |

B5 also merged llm-gateway #4 (`8801f16`), and central #16 (`a7e882c`) recorded the B4 merge. B6 also merged llm-gateway #5 (`4704e39`). At merge, each `main` tree was identical to the head verified in the plan's B6 review round 1; later central commits change only documentation. No M3.1 component PRs are open.

**B6 merged 2026-11-25** on the owner's instruction, after review round 1 (all threads resolved; Sourcery re-ran on every head with no new findings). Deploy the gateway and Project Service together.

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

Deployment notes for B6:
1. **Migration `0009_response_versions`** is additive. Upgrade as usual: stop, migrate, start. Existing turns become version 1, Standard profile.
2. **Deploy llm-gateway 0.4.0 together with Project Service 0.9.0.** Project Service now asks for up to 8,192 output tokens by default, and an older gateway still accepts that, but the total and idle timeouts only work together.
3. **Behaviour change.** Answers are no longer cut off at 60–90 s, 64,000 characters, or 1,024–2,048 tokens. Commercial-provider cost per Comprehensive answer rises accordingly. `MASD_MAX_OUTPUT_TOKENS` lowers it.
4. **`MASD_PROVIDER_TIMEOUT` is now an idle limit.** A deployment that relied on it as a total cap sets `MASD_GENERATION_MAX_SECONDS` instead. `MASD_MAX_ACTIVE_GENERATIONS` (default 16) caps concurrent generations in the gateway.

## Current task: B7 (upload and import) in review

1. B7 implements R4 with its security controls and the R5 long-source strategy; the design is in the plan (B7 design). Its PRs are on `feature/m3.1-upload-import` in contracts, project-service, web, infrastructure and central.
2. Next, after the owner merges B7: B8 (promotion), then B9 (acceptance).

Upload size and format limits arrived with B7 (`Capabilities.sources`). The live-provider smoke test still needs credentials.

Deployment notes for B7:
1. **Migration `0010_sources`** is additive. Upgrade as usual: stop, migrate, start.
2. **Deploy Project Service 0.10.0 with the web client of the same release.** `Capabilities.sources` is required, and the nginx upload route accepts up to 26 MB.
3. **Link import uses Project Service's outbound access.** Set `MASD_URL_IMPORT_ENABLED=false` to turn it off.
4. **Malware scanning is off by default** (`MASD_MALWARE_SCANNER=none`), and each source shows "not malware-scanned". Point `MASD_CLAMAV_HOST` at a running `clamd` to enable it; it fails closed.

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

## Last verified results (B6, merged heads)

| Check | Result |
|---|---|
| project-service | 276 passed / 7 skipped; real PostgreSQL 17: 283 passed, 0 skipped |
| llm-gateway | 127 passed |
| web | 204 Angular tests and build |
| contracts | 107 passed |
| infrastructure | 89 passed |
| Chromium (with Keycloak) | 11/11 |
| `verify_m2_restart` / `verify_m3_restart` / runtime secrets | PASS / PASS / PASS |

## Working notes

- Sourcery reviews every head and raises many findings. Fix each one with a test, reply with the commit, then resolve the thread.
- Never pass `--no-verify`. Project Service's pre-commit hook runs the full suite and takes about 90 s, so commit in the background.
- Python `write_text` on Windows writes cp1252 and CRLF. Always pass `encoding="utf-8", newline="\n"`.
