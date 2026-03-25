from __future__ import annotations

from flask import Flask

from .api import register_routes
from .observability import register_observability
from .services.account_service import AccountService


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["ACCOUNT_SERVICE"] = AccountService.from_default_data_root()
    register_observability(app)
    register_routes(app)
    return app
