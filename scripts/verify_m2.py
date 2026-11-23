"""Reproducible checks for the authorized, isolated local M2 candidate stack."""

import argparse
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def configuration(workspace: Path) -> dict[str, str]:
    values = {}
    for line in (
        (workspace / "masd-infrastructure/.env.m2").read_text(encoding="utf-8").splitlines()
    ):
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value.strip().strip("'")
    return values


def postgres(workspace: Path) -> None:
    values = configuration(workspace)
    port = int(values["DATABASE_PORT"])
    if not 1 <= port <= 65535:
        raise ValueError("Invalid isolated database port")
    project = workspace / "masd-project-service"
    user = quote(values.get("POSTGRES_USER", "masd"), safe="")
    password = quote(values["POSTGRES_PASSWORD"], safe="")
    database = quote(values.get("POSTGRES_DB", "masd"), safe="")
    url = f"postgresql+psycopg://{user}:{password}@127.0.0.1:{port}/{database}"
    print("Running Project tests against isolated PostgreSQL temporary schemas", flush=True)
    subprocess.run(
        ["uv", "run", "--frozen", "pytest", "-q", "--tb=short"],
        cwd=project,
        env={**os.environ, "MASD_TEST_DATABASE_URL": url},
        check=True,
    )


def runtime_secrets(workspace: Path) -> None:
    values = configuration(workspace)
    login = json.loads(
        (workspace / "masd-infrastructure/artifacts/m2-human-login.json").read_text(
            encoding="utf-8"
        )
    )
    credentials = [
        values[k] for k in ("POSTGRES_PASSWORD", "MASD_GATEWAY_TOKEN", "MASD_AGENT_TOKEN")
    ]
    credentials.append(login["password"])
    if not all(credentials):
        raise ValueError("Isolated test credentials must be configured")
    for service in ("project-service", "llm-gateway", "agent-service", "web", "postgres"):
        logs = subprocess.run(
            ["docker", "logs", f"masd-m2-{service}-1"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        if any(value in logs.stdout + logs.stderr for value in credentials):
            raise RuntimeError("A generated test credential appeared in runtime logs")
    container = json.loads(
        subprocess.check_output(["docker", "inspect", "masd-m2-agent-service-1"])
    )[0]
    names = {entry.split("=", 1)[0] for entry in container["Config"]["Env"]}
    if {"MASD_DATABASE_URL", "MASD_HUMAN_ACCOUNTS"} & names:
        raise RuntimeError("Agent unexpectedly received database or human-account configuration")
    print("PASS: five runtime logs contain no generated credential; Agent has no DB/human config")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=["postgres", "runtime-secrets", "visual"])
    parser.add_argument("--workspace", type=Path, default=ROOT.parent)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if args.check == "postgres":
        postgres(workspace)
    elif args.check == "runtime-secrets":
        runtime_secrets(workspace)
    else:
        subprocess.run(
            ["node", str(ROOT / "scripts/verify_m2_visual.cjs"), str(workspace)], check=True
        )


if __name__ == "__main__":
    main()
