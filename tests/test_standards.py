import json
import shutil

import pytest

from scripts.validate_standards import MANDATORY, ROOT, validate


def test_current_standards():
    assert validate() == []


@pytest.fixture
def copied(tmp_path):
    for name in [*MANDATORY, "docs/governance/STANDARDS_MANIFEST.yaml"]:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


@pytest.mark.parametrize("name", sorted(MANDATORY))
def test_missing(copied, name):
    (copied / name).unlink()
    assert any("Missing" in error for error in validate(copied))


@pytest.mark.parametrize("name", sorted(MANDATORY))
def test_modified(copied, name):
    with (copied / name).open("a") as stream:
        stream.write("tampered")
    assert any("Modified" in error for error in validate(copied))


def test_manifest_cannot_omit_required_entry(copied):
    path = copied / "docs/governance/STANDARDS_MANIFEST.yaml"
    data = json.loads(path.read_text())
    data["standards"].pop()
    path.write_text(json.dumps(data))
    assert validate(copied)
