from __future__ import annotations

from app import app


def test_root_route_lists_service_metadata() -> None:
    client = app.test_client()
    response = client.get("/")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["service"] == "portfolio-health-api"
    assert "/v1/accounts/summary" in payload["endpoints"]
    assert "/v1/accounts/action-queue" in payload["endpoints"]


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


def test_segment_summary_endpoint_returns_ranked_segments() -> None:
    client = app.test_client()
    response = client.get("/v1/accounts/segments")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["segments"]
    assert "average_churn_risk" in payload["segments"][0]


def test_high_risk_endpoint_respects_filters() -> None:
    client = app.test_client()
    response = client.get("/v1/accounts/high-risk?limit=2&region=Europe")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] <= 2
    assert len(payload["accounts"]) <= 2
    assert all(account["region"] == "Europe" for account in payload["accounts"])


def test_action_queue_and_renewal_forecast_expose_operational_views() -> None:
    client = app.test_client()
    queue_response = client.get("/v1/accounts/action-queue?limit=3")
    forecast_response = client.get("/v1/accounts/renewal-forecast?horizon_days=90")

    queue_payload = queue_response.get_json()
    forecast_payload = forecast_response.get_json()

    assert queue_response.status_code == 200
    assert queue_payload["items"]
    assert "priority" in queue_payload["items"][0]
    assert forecast_response.status_code == 200
    assert forecast_payload["accounts_in_window"] >= 1
    assert "value_at_risk_usd" in forecast_payload


def test_account_detail_and_recommendations() -> None:
    client = app.test_client()

    detail = client.get("/v1/accounts/ACC-1001")
    recommendations = client.get("/v1/accounts/ACC-1001/recommendations")

    assert detail.status_code == 200
    assert detail.get_json()["account_name"] == "Northwind Health"
    assert recommendations.status_code == 200
    assert recommendations.get_json()["recommended_actions"]


def test_not_found_responses_are_json() -> None:
    client = app.test_client()
    response = client.get("/v1/accounts/ACC-DOES-NOT-EXIST")
    payload = response.get_json()

    assert response.status_code == 404
    assert payload["error"] == "not_found"
