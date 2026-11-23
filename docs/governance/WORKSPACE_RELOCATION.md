# Local workspace relocation

Completed 2026-11-22 (America/Chicago) at the user's request. The dedicated directory is C:/Projects/msad (spelling requested by the user). This parent is not a Git repository.

```text
C:/Projects/msad/
  MultiAgentSoftwareDelivery/
  masd-web/
  masd-project-service/
  masd-contracts/
  masd-infrastructure/
  msad.code-workspace
```

All five independent repositories, including hidden .git data, local preservation branches, ignored archives, working files and dependency directories, were moved together. Original HEADs, branches and origin URLs were compared against the pre-move inventory and preserved. Existing M0 PR/repository URLs remain unchanged; the move does not rename any GitHub repository. Only central workspace documentation changes are committed as part of relocation.

Open C:/Projects/msad/msad.code-workspace for a multi-root editor workspace, or open an individual child repository. Restart this coding session from the new central path: its original directory is empty but remained locked by the active session during cleanup. The empty old directory can be removed after the session releases it. No project data remains there.

The shared standards source remains at C:/Projects/AiEngineeringStandardProject. Imported source paths in standards manifests are accurate provenance and do not require changes. The original M0 requirements/completion report retain the old layout as historical evidence; this record and current README/handoff define the new local layout.

## Compatibility and validation

- Compose build contexts remain ../masd-web and ../masd-project-service. They resolve correctly because the repositories retain their sibling layout.
- Python environment package launchers were refreshed with `uv sync --frozen --reinstall` in each repository. Lockfiles and source dependencies were unchanged.
- `uv run --frozen python -m scripts.check` passed independently in all five repositories: 79 Python tests and 5 Angular unit tests, standards/compliance, lint/format/types, contract validation, security scans and frontend build.
- `git fsck --connectivity-only --no-dangling` passed for every relocated Git repository.
- `git ls-remote --exit-code origin refs/heads/feature/m0-microservices-foundation` succeeded for all five remotes from their new locations.
- From masd-infrastructure, `docker compose config --quiet` and `docker compose up --build --wait` passed with both services healthy.
- `uv run --frozen python -m scripts.smoke` passed health/readiness, runtime config and SPA route. Direct http://127.0.0.1:8000/api/v1/ready returned ready/service/version.
- From masd-web, setting INTEGRATION_BASE_URL=http://127.0.0.1:4200 and running `npx.cmd playwright test` passed the real-browser integration test (1 passed).

Detailed local validation logs and the pre-move repository inventory are retained beside the repositories under msad/relocation-logs and msad/relocation-inventory.json. Temporary integration containers are stopped after validation; restart with the normal Compose command. No main branch changes, merges, repository visibility changes or history rewrites were performed for this relocation.
