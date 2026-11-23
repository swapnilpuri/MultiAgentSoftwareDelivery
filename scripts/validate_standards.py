"""Validate locally pinned copies. This does not enforce upstream synchronization."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANDATORY = {"AGENTS.md", "docs/AI_DEVELOPMENT_OPERATING_MODEL.md"}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(
            (root / "docs/governance/STANDARDS_MANIFEST.yaml").read_text(encoding="utf-8")
        )
        entries = manifest["standards"]
        paths = [entry["imported_copy_path"] for entry in entries]
        if set(paths) != MANDATORY or len(paths) != len(MANDATORY):
            return ["Manifest must pin each mandatory artifact exactly once"]
        for entry in entries:
            path = root / entry["imported_copy_path"]
            if not path.is_file():
                errors.append(f"Missing mandatory artifact: {path.name}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entry["imported_sha256"]:
                errors.append(f"Modified mandatory artifact: {path.name}")
            if not entry["source_sha256"] or not entry["import_status"].startswith("imported"):
                errors.append("Missing source pin or import status")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid standards manifest: {exc}")
    return errors


if __name__ == "__main__":
    failures = validate()
    print("\n".join(failures) if failures else "Standards integrity: PASS")
    raise SystemExit(bool(failures))
