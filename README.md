# transparent-api-service

Production-friendly Flask service that exposes customer portfolio health, risk segmentation, and action recommendations through a lightweight JSON API.

## Highlights

- App factory and package-based service structure
- Request tracing and response timing headers
- Sample enterprise account dataset for realistic demos
- Summary, detail, and recommendation endpoints
- Test coverage for health, summary, filtering, and account detail behavior

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
flask --app app run --debug
pytest
```

## API Endpoints

- `GET /` returns service metadata
- `GET /health` and `GET /healthz` return diagnostics
- `GET /v1/accounts/summary` returns portfolio KPIs and segment mix
- `GET /v1/accounts/high-risk?limit=10&region=Europe` returns prioritized accounts
- `GET /v1/accounts/<account_id>` returns an account snapshot
- `GET /v1/accounts/<account_id>/recommendations` returns targeted actions

## Data Story

The sample data models B2B software accounts with contract, product adoption, support friction, executive engagement, and renewal risk signals. This makes the service useful for demos around customer success operations, backend API design, and portfolio-quality analytics integration.

## Automation Disclosure

**Note:** This repository uses automation and AI assistance for planning, initial scaffolding, routine maintenance, and selected code or documentation generation. I review and curate the outputs as part of my portfolio workflow.
