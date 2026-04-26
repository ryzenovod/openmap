# Медгеосистема

Backend внутренней медицинской геоаналитической системы (итерация 2 MVP).

## Реализовано
- FastAPI backend + `GET /health`
- SQLAlchemy модели для `staging` и `core`
- Alembic migrations:
  - `20260426_0001`: PostGIS + schemas
  - `20260426_0002`: таблицы staging/core
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
- API endpoints:
  - `POST /api/v1/imports/cases`
  - `GET /api/v1/imports`
  - `GET /api/v1/dictionaries/mkb10`
  - `GET /api/v1/territories`
  - `GET /api/v1/territories/tree`
  - `GET /api/v1/cases`
  - `GET /api/v1/cases/{id}`
- Tests:
  - importer/date normalization/dictionary mapping/dedup
  - API tests for `/health`, `/territories`, `/imports`

## Пока не реализовано
- map aggregates
- chart aggregates
- frontend
- auth provider
- forecasting
- AI

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

## Тесты
```bash
pytest
```
