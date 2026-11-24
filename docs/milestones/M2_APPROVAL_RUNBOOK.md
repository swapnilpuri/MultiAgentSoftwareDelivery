# M2 approval controls and acceptance

The feature candidate requires passing CI, actual Sourcery review and addressed conversations before human merge. Automated test-human decisions prove workflow behavior; they do not accept the milestone. Current results and blockers are in [M2_HANDOFF.md](M2_HANDOFF.md).

## Review and merge the coordinated PRs

1. Open each PR below. Record its exact current head SHA with `gh pr view <PR-URL> --json headRefOid`. Confirm checks for that SHA have successful required `validate` results, completed successful Sourcery review, and no unresolved actionable conversations. Read its `M2_REVIEW_EVIDENCE.md` for exact tested source and individual review dispositions. Candidate documentation heads and tested runtime/source commits are separate columns in the central handoff.
2. Review the complete changes and evidence. A reviewer may request changes; those must be fixed and checked before merge. No gate or protection setting should be disabled to make a PR mergeable.
3. Immediately before approving and merging, recheck the head SHA and that SHA's checks/review. If it changed, stop and review/check the new head. After required human approval, use `gh pr merge <PR-URL> --merge --match-head-commit <REVIEWED-HEAD-SHA>` so a changed head is rejected rather than merged. Do not enable automatic merge. Follow this order:

| Order | Repository | PR |
| --- | --- | --- |
| 1 | Contracts | [masd-contracts #4](https://github.com/swapnilpuri/masd-contracts/pull/4) |
| 2 | LLM Gateway | [masd-llm-gateway #2](https://github.com/swapnilpuri/masd-llm-gateway/pull/2) |
| 3 | Agent Service | [masd-agent-service #1](https://github.com/swapnilpuri/masd-agent-service/pull/1) |
| 4 | Project Service | [masd-project-service #3](https://github.com/swapnilpuri/masd-project-service/pull/3) |
| 5 | Angular Studio | [masd-web #4](https://github.com/swapnilpuri/masd-web/pull/4) |
| 6 | Infrastructure | [masd-infrastructure #4](https://github.com/swapnilpuri/masd-infrastructure/pull/4) |
| 7 | Consolidated governance/evidence | [MultiAgentSoftwareDelivery #7](https://github.com/swapnilpuri/MultiAgentSoftwareDelivery/pull/7) |

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
2. Prerequisites for a clean checkout: clone the seven repositories as siblings under any workspace directory; run `uv sync --frozen` in every repository, `npm.cmd ci` and `npx.cmd playwright install chromium` in masd-web, and start Docker. With the required human local-configuration/deployment authorization, infrastructure `uv run --frozen python -m scripts.configure_m2` creates ignored credentials once; preserve existing configuration. Rebuild only the authorized isolated stack with infrastructure `uv run --frozen python -m scripts.m2_compose up --build --wait`. Run each repository's `uv run --frozen python -m scripts.check`. From central, run `uv run --frozen python -m scripts.verify_m2 postgres` for all Project tests on actual PostgreSQL. Helpers default to the parent workspace and accept `--workspace <absolute-parent>`; they print no credentials.
3. From masd-web, set `$m2Workspace` to the parent directory containing all seven repositories, then run the browser suite and enforce four passes with zero skips (the example assumes this standard sibling layout):

```powershell
$m2Workspace = (Resolve-Path ..).Path
$env:INTEGRATION_BASE_URL = 'http://127.0.0.1:4400'
$env:M2_HUMAN_LOGIN_FILE = Join-Path $m2Workspace 'masd-infrastructure/artifacts/m2-human-login.json'
$env:M2_ACCEPTANCE_RECORD = Join-Path $m2Workspace 'MultiAgentSoftwareDelivery/artifacts/m2-implementation/browser-baseline.json'
New-Item -ItemType Directory -Force artifacts | Out-Null
npx.cmd playwright test --max-failures=1 --reporter=json > artifacts/m2-post-merge-browser.json
if ($LASTEXITCODE -ne 0) { throw 'Browser acceptance failed' }
uv run --frozen python -c 'import json; s=json.load(open("artifacts/m2-post-merge-browser.json", encoding="utf-8-sig"))["stats"]; assert s["expected"] == 4 and s["skipped"] == 0 and s["unexpected"] == 0 and s["flaky"] == 0, s'
if ($LASTEXITCODE -ne 0) { throw 'M2 requires four browser passes and zero skips' }
```

Then, from infrastructure, run `uv run --frozen python -m scripts.verify_m2_restart --record "$env:M2_ACCEPTANCE_RECORD"`. From central, run `uv run --frozen python -m scripts.verify_m2 visual` and `uv run --frozen python -m scripts.verify_m2 runtime-secrets`. Inspect generated desktop/mobile screenshots under central artifacts/m2-implementation. The committed helpers consume locally generated configuration/records, not author-owned untracked scripts. Confirm durable history, decisions and baseline, interruption recovery, mobile rendering and absence of generated credentials in runtime logs. A skipped M2 scenario never passes acceptance.
4. Reconcile all 29 criteria with actual merged-source evidence, final CI and review outcomes. Record failures/skips/limits explicitly; do not substitute feature-branch evidence for unexecuted post-merge tests.
5. Review the final verification/handoff and explicitly accept M2. Only then assess M3 readiness. No M3 work or production deployment is authorized by this runbook.
