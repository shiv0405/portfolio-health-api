# Operating Model

Portfolio Health API is designed to support a customer success, revenue operations, or renewal-management workflow.

## Core Views

- `summary`
  - portfolio-wide KPI view for health, churn risk, and value concentration
- `segments`
  - segment-level risk concentrations for planning and executive review
- `high-risk`
  - ranked account list for tactical escalation
- `action-queue`
  - intervention queue with priority labels and recommended actions
- `renewal-forecast`
  - upcoming renewal exposure and value at risk across a configurable horizon

## Production Extension Path

- move the JSON dataset to a warehouse, lakehouse, or service-owned datastore
- add authentication, rate limiting, and service-level objectives
- publish the OpenAPI contract to an internal developer portal
- route action-queue outputs into CRM, ticketing, or lifecycle orchestration tools
