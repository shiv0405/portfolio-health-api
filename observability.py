from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from flask import Flask, g, has_request_context, request


LOGGER_NAME = "transparent_api_service"


def configure_logging() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


def register_observability(app: Flask) -> None:
    logger = configure_logging()

    @app.before_request
    def start_request_timer() -> None:
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.started_at = time.perf_counter()

    @app.after_request
    def enrich_response(response: Any) -> Any:
        duration_ms = 0.0
        if hasattr(g, "started_at"):
            duration_ms = round((time.perf_counter() - g.started_at) * 1000, 2)

        response.headers["X-Request-ID"] = getattr(g, "request_id", "unknown")
        response.headers["X-Response-Time-Ms"] = str(duration_ms)

        logger.info(
            "request_complete method=%s path=%s status=%s request_id=%s duration_ms=%s",
            request.method,
            request.path,
            response.status_code,
            getattr(g, "request_id", "unknown"),
            duration_ms,
        )
        return response


def diagnostics_payload(status: str = "ok") -> dict[str, Any]:
    payload: dict[str, Any] = {"status": status}

    if has_request_context():
        payload["request_id"] = getattr(g, "request_id", "unknown")
        payload["path"] = request.path

    return payload
