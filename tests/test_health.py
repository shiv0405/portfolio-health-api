from flask import jsonify

from app import app
from observability import diagnostics_payload, register_observability


if not app.before_request_funcs:
    register_observability(app)


@app.get("/health")
def health():
    return jsonify(diagnostics_payload())


def test_health_route_returns_status_and_request_id() -> None:
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert "X-Response-Time-Ms" in response.headers

    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["request_id"] == response.headers["X-Request-ID"]
