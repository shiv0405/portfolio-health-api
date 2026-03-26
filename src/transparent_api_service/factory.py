from __future__ import annotations

from flask import Flask, jsonify

from .api import register_routes
from .observability import register_observability
from .services.account_service import AccountService
from .settings import AppSettings


def create_app() -> Flask:
    app = Flask(__name__)
    settings = AppSettings.from_env()
    app.config["SETTINGS"] = settings
    app.config["ACCOUNT_SERVICE"] = AccountService.from_json_path(settings.data_path)
    register_observability(app)
    register_routes(app)
    register_error_handlers(app)
    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "not_found", "message": getattr(error, "description", "Resource was not found.")}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "bad_request", "message": getattr(error, "description", "Request was invalid.")}), 400
