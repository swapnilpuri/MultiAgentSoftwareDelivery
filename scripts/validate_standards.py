"""Validate pinned local copies. Manifest uses JSON-compatible YAML (JSON syntax)."""

import hashlib
import json
import re
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
        if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
            return ["Invalid standards entry list"]
        paths = [entry["imported_copy_path"] for entry in entries]
        if set(paths) != MANDATORY or len(paths) != len(MANDATORY):
            return ["Manifest must pin each mandatory artifact exactly once"]
        for entry in entries:
            path = root / entry["imported_copy_path"]
            if not path.is_file():
                errors.append(f"Missing mandatory artifact: {path.name}")
            elif hashlib.sha256(path.read_bytes()).hexdigest() != entry["imported_sha256"]:
                errors.append(f"Modified mandatory artifact: {path.name}")
            for field in ("source_sha256", "imported_sha256"):
                value = entry.get(field)
                if not isinstance(value, str) or re.fullmatch(r"[a-f0-9]{64}", value) is None:
                    errors.append(f"Invalid {field}: expected 64 lowercase hexadecimal characters")
            status = entry.get("import_status")
            if not isinstance(status, str) or not status.startswith("imported"):
                errors.append("Missing source pin or import status")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"Invalid standards manifest (JSON-compatible YAML required): {exc}")
    return errors


if __name__ == "__main__":
    failures = validate()
    print("\n".join(failures) if failures else "Standards integrity: PASS")
    raise SystemExit(bool(failures))
