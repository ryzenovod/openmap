# Medical Geo Analytics Platform

Backend skeleton для внутренней медицинской геоаналитической системы (первая итерация MVP).

## Что реализовано в этой итерации
- FastAPI skeleton (`app/main.py`)
- Endpoint `GET /health`
- SQLAlchemy 2.x Base и engine/session scaffolding
- Alembic конфигурация
- Initial migration:
  - `CREATE EXTENSION IF NOT EXISTS postgis`
  - создание schema: `staging`, `core`, `mart`
- Dockerfile для API
- `docker-compose.yml` для API + PostgreSQL/PostGIS

## Что пока **не** реализовано
- importer CSV
- seed scripts
- business API (`/api/v1/cases`, `/api/v1/territories`, aggregates)
- frontend

## Структура проекта
- `app/` — FastAPI приложение и DB foundation
- `alembic/` — миграции
- `docs/` — предметная документация и reference
- `legacy_assets/dictionaries/` — legacy словари (reference only)
- `samples/csv/` — synthetic примеры CSV

## Быстрый старт
```bash
docker compose up --build
```

После старта:
- API: http://localhost:8000
- Healthcheck: http://localhost:8000/health

## Локальный запуск без Docker
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .

# указать OPENMAP_DATABASE_URL при необходимости
alembic upgrade head
uvicorn app.main:app --reload
```

## Миграции
Создать новую миграцию:
```bash
alembic revision -m "message"
```

Применить миграции:
```bash
alembic upgrade head
```

## Важно
- Не коммитить реальные медицинские данные и секреты.
- Legacy используется только как reference для словарей/семантики полей.
