# Medical Geo Analytics Platform

Внутренний backend-first проект медицинской геоаналитики.

## Что есть в репозитории

### Backend
- FastAPI API (`/health`, imports, dictionaries, territories, cases, aggregates)
- Слои данных `staging` / `core` / `mart`
- Alembic миграции
- Seed-скрипты словарей
- MVP importer CSV
- Тесты (`pytest`)

### Frontend
- Отдельное приложение в `frontend/` (TypeScript + React + Vite + Leaflet)
- MVP страницы: карта, графики, список cases

---

## Режим 1: запуск одной командой через Docker Compose (рекомендуется)

```bash
docker compose up --build
```

После запуска:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health endpoint: http://localhost:8000/health
- PostgreSQL на хосте: `localhost:5433` (в контейнерной сети backend подключается к `db:5432`)

### Примечание для Apple Silicon (M1/M2/M3)

Если у вас warning про platform mismatch для образов, запустите compose так:

```bash
DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose up --build
```

Используйте это только при необходимости; на большинстве окружений текущий запуск работает без дополнительных флагов.

---

## Режим 2: ручной запуск backend/frontend для разработки

### 1) Поднять только БД в Docker

```bash
docker compose up -d db
```

БД будет доступна с хоста по `localhost:5433`.

### 2) Запустить backend локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

export OPENMAP_DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/openmap
make migrate
make seed
make run
```

### 3) Запустить frontend локально

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Команды разработки

### Backend
```bash
make lint      # ruff + black --check
make test      # pytest
make ci        # compile + lint + tests
make migrate   # alembic upgrade head
make seed      # загрузка словарей
```

### Frontend
```bash
cd frontend
npm run lint
npm run test
npm run build
npm run dev
```

---

## Что не входит в текущий scope
- production auth
- forecasting
- AI
- background jobs
- внешние интеграции
- production deployment/hardening
