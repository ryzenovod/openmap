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

Legacy raster tiles подключаются как базовая фоновая подложка Leaflet через env-переменную frontend.
По `legacy_scan/tile_sample_files.txt` фактическое расширение тайлов: `.png`, поэтому шаблон должен быть с `{y}.png`.

```env
# frontend/.env
VITE_LEGACY_TILE_URL=http://localhost:8081/tiles/{z}/{x}/{y}.png
```

Если переменная не задана или tiles недоступны, карта показывает состояние:

> «Локальная картографическая подложка не подключена»

Полный каталог tiles весит около 20 GB, не лежит в git и не должен копироваться в репозиторий.
Для Docker Compose используйте bind mount через пример override:

```bash
LEGACY_TILES_DIR=/path/to/local/legacy/tiles \
  docker compose -f docker-compose.yml -f docker-compose.override.example.yml up --build
```

Для локального запуска без Docker можно создать symlink в публичную директорию Vite:

```bash
mkdir -p frontend/public/tileserver
ln -s /path/to/local/legacy/tiles frontend/public/tileserver/tiles
```

Путь `frontend/public/tileserver/tiles` добавлен в `.gitignore`.

### Геометрия территорий

В репозитории не обнаружены готовые GeoJSON/polygon-границы для полноценного choropleth.
Поэтому при отсутствии подключённых геоданных frontend честно показывает состояние:

> «Карта готова к работе, но не загружены территориальные границы/геоданные»

Backend готовит отдельную PostGIS-таблицу `core.territory_geometry`. Legacy raster tiles остаются только фоновой подложкой; choropleth строится только по реальным векторным границам.

Ожидаемый локальный файл:

```text
data/boundaries/primorye_territories.geojson
```

Ожидаемый формат:

```jsonc
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "territory_id": 10,
        "territory_name": "Название территории",
        "level": "municipality"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [/* непустой GeoJSON coordinates-массив */]
      }
    }
  ]
}
```

`properties.territory_id` связывает геометрию с агрегатами `/api/v1/map/aggregate` по `row.territory_id`. Если агрегатов нет, территория отображается нейтрально. Если геометрия есть, но агрегата по ней нет, стиль также нейтральный.

Импорт в Docker Compose:

```bash
docker compose exec api python -m app.scripts.import_boundaries
```

Можно передать явный путь внутри контейнера:

```bash
docker compose exec api python -m app.scripts.import_boundaries /app/data/boundaries/primorye_territories.geojson
```

Проверка GeoJSON endpoint:

```bash
curl http://localhost:8000/api/v1/map/territories.geojson
```

Если геометрии ещё не импортированы, endpoint возвращает пустой `FeatureCollection`, а frontend продолжает показывать raster-карту с неблокирующим сообщением:

> «Векторные границы территорий пока не загружены»

Флаг:

```env
VITE_MAP_GEOMETRY_ENABLED=true
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
