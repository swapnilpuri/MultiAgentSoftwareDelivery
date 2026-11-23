"""Scan Git-visible source; only known manifest hash fields are nonsecret metadata."""

import re
import subprocess
from pathlib import Path

from detect_secrets.core.secrets_collection import SecretsCollection
from detect_secrets.settings import default_settings


def main() -> int:
    names = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
        )
        .decode()
        .split("\0")
    )
    secrets = SecretsCollection()
    count = 0
    with default_settings():
        for name in sorted(set(names) - {""}):
            if Path(name).is_file():
                secrets.scan_file(name)
    for name, findings in secrets.data.items():
        lines = Path(name).read_text(encoding="utf-8", errors="replace").splitlines()
        for finding in findings:
            is_manifest_hash = (
                Path(name).as_posix() == "docs/governance/STANDARDS_MANIFEST.yaml"
                and finding.type == "Hex High Entropy String"
                and re.fullmatch(
                    r'\s*"(?:source|imported)_sha256": "[a-f0-9]{64}",?',
                    lines[finding.line_number - 1],
                )
                is not None
            )
            if not is_manifest_hash:
                print(f"Potential secret: {name}:{finding.line_number} ({finding.type})")
                count += 1
    print(f"Secret scan: {count} findings")
    return int(bool(count))


if __name__ == "__main__":
    raise SystemExit(main())
