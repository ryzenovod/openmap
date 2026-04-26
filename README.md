# Медгеосистема

Внутренний backend-first проект медицинской геоаналитики.

## Быстрый запуск (Docker Compose)

1) Перед запуском (особенно после изменения `docker-compose.yml`) очистите старые сервисы и orphan-контейнеры:

```bash
docker compose down --remove-orphans
```

2) Поднимите стек:

```bash
docker compose up --build
```

После старта:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health: http://localhost:8000/health

> В текущем compose база данных **не публикуется на хост**. Backend подключается к БД внутри compose-сети по адресу `db:5432`.

---

## Что сделано для более устойчивого startup API

`api` теперь стартует в таком порядке:
1. wait-loop на DNS-резолв `db`;
2. wait-loop на TCP/DB соединение с Postgres;
3. `alembic upgrade head`;
4. запуск `uvicorn`.

Это уменьшает флаки при старте, когда БД уже поднялась как контейнер, но ещё не готова принимать подключения.

---

## Как запускать в ручном режиме для разработки

### Backend локально + БД в Docker

```bash
# 1) поднять только БД
docker compose up -d db

# 2) backend локально
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]

# ВАЖНО: если запускаете backend не в compose, db:5432 недоступен с хоста.
# Нужен локальный PostgreSQL или временный override compose с пробросом порта.
make migrate
make seed
make run
```

### Frontend локально

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Troubleshooting

### 1) Orphan containers

Симптомы: неожиданные ошибки старта после изменений compose-сервисов.

Решение:

```bash
docker compose down --remove-orphans
docker compose up --build
```

### 2) Конфликт порта на хосте

Симптомы: `Bind for 0.0.0.0:8000 failed` или аналогично для `5173`.

Решение:
- освободить порт занятым процессом;
- либо изменить publish-порт в `docker-compose.yml` для соответствующего сервиса.

### 3) `failed to resolve host 'db'`

Причина: сервис `api` запускается вне compose-сети или сеть compose в неконсистентном состоянии.

Решение:
1. Убедиться, что `api` запущен через `docker compose up`.
2. Выполнить полную перезагрузку стека:

```bash
docker compose down --remove-orphans
docker compose up --build
```

3. Если backend запускается локально (не в контейнере), использовать доступный хост БД (не `db`).

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
