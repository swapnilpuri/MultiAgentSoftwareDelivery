import json
import logging

from fastapi.testclient import TestClient

from services.api.app.main import Settings, create_app


def test_health_and_logging(caplog):
    with caplog.at_level(logging.INFO, logger="masd.api"):
        with TestClient(create_app()) as client:
            response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "0.1.0"
    assert json.loads(caplog.records[-1].message)["event"] == "http_request"


def test_cors_and_not_found():
    with TestClient(create_app(Settings(cors_origins=["http://localhost:4200"]))) as client:
        allowed = client.get("/api/v1/health", headers={"Origin": "http://localhost:4200"})
        denied = client.get("/api/v1/health", headers={"Origin": "https://untrusted.example"})
        assert allowed.headers["access-control-allow-origin"] == "http://localhost:4200"
        assert "access-control-allow-origin" not in denied.headers
        assert client.get("/api/v1/missing").status_code == 404


def test_environment_configuration(monkeypatch):
    monkeypatch.setenv("MASD_CORS_ORIGINS", '["http://localhost:4300"]')
    assert Settings().cors_origins == ["http://localhost:4300"]


def test_errors_are_sanitized(caplog):
    app = create_app()

    @app.get("/failure")
    def failure():
        raise RuntimeError("sensitive-detail")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/failure")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
    assert "sensitive-detail" not in caplog.text
