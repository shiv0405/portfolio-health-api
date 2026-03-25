from __future__ import annotations

from app import app


def test_root_route_lists_service_metadata() -> None:
    client = app.test_client()
    response = client.get("/")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["service"] == "transparent-api-service"
    assert "/v1/accounts/summary" in payload["endpoints"]


def test_health_route_returns_headers() -> None:
    client = app.test_client()
    response = client.get("/health", headers={"X-Request-ID": "req-123"})
    payload = response.get_json()

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-123"
    assert "X-Response-Time-Ms" in response.headers
    assert payload["status"] == "ok"
    assert payload["path"] == "/health"


def test_summary_endpoint_returns_portfolio_metrics() -> None:
    client = app.test_client()
    response = client.get("/v1/accounts/summary")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["portfolio_size"] >= 10
    assert "segment_mix" in payload
    assert "risk_band_mix" in payload


def test_high_risk_endpoint_respects_filters() -> None:
    client = app.test_client()
    response = client.get("/v1/accounts/high-risk?limit=2&region=Europe")
    payload = response.get_json()

    assert response.status_code == 200
    assert len(payload["accounts"]) <= 2
    assert all(account["region"] == "Europe" for account in payload["accounts"])


def test_account_detail_and_recommendations() -> None:
    client = app.test_client()

    detail = client.get("/v1/accounts/ACC-1001")
    recommendations = client.get("/v1/accounts/ACC-1001/recommendations")

    assert detail.status_code == 200
    assert detail.get_json()["account_name"] == "Northwind Health"
    assert recommendations.status_code == 200
    assert recommendations.get_json()["recommended_actions"]
