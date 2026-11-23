import json
import shutil

import pytest

from scripts.validate_governance import ROOT, check


def test_repository_compliance():
    assert check() == []


@pytest.fixture
def repository(tmp_path):
    metadata = json.loads((ROOT / "repository.json").read_text())
    for name in [
        *metadata["required_docs"],
        "README.md",
        "AGENTS.md",
        ".gitignore",
        "repository.json",
        "docs/AI_DEVELOPMENT_OPERATING_MODEL.md",
        "docs/governance/STANDARDS_MANIFEST.yaml",
        ".github/workflows/ci.yml",
    ]:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


@pytest.mark.parametrize("name", ["README.md", "AGENTS.md", ".github/workflows/ci.yml"])
def test_missing_required_file(repository, name):
    (repository / name).unlink()
    assert check(repository)


def test_missing_owner(repository):
    path = repository / "repository.json"
    data = json.loads(path.read_text())
    data.pop("owner")
    path.write_text(json.dumps(data))
    assert any("owner" in error for error in check(repository))


def test_secret_exclusion(repository):
    (repository / ".gitignore").write_text(".venv/\n")
    assert any("secret exclusion" in error for error in check(repository))


def test_command_documentation(repository):
    path = repository / "repository.json"
    data = json.loads(path.read_text())
    data["commands"]["test"] = "undocumented command"
    path.write_text(json.dumps(data))
    assert any("Undocumented" in error for error in check(repository))


def test_ci_must_run_checks(repository):
    (repository / ".github/workflows/ci.yml").write_text("name: empty")
    assert any("CI must" in error for error in check(repository))
