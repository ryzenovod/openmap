# Медгеосистема

Backend-first medical geo analytics service (iteration 4 MVP).

## Implemented
- FastAPI backend and healthcheck (`GET /health`)
- `staging` / `core` / `mart` SQLAlchemy models
- Alembic migrations `0001..0003`
- Seed scripts for dictionaries and reference statuses
- CSV importer MVP with normalization, mapping, conservative dedup, row-level errors
- Aggregation services and endpoints for map/charts
- Role/access skeleton (stub): `admin`, `analyst`, `doctor`, `manager`, `viewer`
- Unified error response layer (`error.code/message/details`)
- Unified API style for pagination/sorting/filter DTOs and response envelopes where applicable
- Dev workflow tooling: `Makefile`, `.pre-commit-config.yaml`, `ruff`/`black`
- CI workflow: install, lint, tests, compile/import smoke

## Not implemented (by design)
- frontend
- production auth provider
- forecasting
- AI
- background jobs
- external integrations

## Quickstart (Docker)
```bash
docker compose up --build
```

## Local dev (without Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

make migrate
make seed
make run
```

## Commands reference
```bash
make install   # install project with dev deps
make run       # run FastAPI in reload mode
make test      # run pytest
make lint      # ruff + black --check
make format    # autofix formatting
make migrate   # alembic upgrade head
make seed      # load dictionaries
make ci        # compile + lint + tests
```

## Role stub usage
- Optional header: `X-Role`
- Allowed values: `admin|analyst|doctor|manager|viewer`
- No token/user integration yet (stub only)

## API examples
```bash
curl -H "X-Role: analyst" "http://localhost:8000/api/v1/charts/yearly?date_from=2025-01-01&date_to=2025-12-31"
curl -H "X-Role: viewer" "http://localhost:8000/api/v1/territories?limit=20&offset=0&sort_by=name&sort_order=asc"
```

## Tests
```bash
pytest
pytest -q tests/test_importer.py
pytest -q tests/test_api.py tests/test_api_aggregates.py
```
