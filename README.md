# MultiAgentSoftwareDelivery

Central architecture, governance and milestone repository for independently versioned and deployed MASD microservices. This repository contains no active frontend or backend application. M0 does not execute agents, call LLMs, persist projects or provision cloud resources.

## Workspace and delivery

Sibling repositories under C:/Projects: masd-web, masd-project-service, masd-contracts and masd-infrastructure. Each owns its Git history, dependencies, tests, standards manifest and CI. Local repositories are independent; remote creation requires explicit visibility authorization. See repository.json, the architecture documents and M0 completion report for actual delivery status.

The original monorepo work is preserved in local checkpoint d729e8c on feature/m0-foundation-standards. Reusable application code was moved into siblings, with remaining superseded files in an ignored .m0-preserved directory. Do not delete the checkpoint/archive until human review. The active branch follows the multi-repository architecture.

## Repository-local commands

Prerequisites: Python 3.12+ and uv 0.9.26. Install with `uv sync --frozen`.

- Build/document compliance: `uv run --frozen python -m scripts.validate_governance`
- Tests: `uv run --frozen pytest -q`
- Lint: `uv run --frozen ruff check .`
- Smoke/integrity: `uv run --frozen python scripts/validate_standards.py`
- Full required gates: `uv run --frozen python -m scripts.check`

Full gates include standards/compliance, Ruff format/lint, mypy, tests, source secret scanning and pip-audit. They require no sibling source. Offline advisory failures are BLOCKED, never PASS. GitHub Actions invokes the same entry point. Local copies enforce local pins only; they are not a central policy service.

## Local integrated environment

From ../masd-infrastructure, run `docker compose up --build --wait`, then `uv run --frozen python -m scripts.smoke`. Open http://127.0.0.1:4200/projects. Compose builds each service using its own context. Later, update only one with `docker compose up -d --no-deps --build project-service`; it must not rebuild the web image. Docker is needed for runtime verification. Review actual evidence in docs/milestones/M0_COMPLETION_REPORT.md.

Architecture: docs/architecture/. Decisions: docs/adr/. Authorized scope: docs/milestones/M0_REQUIREMENTS.md. Human acceptance and approval are required before merge; M1 is not authorized.
