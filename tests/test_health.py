from app import app


def test_health_route_returns_status_and_request_id() -> None:
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert "X-Response-Time-Ms" in response.headers

    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["request_id"] == response.headers["X-Request-ID"]
    assert payload["path"] == "/health"


def test_healthz_route_accepts_forwarded_request_id() -> None:
    client = app.test_client()
    response = client.get("/healthz", headers={"X-Request-ID": "test-request-id"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-id"

    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["request_id"] == "test-request-id"
    assert payload["path"] == "/healthz"
