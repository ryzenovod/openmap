# Медгеосистема

Внутренний backend-first проект медицинской геоаналитики.

## Запуск Docker Compose с нуля

```bash
docker compose down --remove-orphans
docker compose up --build
```

После старта:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Health: http://localhost:8000/health

## Frontend: redesign + локализация

В этой итерации frontend переведён на русский и визуально переработан:
- современный спокойный layout (навигация, фильтры, карта, инфо-панель);
- единая i18n-структура через `react-i18next`;
- пустые и ошибочные состояния на русском;
- backend-статус скрыт из обычного режима и доступен только в debug.

### Debug mode frontend

```env
# frontend/.env
VITE_DEBUG_MODE=true
```

### Legacy tiles

```env
# frontend/.env
VITE_LEGACY_TILE_URL=http://localhost:8080/tiles/{z}/{x}/{y}.png
```

Если переменная не задана, используется OpenStreetMap.

### Геометрия территорий

В репозитории не обнаружены готовые GeoJSON/polygon-границы для полноценного choropleth.
Поэтому при отсутствии подключённых геоданных frontend честно показывает состояние:

> «Карта готова к работе, но не загружены территориальные границы/геоданные»

Флаг:

```env
VITE_MAP_GEOMETRY_ENABLED=false
```

---

## Troubleshooting

### Занят порт 8000

Симптом: ошибка bind на `0.0.0.0:8000`.

Решение:
- освободить порт;
- или поменять publish-порт `api` в `docker-compose.yml`.

### `failed to resolve host 'db'`

Симптом: API не может резолвить hostname `db`.

Решение:

```bash
docker compose down --remove-orphans
docker compose up --build
```

### Orphan containers

```bash
docker compose down --remove-orphans
docker compose up --build
```
