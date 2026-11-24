"""Reproducible checks for the authorized, isolated local M2 candidate stack."""

import argparse
import json
import os
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote_to_bytes

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "masd-m2"
SERVICES = ("project-service", "llm-gateway", "agent-service", "web", "postgres")
CHUNK = 65536
CONTAINER_ID = re.compile(r"^[0-9a-f]{64}$")


def configuration(workspace: Path) -> dict[str, str]:
    values = {}
    for line in (
        (workspace / "masd-infrastructure/.env.m2").read_text(encoding="utf-8").splitlines()
    ):
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            values[key] = value.strip().strip("'")
    return values


# Every subprocess argv below is a complete string literal (no runtime values), pinned to
# the local `default` Docker context and to the fixed masd-m2 container names.
INSPECT = {
    "project-service": lambda: subprocess.check_output(
        ["docker", "--context", "default", "inspect", "masd-m2-project-service-1"]
    ),
    "llm-gateway": lambda: subprocess.check_output(
        ["docker", "--context", "default", "inspect", "masd-m2-llm-gateway-1"]
    ),
    "agent-service": lambda: subprocess.check_output(
        ["docker", "--context", "default", "inspect", "masd-m2-agent-service-1"]
    ),
    "web": lambda: subprocess.check_output(
        ["docker", "--context", "default", "inspect", "masd-m2-web-1"]
    ),
    "postgres": lambda: subprocess.check_output(
        ["docker", "--context", "default", "inspect", "masd-m2-postgres-1"]
    ),
}
LOGS = {
    "project-service": lambda: subprocess.Popen(
        ["docker", "--context", "default", "logs", "masd-m2-project-service-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ),
    "llm-gateway": lambda: subprocess.Popen(
        ["docker", "--context", "default", "logs", "masd-m2-llm-gateway-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ),
    "agent-service": lambda: subprocess.Popen(
        ["docker", "--context", "default", "logs", "masd-m2-agent-service-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ),
    "web": lambda: subprocess.Popen(
        ["docker", "--context", "default", "logs", "masd-m2-web-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ),
    "postgres": lambda: subprocess.Popen(
        ["docker", "--context", "default", "logs", "masd-m2-postgres-1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ),
}


def local_docker() -> None:
    """The pinned `default` context must itself resolve to the local daemon."""
    endpoint = subprocess.check_output(
        ["docker", "context", "inspect", "default", "--format", "{{.Endpoints.docker.Host}}"],
        text=True,
    ).strip()
    if not endpoint.startswith(("unix:///", "npipe:////./pipe/")):
        raise RuntimeError("The default Docker context is not a local Unix socket or named pipe")


def inspect(service: str) -> dict[str, Any]:
    """Inspect a container and require that it belongs to the authorized M2 project."""
    if service not in SERVICES:
        raise ValueError("Unknown M2 service")
    output = INSPECT[service]()
    container: dict[str, Any] = json.loads(output)[0]
    labels = container["Config"].get("Labels") or {}
    if (
        labels.get("com.docker.compose.project") != PROJECT
        or labels.get("com.docker.compose.service") != service
    ):
        raise RuntimeError(f"Container for {service} is not part of the {PROJECT} Compose project")
    if not container["State"].get("Running"):
        raise RuntimeError(f"{PROJECT} {service} container is not running")
    # Only a validated full container ID is ever passed on to later Docker argv lists.
    if not CONTAINER_ID.fullmatch(str(container.get("Id", ""))):
        raise RuntimeError(f"Unexpected container ID for {service}")
    return container


def verify_database_target(workspace: Path, port: int, env: dict[str, str], database: str) -> str:
    """Require that the test URL reaches the M2 PostgreSQL database; return its container."""
    local_docker()
    container = inspect("postgres")
    bindings = (container["NetworkSettings"].get("Ports") or {}).get("5432/tcp") or []
    if not any(b.get("HostIp") == "127.0.0.1" and b.get("HostPort") == str(port) for b in bindings):
        raise RuntimeError("Configured database port is not published by the M2 PostgreSQL")
    # Static argv: the fixed container name, with psql using the container's own configured
    # user and database. The pinned container ID is re-checked around the call.
    inside = subprocess.check_output(
        [
            "docker",
            "--context",
            "default",
            "exec",
            "masd-m2-postgres-1",
            "sh",
            "-c",
            'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc '
            '"select system_identifier::text || chr(58) || current_database() '
            'from pg_control_system()"',
        ],
        text=True,
    ).strip()
    if inspect("postgres")["Id"] != container["Id"]:
        raise RuntimeError("The M2 PostgreSQL container changed during verification")
    through_url = subprocess.check_output(
        [
            "uv",
            "run",
            "--frozen",
            "python",
            "-c",
            "import os, sqlalchemy\n"
            "engine = sqlalchemy.create_engine(os.environ['MASD_TEST_DATABASE_URL'])\n"
            "with engine.connect() as connection:\n"
            "    print(connection.exec_driver_sql('select system_identifier::text || chr(58) "
            "|| current_database() from pg_control_system()').scalar())\n",
        ],
        cwd=workspace / "masd-project-service",
        env=env,
        text=True,
    ).strip()
    identifier, _, name = inside.partition(":")
    if (
        not identifier.isdecimal()
        or name != database
        or inside != through_url.splitlines()[-1].strip()
    ):
        raise RuntimeError("Database URL does not reach the M2 PostgreSQL database")
    return str(container["Id"])


def postgres(workspace: Path) -> None:
    values = configuration(workspace)
    port = int(values["DATABASE_PORT"])
    if not 1 <= port <= 65535:
        raise ValueError("Invalid isolated database port")
    project = workspace / "masd-project-service"
    raw_user = values.get("POSTGRES_USER", "masd")
    raw_database = values.get("POSTGRES_DB", "masd")
    user = quote(raw_user, safe="")
    password = quote(values["POSTGRES_PASSWORD"], safe="")
    database = quote(raw_database, safe="")
    url = f"postgresql+psycopg://{user}:{password}@127.0.0.1:{port}/{database}"
    env = {
        k: v
        for k, v in {**os.environ, "MASD_TEST_DATABASE_URL": url}.items()
        if k not in {"PYTEST_ADDOPTS", "PYTEST_PLUGINS"}
    }
    verified = verify_database_target(workspace, port, env, raw_database)
    print("Running Project tests against isolated PostgreSQL temporary schemas", flush=True)
    subprocess.run(
        ["uv", "run", "--frozen", "pytest", "-q", "--tb=short"],
        cwd=project,
        env=env,
        check=True,
    )
    # The same container must still serve the target afterwards; otherwise the run is void.
    if verify_database_target(workspace, port, env, raw_database) != verified:
        raise RuntimeError("The M2 PostgreSQL target changed during the test run")


def credential_forms(credentials: Iterable[str]) -> list[bytes]:
    """Raw and percent-encoded forms; logs are matched after escape-case normalization."""
    forms = {
        form.encode("utf-8")
        for credential in credentials
        for form in (credential, quote(credential, safe=""))
    }
    return sorted(forms, key=len)


def normalize(window: bytes) -> bytes:
    """Decode every percent-escape, so any partially encoded credential is found raw."""
    return unquote_to_bytes(window)


def scan_stream(stream: Any, forms: list[bytes]) -> tuple[bool, int]:
    """Stream-scan with constant memory; an overlap catches matches split across chunks."""
    overlap = max(len(form) for form in forms) * 3
    tail = b""
    scanned = 0
    while chunk := stream.read(CHUNK):
        scanned += len(chunk)
        window = tail + chunk
        normalized = normalize(window)
        if any(form in window or form in normalized for form in forms):
            return True, scanned
        tail = window[-overlap:]
    return False, scanned


def read_credentials(workspace: Path) -> list[str]:
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
    return credentials


def runtime_secrets(workspace: Path) -> None:
    local_docker()
    # Pin container IDs first, then read credentials; both are re-checked after the scan,
    # so neither a recreated container nor a rotated credential can produce a false PASS.
    pinned = {service: inspect(service)["Id"] for service in SERVICES}
    credentials = read_credentials(workspace)
    forms = credential_forms(credentials)
    total = 0
    # Each fixed container's complete log prefix at scan time; the pinned IDs are compared
    # again afterwards, so a recreated container cannot substitute its logs.
    for service in pinned:
        with LOGS[service]() as process:
            assert process.stdout is not None
            leaked, scanned = scan_stream(process.stdout, forms)
            if leaked:
                process.kill()
                raise RuntimeError("A generated test credential appeared in runtime logs")
            if process.wait() != 0:
                raise RuntimeError(f"Could not read the complete {service} log prefix")
        total += scanned
    if {service: inspect(service)["Id"] for service in SERVICES} != pinned:
        raise RuntimeError("The M2 stack changed during the log scan; rerun on a stable stack")
    if read_credentials(workspace) != credentials:
        raise RuntimeError("M2 credentials changed during the log scan; rerun on a stable stack")
    container = inspect("agent-service")
    names = {entry.split("=", 1)[0] for entry in container["Config"]["Env"]}
    if {"MASD_DATABASE_URL", "MASD_HUMAN_ACCOUNTS"} & names:
        raise RuntimeError("Agent unexpectedly received database or human-account configuration")
    print(
        f"PASS: {total} bytes of complete {PROJECT} runtime log prefixes (container IDs "
        "unchanged during the scan) contain no generated credential; Agent has no DB/human config"
    )


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
