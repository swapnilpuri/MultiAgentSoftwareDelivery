import io
import json
import secrets
from urllib.parse import quote

import pytest

from scripts import verify_m2

ids = {
    name: format(index + 1, "064x")
    for index, name in enumerate(
        ["project-service", "llm-gateway", "agent-service", "web", "postgres", "recreated"]
    )
}


def container(service, identifier=None, project="masd-m2", port="5434"):
    return {
        "Id": identifier or ids[service],
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
    configured = {
        "POSTGRES_PASSWORD": credential,
        "MASD_GATEWAY_TOKEN": secrets.token_urlsafe(24),
        "MASD_AGENT_TOKEN": secrets.token_urlsafe(24),
    }
    monkeypatch.setattr(verify_m2, "configuration", lambda root: dict(configured))
    inspected: dict[str, int] = {}

    def check_output(args, **kwargs):
        state["calls"].append(list(args))
        if "context" in args:
            return state.get("endpoint", "npipe:////./pipe/docker_engine") + "\n"
        service = args[-1].removeprefix("masd-m2-").removesuffix("-1")
        inspected[service] = inspected.get(service, 0) + 1
        found = state["inspect"].get(service, container(service))
        if state["recreate"] == service and inspected[service] > 1:
            found = container(service, ids["recreated"])
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
    container_calls = [call for call in stack["calls"] if call[1] != "context"]
    assert all(call[:3] == ["docker", "--context", "default"] for call in container_calls)
    assert ["docker", "context", "inspect", "default"] == stack["calls"][0][:4]
    log_targets = [call[-1] for call in stack["calls"] if "logs" in call]
    assert log_targets == [f"masd-m2-{service}-1" for service in verify_m2.SERVICES]
    assert "PASS" in capsys.readouterr().out


@pytest.mark.parametrize("encode", [str.lower, str.upper, lambda value: value])
def test_scan_detects_percent_encoded_credentials_in_any_escape_case(stack, tmp_path, encode):
    encoded = quote(stack["credential"], safe="")
    leaked = encoded.replace("%2B", encode("%2B")).replace("%2F", encode("%2F"))
    stack["logs"]["masd-m2-web-1"] = f"request url={leaked}\n".encode()
    with pytest.raises(RuntimeError, match="credential appeared"):
        verify_m2.runtime_secrets(tmp_path)


def test_scan_detects_a_credential_split_across_stream_chunks(stack, tmp_path, monkeypatch):
    monkeypatch.setattr(verify_m2, "CHUNK", 7)
    stack["logs"]["masd-m2-postgres-1"] = b"x" * 1000 + stack["credential"].encode() + b"y" * 1000
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


def _database(monkeypatch, tmp_path, port="5434", inside="7300:masd", through="7300:masd"):
    monkeypatch.setattr(
        verify_m2,
        "configuration",
        lambda root: {"DATABASE_PORT": "5434", "POSTGRES_PASSWORD": secrets.token_urlsafe(24)},
    )
    calls = []

    def check_output(args, **kwargs):
        calls.append(list(args))
        if "context" in args:
            return "unix:///var/run/docker.sock\n"
        if "inspect" in args:
            return json.dumps([container("postgres", port=port)]).encode()
        return inside + "\n" if "exec" in args else "uv warning\n" + through + "\n"

    monkeypatch.setattr(verify_m2.subprocess, "check_output", check_output)
    monkeypatch.setattr(verify_m2.subprocess, "run", lambda *a, **kw: calls.append(["pytest"]))
    return calls


def test_postgres_tests_run_only_against_the_m2_cluster(monkeypatch, tmp_path):
    calls = _database(monkeypatch, tmp_path)
    verify_m2.postgres(tmp_path)
    # Verified before pytest and re-verified after it.
    position = calls.index(["pytest"])
    assert any("exec" in call for call in calls[:position])
    assert any("exec" in call for call in calls[position:])
    docker = [call for call in calls if call[0] == "docker" and call[1] != "context"]
    assert docker and all(call[:3] == ["docker", "--context", "default"] for call in docker)


@pytest.mark.parametrize(
    ("override", "message"),
    [
        ({"port": "5433"}, "not published"),
        ({"through": "9999:masd"}, "does not reach"),
        ({"inside": "7300:other", "through": "7300:other"}, "does not reach"),
    ],
    ids=["other-port", "other-cluster", "other-database"],
)
def test_postgres_refuses_another_database_server(monkeypatch, tmp_path, override, message):
    calls = _database(monkeypatch, tmp_path, **override)
    with pytest.raises(RuntimeError, match=message):
        verify_m2.postgres(tmp_path)
    assert ["pytest"] not in calls


@pytest.mark.parametrize("encoded", ["%2B", "%2b"])
def test_scan_detects_partially_percent_encoded_credentials(stack, tmp_path, encoded):
    credential = stack["credential"]
    # Only some characters are escaped: the first one always, the "+" in either hex case.
    partial = "%" + format(ord(credential[0]), "02X") + credential[1:].replace("+", encoded)
    stack["logs"]["masd-m2-web-1"] = f"url={partial}\n".encode()
    with pytest.raises(RuntimeError, match="credential appeared"):
        verify_m2.runtime_secrets(tmp_path)


def test_scan_refuses_a_remote_default_docker_context(stack, tmp_path):
    stack["endpoint"] = "tcp://remote.example:2376"
    with pytest.raises(RuntimeError, match="not a local"):
        verify_m2.runtime_secrets(tmp_path)
    assert not any("logs" in call for call in stack["calls"])


def test_scan_fails_when_credentials_rotate_during_the_scan(stack, tmp_path, monkeypatch):
    original = verify_m2.read_credentials
    reads = []

    def rotating(workspace):
        reads.append(True)
        values = original(workspace)
        return values if len(reads) == 1 else [*values[:-1], "rotated"]

    monkeypatch.setattr(verify_m2, "read_credentials", rotating)
    with pytest.raises(RuntimeError, match="credentials changed"):
        verify_m2.runtime_secrets(tmp_path)


def test_postgres_identity_uses_static_argv_and_the_configured_database(monkeypatch, tmp_path):
    calls = _database(monkeypatch, tmp_path, inside="7300:product", through="7300:product")
    monkeypatch.setattr(
        verify_m2,
        "configuration",
        lambda root: {
            "DATABASE_PORT": "5434",
            "POSTGRES_PASSWORD": secrets.token_urlsafe(24),
            "POSTGRES_DB": "product",
        },
    )
    verify_m2.postgres(tmp_path)
    exec_call = next(call for call in calls if "exec" in call)
    assert exec_call[:5] == ["docker", "--context", "default", "exec", "masd-m2-postgres-1"]
    assert '"$POSTGRES_USER"' in exec_call[-1] and '"$POSTGRES_DB"' in exec_call[-1]


def test_postgres_run_is_void_if_the_target_changes(monkeypatch, tmp_path):
    calls = _database(monkeypatch, tmp_path)
    seen = []
    original = verify_m2.verify_database_target

    def changing(*args):
        seen.append(original(*args))
        return seen[0] if len(seen) == 1 else "f" * 64

    monkeypatch.setattr(verify_m2, "verify_database_target", changing)
    with pytest.raises(RuntimeError, match="target changed"):
        verify_m2.postgres(tmp_path)
    assert ["pytest"] in calls
