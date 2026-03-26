# Portfolio Health Control API

Production-oriented Flask service for portfolio health, renewal risk, and intervention planning. The project is designed to showcase backend engineering with a strong analytics story: it exposes customer portfolio KPIs, segment-level risk concentrations, ranked action queues, and renewal exposure views through a clean JSON API.

## Why This Project Works For Senior Roles

- Combines service design with commercial analytics instead of exposing toy CRUD endpoints
- Models realistic account signals such as adoption, executive engagement, support friction, billing delay, and renewal timing
- Includes observability headers, a machine-readable contract, and operationally useful endpoints
- Reads like an internal platform API a revenue operations or customer success engineering team could evolve

## Core Capabilities

- Portfolio summary view with health, risk, region mix, and contract value
- Segment risk summary for leadership planning
- High-risk account ranking with filtering support
- Action queue endpoint for intervention prioritization
- Renewal forecast endpoint for exposure review inside a configurable horizon
- JSON error responses and request tracing headers for cleaner integration behavior

## Project Layout

- `src/transparent_api_service/` contains the app factory, route layer, settings, and domain logic
- `data/account_health_snapshot.json` contains the sample enterprise portfolio
- `docs/` contains architecture and operating-model notes
- `tests/` covers health, summary, ranking, action queue, and contract behavior

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
flask --app app run --debug
python -m pytest -q tests
```

## API Surface

- `GET /openapi.json`
- `GET /health`
- `GET /v1/accounts/summary`
- `GET /v1/accounts/segments`
- `GET /v1/accounts/high-risk?limit=10&region=Europe`
- `GET /v1/accounts/action-queue?limit=15`
- `GET /v1/accounts/renewal-forecast?horizon_days=120`
- `GET /v1/accounts/<account_id>`
- `GET /v1/accounts/<account_id>/recommendations`

## Data Story

The sample portfolio models B2B software accounts with renewal timing, adoption quality, executive sponsorship, support pressure, and billing reliability signals. That makes the service suitable for discussions around customer success engineering, backend API ownership, operational analytics, and intervention design.

## Production Path

- move the JSON source into a warehouse or service-owned data store
- add authentication, request budgets, and formal service-level objectives
- wire the action queue into CRM, support, or account-management workflows
- publish the OpenAPI contract and version the service as part of a platform catalog

## Automation Disclosure

**Note:** This repository uses automation and AI assistance for planning, initial scaffolding, routine maintenance, and selected code or documentation generation. I review and curate the outputs as part of my portfolio workflow.
