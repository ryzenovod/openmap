# Medical Geo Analytics Platform

Внутренний backend-first проект медицинской геоаналитики.

## Запуск Docker Compose с нуля

Рекомендуемая последовательность (особенно после изменения `docker-compose.yml`):

```bash
docker compose down --remove-orphans
docker compose up --build
```

После старта:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health: http://localhost:8000/health

> База данных в compose не публикуется на хост. Backend подключается к ней внутри сети compose по `db:5432`.

---

## Устойчивый startup API

`api` стартует в порядке:
1. ожидание DNS для `db`;
2. ожидание подключения к Postgres (`db:5432`);
3. `alembic upgrade head`;
4. запуск `uvicorn`.

Это снижает флаки при старте после `up --build`.

---

## Troubleshooting

### 1) Занят порт 8000

Симптом: ошибка bind на `0.0.0.0:8000`.

Что делать:
1. Освободить порт процессом, который его занимает.
2. Либо поменять порт в `docker-compose.yml` у сервиса `api` (например `8001:8000`).

### 2) `failed to resolve host 'db'`

Симптом: API не может резолвить hostname `db`.

Что делать:
1. Убедиться, что API запущен через compose, а не локально вне сети compose.
2. Полностью перезапустить стек:

```bash
docker compose down --remove-orphans
docker compose up --build
```

### 3) Orphan containers

Симптом: после правок compose появляются странные конфликты сервисов/сетей.

Что делать:

```bash
docker compose down --remove-orphans
docker compose up --build
```

---

## Команды разработки

### Backend
```bash
make lint
make test
make ci
make migrate
make seed
```

### Frontend
```bash
cd frontend
npm run lint
npm run test
npm run build
npm run dev
```
