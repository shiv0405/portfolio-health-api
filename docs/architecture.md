# Architecture Notes

## Goals
- Keep the service easy to read and easy to run.
- Make automation-visible behavior explicit.
- Add basic observability without introducing heavy dependencies.

## Current Structure
- `app.py`: Flask entrypoint and HTTP routes.
- `observability.py`: request ID generation, timing, and structured log setup.
- `tests/`: smoke tests for service behavior.

## Request Flow
1. A request enters the Flask app.
2. `register_observability()` assigns a request ID and starts a timer.
3. The route handler builds a JSON response.
4. The response is enriched with diagnostic headers.
5. A structured log line is emitted for local debugging or container logs.

## Recommended Next Steps
- Move route registration into a small application factory if the service grows.
- Add `/health` and `/ready` endpoints in `app.py` for deployment checks.
- Keep observability helpers dependency-light until metrics/tracing are truly needed.
- Avoid hidden automation: document generated code, maintenance scripts, and policy decisions in the README.

## Extension Pattern
For new endpoints:
- Keep response payloads JSON-first.
- Return explicit status fields for operational endpoints.
- Reuse request IDs in logs and error responses.
- Add one test per route plus one failure-path test where relevant.
