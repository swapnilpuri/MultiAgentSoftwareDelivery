import json
import logging
import time
from collections.abc import Awaitable, Callable
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.responses import Response


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MASD_")
    environment: Literal["development", "test", "production"] = "development"
    cors_origins: list[str] = ["http://localhost:4200", "http://127.0.0.1:4200"]


class Health(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "multi-agent-software-delivery-api"
    version: str = "0.1.0"


logger = logging.getLogger("masd.api")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


def create_app(settings: Settings | None = None) -> FastAPI:
    config = settings or Settings()
    app = FastAPI(title="MultiAgentSoftwareDelivery", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_methods=["GET"],
        allow_headers=["Accept"],
        allow_credentials=False,
    )

    @app.middleware("http")
    async def request_log(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        started = time.perf_counter()
        response = await call_next(request)
        logger.info(
            json.dumps(
                {
                    "event": "http_request",
                    "method": request.method,
                    "status": response.status_code,
                    "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                }
            )
        )
        return response

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.error(json.dumps({"event": "unhandled_error", "type": type(exc).__name__}))
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    @app.get("/api/v1/health", response_model=Health)
    async def health() -> Health:
        return Health()

    return app


app = create_app()
