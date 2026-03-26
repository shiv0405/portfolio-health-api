from __future__ import annotations


def openapi_document() -> dict[str, object]:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "Portfolio Health API",
            "version": "1.1.0",
            "description": "Operational API for portfolio health, renewal risk, and intervention planning.",
        },
        "paths": {
            "/health": {"get": {"summary": "Health check"}},
            "/v1/accounts/summary": {"get": {"summary": "Portfolio KPI summary"}},
            "/v1/accounts/segments": {"get": {"summary": "Segment-level portfolio risk summary"}},
            "/v1/accounts/high-risk": {"get": {"summary": "High-risk accounts ordered by churn risk"}},
            "/v1/accounts/action-queue": {"get": {"summary": "Intervention queue for account teams"}},
            "/v1/accounts/renewal-forecast": {"get": {"summary": "Renewal exposure across a configurable horizon"}},
            "/v1/accounts/{account_id}": {"get": {"summary": "Detailed account snapshot"}},
            "/v1/accounts/{account_id}/recommendations": {"get": {"summary": "Suggested intervention actions"}},
        },
    }
