# Медгеосистема

Backend + Frontend MVP (iteration 5).

## Implemented backend
- FastAPI backend, importer, aggregates, role/access stub, unified error envelope
- staging/core/mart schemas and Alembic migrations
- tests, CI, dev tooling (`Makefile`, lint/format/test)

## Implemented frontend MVP
- New standalone TypeScript app in `frontend/` (Vite + React + Leaflet)
- Vertical slices:
  - map page (layout + filters + map aggregate data + metric details panel)
  - charts page (yearly + structure blocks)
  - cases page (table, pagination/sorting, case details)
- Backend health-check integration and reusable loading/empty/error components
- API client supporting backend error envelope format

## Quickstart backend
```bash
docker compose up --build
```

## Local backend dev
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

make migrate
make seed
make run
```

## Frontend startup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend default URL: `http://localhost:5173`  
Backend expected URL: `http://localhost:8000` (override via `VITE_API_BASE_URL`)

## Commands
```bash
# backend
make lint
make test
make ci

# frontend
cd frontend
npm run lint
npm run test
npm run build
```

## Not in scope
- production auth
- forecasting/AI
- background jobs
- external integrations
- polished design system
