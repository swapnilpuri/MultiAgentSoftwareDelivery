import io
import json
import secrets
from urllib.parse import quote

import pytest

from scripts import verify_m2


def container(service, identifier=None, project="masd-m2", port="5434"):
    return {
        "Id": identifier or f"id-{service}",
        "Config": {
            "Labels": {
                "com.docker.compose.project": project,
                "com.docker.compose.service": service,
            },
            "Env": ["MASD_AGENT_TOKEN=x"],
        },
        "State": {"Running": True},
        "NetworkSettings": {"Ports": {"5432/tcp": [{"HostIp": "127.0.0.1", "HostPort": port}]}},
    }


@pytest.fixture
def stack(tmp_path, monkeypatch):
    """Fake pinned-context Docker: inspect results, per-container log bytes, recorded argv."""
    login = tmp_path / "masd-infrastructure/artifacts/m2-human-login.json"
    login.parent.mkdir(parents=True)
    login.write_text(json.dumps({"password": secrets.token_urlsafe(24)}))
    credential = secrets.token_urlsafe(24) + "+/"
    state = {"credential": credential, "logs": {}, "inspect": {}, "calls": [], "recreate": None}
    monkeypatch.setattr(
        verify_m2,
        "configuration",
        lambda root: {
            "POSTGRES_PASSWORD": credential,
            "MASD_GATEWAY_TOKEN": secrets.token_urlsafe(24),
            "MASD_AGENT_TOKEN": secrets.token_urlsafe(24),
        },
    )
    inspected: dict[str, int] = {}

    def check_output(args, **kwargs):
        state["calls"].append(list(args))
        service = args[-1].removeprefix("masd-m2-").removesuffix("-1")
        inspected[service] = inspected.get(service, 0) + 1
        found = state["inspect"].get(service, container(service))
        if state["recreate"] == service and inspected[service] > 1:
            found = container(service, "id-recreated")
        return json.dumps([found]).encode()

    class Process:
        def __init__(self, args, **kwargs):
            state["calls"].append(list(args))
            self.stdout = io.BytesIO(state["logs"].get(args[-1], b"ordinary log line\n"))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def wait(self):
            return 0

        def kill(self):
            pass

    monkeypatch.setattr(verify_m2.subprocess, "check_output", check_output)
    monkeypatch.setattr(verify_m2.subprocess, "Popen", Process)
    return state


def test_clean_scan_pins_context_project_and_container_ids(stack, tmp_path, capsys):
    verify_m2.runtime_secrets(tmp_path)
    assert all(call[:3] == ["docker", "--context", "default"] for call in stack["calls"])
    log_targets = [call[-1] for call in stack["calls"] if "logs" in call]
    assert log_targets == [f"id-{service}" for service in verify_m2.SERVICES]
    assert "PASS" in capsys.readouterr().out


@pytest.mark.parametrize("encode", [str.lower, str.upper, lambda value: value])
def test_scan_detects_percent_encoded_credentials_in_any_escape_case(stack, tmp_path, encode):
    encoded = quote(stack["credential"], safe="")
    leaked = encoded.replace("%2B", encode("%2B")).replace("%2F", encode("%2F"))
    stack["logs"]["id-web"] = f"request url={leaked}\n".encode()
    with pytest.raises(RuntimeError, match="credential appeared"):
        verify_m2.runtime_secrets(tmp_path)


def test_scan_detects_a_credential_split_across_stream_chunks(stack, tmp_path, monkeypatch):
    monkeypatch.setattr(verify_m2, "CHUNK", 7)
    stack["logs"]["id-postgres"] = b"x" * 1000 + stack["credential"].encode() + b"y" * 1000
    with pytest.raises(RuntimeError, match="credential appeared"):
        verify_m2.runtime_secrets(tmp_path)


def test_scan_streams_large_logs_in_bounded_chunks(stack, tmp_path):
    class Endless(io.RawIOBase):
        reads = 0

        def read(self, size=-1):
            assert 0 < size <= verify_m2.CHUNK
            self.reads += 1
            return b"z" * size if self.reads < 2000 else b""

    stream = Endless()
    assert verify_m2.scan_stream(stream, [stack["credential"].encode()]) == (
        False,
        1999 * verify_m2.CHUNK,
    )


def test_scan_refuses_containers_from_another_project(stack, tmp_path):
    stack["inspect"]["web"] = container("web", project="other-stack")
    with pytest.raises(RuntimeError, match="not part of the masd-m2"):
        verify_m2.runtime_secrets(tmp_path)
    assert not any("logs" in call for call in stack["calls"])


def test_scan_fails_when_a_container_is_recreated_during_the_scan(stack, tmp_path):
    stack["recreate"] = "agent-service"
    with pytest.raises(RuntimeError, match="stack changed during the log scan"):
        verify_m2.runtime_secrets(tmp_path)


def _database(monkeypatch, tmp_path, port="5434", inside="7300", through="7300"):
    monkeypatch.setattr(
        verify_m2,
        "configuration",
        lambda root: {"DATABASE_PORT": "5434", "POSTGRES_PASSWORD": secrets.token_urlsafe(24)},
    )
    calls = []

    def check_output(args, **kwargs):
        calls.append(list(args))
        if "inspect" in args:
            return json.dumps([container("postgres", port=port)]).encode()
        return inside + "\n" if "exec" in args else "uv warning\n" + through + "\n"

    monkeypatch.setattr(verify_m2.subprocess, "check_output", check_output)
    monkeypatch.setattr(verify_m2.subprocess, "run", lambda *a, **kw: calls.append(["pytest"]))
    return calls


def test_postgres_tests_run_only_against_the_m2_cluster(monkeypatch, tmp_path):
    calls = _database(monkeypatch, tmp_path)
    verify_m2.postgres(tmp_path)
    assert calls[-1] == ["pytest"]
    assert all(call[:3] == ["docker", "--context", "default"] for call in calls if "docker" in call)


@pytest.mark.parametrize(
    ("override", "message"),
    [({"port": "5433"}, "not published"), ({"through": "9999"}, "does not reach")],
    ids=["other-port", "other-cluster"],
)
def test_postgres_refuses_another_database_server(monkeypatch, tmp_path, override, message):
    calls = _database(monkeypatch, tmp_path, **override)
    with pytest.raises(RuntimeError, match=message):
        verify_m2.postgres(tmp_path)
    assert ["pytest"] not in calls
