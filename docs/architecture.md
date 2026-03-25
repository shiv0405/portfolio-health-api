# Architecture Notes

## Service Shape

- `app.py` exposes the Flask entrypoint for local development.
- `src/transparent_api_service/factory.py` creates the application and wires dependencies.
- `src/transparent_api_service/services/account_service.py` owns the portfolio-health domain logic.
- `src/transparent_api_service/api.py` keeps HTTP route handling thin and delegates business logic to the service layer.

## Why This Structure

This layout is intentionally small but production-friendly:

- app creation is testable
- domain logic is separated from routing
- the sample dataset can later be replaced by a database or warehouse adapter
- observability is centralized instead of being mixed into endpoint code

## Extension Points

- Replace the JSON dataset with a repository backed by Postgres or DynamoDB
- Add authentication and tenant scoping in a dedicated middleware or blueprint layer
- Emit structured metrics to OpenTelemetry or Prometheus
