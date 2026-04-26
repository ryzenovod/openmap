# Медгеосистема

Внутренний backend-first проект медицинской геоаналитики.

## Что в репозитории сейчас

### Backend
- FastAPI API (`/health`, imports, dictionaries, territories, cases, aggregates)
- Слои данных `staging` / `core` / `mart`
- Alembic миграции (`0001..0003`)
- Seed-скрипты словарей
- MVP importer CSV
- MVP aggregate services (map/charts)
- Тесты (`pytest`)

### Frontend
- Отдельное приложение в `frontend/` (TypeScript + React + Vite + Leaflet)
- MVP страницы:
  - карта + фильтры + summary
  - графики
  - cases list + case details
- Базовый API client с поддержкой backend error envelope

---

## Быстрый старт одной командой (рекомендуется)

Поднимает весь стек: **db + backend + frontend**.

```bash
docker compose up --build
```

После запуска:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health: http://localhost:8000/health
- Postgres/PostGIS: localhost:5432

---

## Альтернативный ручной запуск для разработки

### 1) Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

make migrate
make seed
make run
```

### 2) Frontend
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

## Переменные окружения (frontend)

Файл: `frontend/.env`

- `VITE_API_BASE_URL` — URL backend для браузера (по умолчанию `http://localhost:8000`)
- `VITE_API_ROLE` — роль для access-stub заголовка `X-Role` (по умолчанию `viewer`)

---

## Что не входит в текущий scope
- production auth
- forecasting
- AI
- background jobs
- внешние интеграции
- production deployment/hardening
