"""Scan Git-visible source; fail on findings without printing secret values."""

import subprocess

from detect_secrets import SecretsCollection  # type: ignore[import-untyped]
from detect_secrets.settings import default_settings  # type: ignore[import-untyped]


def main() -> int:
    names = (
        subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
        )
        .decode()
        .split("\0")
    )
    secrets = SecretsCollection()
    with default_settings():
        for name in sorted(set(names) - {""}):
            secrets.scan_file(name)
    for name, findings in secrets.data.items():
        for finding in findings:
            print(f"Potential secret: {name}:{finding.line_number} ({finding.type})")
    print(f"Secret scan: {len(secrets.data)} files with findings")
    return int(bool(secrets.data))


if __name__ == "__main__":
    raise SystemExit(main())
