"""Offline repository compliance; not runtime authorization or central enforcement."""

import json
from pathlib import Path

from scripts.validate_standards import ROOT, validate


def check(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        errors.extend(validate(root))
        metadata = json.loads((root / "repository.json").read_text(encoding="utf-8"))
        for key in ("name", "owner", "domain", "standards_version", "architecture_repository"):
            if not metadata.get(key):
                errors.append(f"Missing ownership/standards metadata: {key}")
        required = set(metadata["required_docs"]) | {
            "README.md",
            "AGENTS.md",
            ".gitignore",
            "docs/AI_DEVELOPMENT_OPERATING_MODEL.md",
            "docs/governance/STANDARDS_MANIFEST.yaml",
            ".github/workflows/ci.yml",
        }
        for name in required:
            path = (root / name).resolve()
            if not path.is_relative_to(root.resolve()) or not path.is_file():
                errors.append(f"Missing or invalid required path: {name}")
        readme_path = root / "README.md"
        readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
        for key in ("build", "test", "lint", "smoke"):
            command = metadata.get("commands", {}).get(key)
            if not isinstance(command, str) or not command.strip():
                errors.append(f"Missing command: {key}")
            elif readme and command not in readme:
                errors.append(f"Undocumented command: {key}")
        agents_path = root / "AGENTS.md"
        if agents_path.is_file():
            agents = agents_path.read_text(encoding="utf-8")
            if (
                metadata["architecture_repository"] not in agents
                or "Standards version: `1.0`" not in agents
            ):
                errors.append(
                    "AGENTS.md must reference governing architecture and standards version"
                )
        ignore_path = root / ".gitignore"
        lines = (
            ignore_path.read_text(encoding="utf-8").splitlines() if ignore_path.is_file() else []
        )
        # Git ignores unescaped trailing spaces; inline # text is part of a pattern.
        ignore = {line if line.endswith("\\ ") else line.rstrip(" ") for line in lines}
        for pattern in (".env", ".env.*", "*.pem", "*.key"):
            if pattern not in ignore:
                errors.append(f"Missing secret exclusion: {pattern}")
        workflow_path = root / ".github/workflows/ci.yml"
        if workflow_path.is_file() and "scripts.check" not in workflow_path.read_text(
            encoding="utf-8"
        ):
            errors.append("CI must invoke the mandatory compliance and quality entry point")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        errors.append(f"Invalid governance configuration: {exc}")
    return errors


if __name__ == "__main__":
    failures = check()
    print("\n".join(failures) if failures else "Governance compliance: PASS")
    raise SystemExit(bool(failures))
