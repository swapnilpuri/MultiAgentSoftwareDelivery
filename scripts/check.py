"""Required repository-local quality and security gates; fail on first error."""

import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    if Path.cwd().resolve() != root:
        raise SystemExit("Run from repository root")
    run(sys.executable, "-m", "scripts.validate_governance")
    run("ruff", "check", ".")
    run("ruff", "format", "--check", ".")
    run("mypy")
    run("pytest", "-q")
    run(sys.executable, "-m", "scripts.scan_secrets")
    run("pip-audit")
    name = json.loads(Path("repository.json").read_text())["name"]
    if name == "masd-contracts":
        run(sys.executable, "-m", "scripts.validate_contracts")
    elif name == "masd-infrastructure":
        run("docker", "compose", "config", "--quiet")
    elif name == "masd-web":
        npm = shutil.which("npm.cmd") or shutil.which("npm")
        if not npm:
            raise SystemExit("npm is required")
        for gate in ("lint", "typecheck", "format:check", "test", "build"):
            run(npm, "run", gate)
        run(npm, "audit", "--audit-level=low")


if __name__ == "__main__":
    main()
