import json
import secrets
from types import SimpleNamespace
from urllib.parse import quote

import pytest

from scripts import verify_m2


def test_runtime_scan_detects_url_encoded_credentials(tmp_path, monkeypatch):
    login = tmp_path / "masd-infrastructure/artifacts/m2-human-login.json"
    login.parent.mkdir(parents=True)
    login.write_text(json.dumps({"password": secrets.token_urlsafe(24)}))
    credential = secrets.token_urlsafe(24) + "+"
    monkeypatch.setattr(
        verify_m2,
        "configuration",
        lambda root: {
            "POSTGRES_PASSWORD": credential,
            "MASD_GATEWAY_TOKEN": secrets.token_urlsafe(24),
            "MASD_AGENT_TOKEN": secrets.token_urlsafe(24),
        },
    )
    monkeypatch.setattr(
        verify_m2.subprocess,
        "run",
        lambda *a, **kw: SimpleNamespace(
            stdout=quote(credential, safe=""),
            stderr="",
        ),
    )
    with pytest.raises(RuntimeError, match="credential appeared"):
        verify_m2.runtime_secrets(tmp_path)
