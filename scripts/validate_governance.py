"""Offline repository compliance; not runtime authorization or central enforcement."""

import json
from pathlib import Path

from scripts.validate_standards import ROOT, validate


def check(root: Path = ROOT) -> list[str]:
    errors = validate(root)
    try:
        metadata = json.loads((root / "repository.json").read_text())
        for key in ("name", "owner", "domain", "standards_version", "architecture_repository"):
            if not metadata.get(key):
                errors.append(f"Missing ownership/standards metadata: {key}")
        for key in ("build", "test", "lint", "smoke"):
            command = metadata.get("commands", {}).get(key)
            if not isinstance(command, str) or not command.strip():
                errors.append(f"Missing command: {key}")
            elif command not in (root / "README.md").read_text():
                errors.append(f"Undocumented command: {key}")
        required = set(metadata["required_docs"]) | {
            "README.md",
            "AGENTS.md",
            "docs/AI_DEVELOPMENT_OPERATING_MODEL.md",
            "docs/governance/STANDARDS_MANIFEST.yaml",
            ".github/workflows/ci.yml",
        }
        for name in required:
            path = (root / name).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f"Missing or invalid required path: {name}")
        agents = (root / "AGENTS.md").read_text()
        if (
            metadata["architecture_repository"] not in agents
            or "Standards version: `1.0`" not in agents
        ):
            errors.append("AGENTS.md must reference governing architecture and standards version")
        ignore = (root / ".gitignore").read_text().splitlines()
        for pattern in (".env", ".env.*", "*.pem", "*.key"):
            if pattern not in ignore:
                errors.append(f"Missing secret exclusion: {pattern}")
        workflow = (root / ".github/workflows/ci.yml").read_text()
        if "scripts.check" not in workflow:
            errors.append("CI must invoke the mandatory compliance and quality entry point")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid governance configuration: {exc}")
    return errors


if __name__ == "__main__":
    failures = check()
    print("\n".join(failures) if failures else "Governance compliance: PASS")
    raise SystemExit(bool(failures))
