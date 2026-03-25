from __future__ import annotations

from flask import Flask, jsonify

from observability import diagnostics_payload, register_observability


app = Flask(__name__)
register_observability(app)


@app.get("/")
def index():
    return jsonify(
        {
            "service": "transparent-api-service",
            "message": "Transparent backend starter is running.",
        }
    )


@app.get("/health")
def health() -> tuple[dict[str, str], int]:
    return diagnostics_payload(), 200


@app.get("/healthz")
def healthcheck() -> tuple[dict[str, str], int]:
    return diagnostics_payload(), 200


if __name__ == "__main__":
    app.run(debug=True)
