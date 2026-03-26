from __future__ import annotations

from flask import Flask, abort, current_app, jsonify, request

from .api_contract import openapi_document
from .observability import diagnostics_payload
from .services.account_service import AccountService


def register_routes(app: Flask) -> None:
    @app.get("/")
    def index():
        settings = current_app.config["SETTINGS"]
        return jsonify(
            {
                "service": settings.service_name,
                "description": "Portfolio account health, renewal risk, and intervention planning API",
                "version": "1.1.0",
                "environment": settings.environment,
                "endpoints": [
                    "/openapi.json",
                    "/health",
                    "/healthz",
                    "/v1/accounts/summary",
                    "/v1/accounts/segments",
                    "/v1/accounts/high-risk",
                    "/v1/accounts/action-queue",
                    "/v1/accounts/renewal-forecast",
                    "/v1/accounts/<account_id>",
                    "/v1/accounts/<account_id>/recommendations",
                ],
            }
        )

    @app.get("/openapi.json")
    def openapi_spec():
        return jsonify(openapi_document())

    @app.get("/health")
    def health():
        return diagnostics_payload(), 200

    @app.get("/healthz")
    def healthz():
        return diagnostics_payload(), 200

    @app.get("/v1/accounts/summary")
    def summary():
        return jsonify(_service().summary())

    @app.get("/v1/accounts/segments")
    def segment_summary():
        return jsonify(_service().segment_summary())

    @app.get("/v1/accounts/high-risk")
    def high_risk_accounts():
        limit = min(max(_read_int(request.args.get("limit"), default=10), 1), 50)
        region = request.args.get("region")
        accounts = _service().high_risk_accounts(limit=limit, region=region)
        return jsonify({"count": len(accounts), "accounts": accounts})

    @app.get("/v1/accounts/action-queue")
    def action_queue():
        limit = min(max(_read_int(request.args.get("limit"), default=15), 1), 50)
        region = request.args.get("region")
        return jsonify(_service().action_queue(limit=limit, region=region))

    @app.get("/v1/accounts/renewal-forecast")
    def renewal_forecast():
        horizon_days = min(max(_read_int(request.args.get("horizon_days"), default=120), 15), 365)
        return jsonify(_service().renewal_forecast(horizon_days=horizon_days))

    @app.get("/v1/accounts/<account_id>")
    def get_account(account_id: str):
        payload = _service().get_account(account_id)
        if payload is None:
            abort(404, description=f"Account '{account_id}' was not found.")
        return jsonify(payload)

    @app.get("/v1/accounts/<account_id>/recommendations")
    def account_recommendations(account_id: str):
        payload = _service().recommendations(account_id)
        if payload is None:
            abort(404, description=f"Account '{account_id}' was not found.")
        return jsonify(payload)


def _service() -> AccountService:
    return current_app.config["ACCOUNT_SERVICE"]


def _read_int(raw_value: str | None, default: int) -> int:
    if raw_value is None:
        return default
    try:
        return int(raw_value)
    except ValueError:
        return default
