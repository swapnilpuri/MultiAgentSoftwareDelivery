import json
import shutil

import pytest

from scripts.scan_secrets import within_repository
from scripts.validate_governance import check
from scripts.validate_standards import ROOT, validate


@pytest.fixture
def repository(tmp_path):
    metadata = json.loads((ROOT / "repository.json").read_text(encoding="utf-8"))
    names = set(metadata["required_docs"]) | {
        "README.md",
        "AGENTS.md",
        ".gitignore",
        "repository.json",
        "docs/AI_DEVELOPMENT_OPERATING_MODEL.md",
        "docs/governance/STANDARDS_MANIFEST.yaml",
        ".github/workflows/ci.yml",
    }
    for name in names:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


def test_ignore_trailing_spaces_are_accepted(repository):
    path = repository / ".gitignore"
    path.write_text(
        path.read_text(encoding="utf-8").replace(".env\n", ".env   \n"), encoding="utf-8"
    )
    assert check(repository) == []


def test_inline_comment_is_not_a_valid_secret_exclusion(repository):
    path = repository / ".gitignore"
    path.write_text(
        path.read_text(encoding="utf-8").replace(".env\n", ".env # not a Git comment\n"),
        encoding="utf-8",
    )
    assert any("secret exclusion: .env" in error for error in check(repository))


def test_missing_instructions_do_not_hide_other_missing_files(repository):
    (repository / "AGENTS.md").unlink()
    (repository / ".github/workflows/ci.yml").unlink()
    errors = check(repository)
    assert any("AGENTS.md" in error for error in errors)
    assert any(".github/workflows/ci.yml" in error for error in errors)


def test_missing_artifact_does_not_invent_a_missing_pin(repository):
    (repository / "AGENTS.md").unlink()
    errors = validate(repository)
    assert errors == ["Missing mandatory artifact: AGENTS.md"]


def test_invalid_hash_and_status_are_reported(repository):
    path = repository / "docs/governance/STANDARDS_MANIFEST.yaml"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["standards"][0]["source_sha256"] = "a" * 63
    document["standards"][0]["import_status"] = 123
    path.write_text(json.dumps(document), encoding="utf-8")
    errors = validate(repository)
    assert any("64 lowercase" in error for error in errors)
    assert any("import status" in error for error in errors)


def test_scan_paths_cannot_escape_checkout(tmp_path):
    assert within_repository(tmp_path, "source.py")
    assert not within_repository(tmp_path, "../outside.env")


def test_manifest_format_failure_is_explicit(repository):
    (repository / "docs/governance/STANDARDS_MANIFEST.yaml").write_text(
        "standards: []", encoding="utf-8"
    )
    assert any("JSON-compatible YAML required" in error for error in validate(repository))


def test_stale_scanner_line_is_reported_without_crashing(repository, monkeypatch):
    import contextlib
    from types import SimpleNamespace

    from scripts import scan_secrets

    name = "docs/governance/STANDARDS_MANIFEST.yaml"

    class Collection:
        data = {name: [SimpleNamespace(line_number=99999, type="Hex High Entropy String")]}

        def scan_file(self, filename):
            pass

    monkeypatch.chdir(repository)
    monkeypatch.setattr(
        scan_secrets.subprocess, "check_output", lambda *a, **k: name.encode() + b"\0"
    )
    monkeypatch.setattr(scan_secrets, "SecretsCollection", Collection)
    monkeypatch.setattr(scan_secrets, "default_settings", contextlib.nullcontext)
    assert scan_secrets.main() == 1
