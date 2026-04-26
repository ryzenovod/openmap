# Medical Geo Analytics Platform

Backend внутренней медицинской геоаналитической системы (итерация 3 MVP).

## Реализовано
- FastAPI backend + `GET /health`
- SQLAlchemy модели для `staging`, `core`, `mart`
- Alembic migrations:
  - `20260426_0001`: PostGIS + schemas
  - `20260426_0002`: таблицы staging/core
  - `20260426_0003`: таблицы mart + индексы
- Seed scripts:
  - `legacy_assets/dictionaries/mkb10Codes.csv`
  - `legacy_assets/dictionaries/territories.csv`
  - `legacy_assets/dictionaries/populations.csv`
  - справочники статусов (`gdu/cv/mbt/found/case_type/location_role`)
- Importer MVP для synthetic CSV:
  - import batch + raw rows
  - validation/date normalization
  - dictionary mapping
  - conservative dedup v0.1
  - row-level errors
- Aggregate services (mart-backed):
  - map aggregates: территория, период, case/cv+/mbt+, children count, incidence per 100k, level filter
  - chart aggregates: yearly dynamics, structure by MKB, structure by sex, structure by age group, territorial comparison
- API endpoints:
  - `POST /api/v1/imports/cases`
  - `GET /api/v1/imports`
  - `GET /api/v1/dictionaries/mkb10`
  - `GET /api/v1/territories`
  - `GET /api/v1/territories/tree`
  - `GET /api/v1/cases`
  - `GET /api/v1/cases/{id}`
  - `GET /api/v1/map/aggregate`
  - `GET /api/v1/charts/yearly`
  - `GET /api/v1/charts/structure`
- Tests:
  - importer/date normalization/dictionary mapping/dedup
  - aggregate services
  - API tests for `/health`, `/territories`, `/imports`, `/api/v1/map/aggregate`, `/api/v1/charts/yearly`, `/api/v1/charts/structure`

## Пока не реализовано
- frontend
- auth provider
- forecasting
- AI
- background jobs
- external integrations

## Быстрый старт
```bash
docker compose up --build
```

API будет доступен на `http://localhost:8000`.

## Локальная разработка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

# применить миграции
alembic upgrade head

# загрузить словари
python -m app.scripts.seed

# запустить API
uvicorn app.main:app --reload
```

## Импорт synthetic CSV
```bash
curl -X POST "http://localhost:8000/api/v1/imports/cases" \
  -F "file=@samples/csv/cases_sample.csv"
```

## Aggregates
```bash
curl "http://localhost:8000/api/v1/map/aggregate?date_from=2025-01-01&date_to=2025-12-31"
curl "http://localhost:8000/api/v1/charts/yearly"
curl "http://localhost:8000/api/v1/charts/structure"
```

## Тесты
```bash
pytest
```
