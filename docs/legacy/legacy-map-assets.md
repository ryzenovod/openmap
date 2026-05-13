# Legacy map assets

В legacy-проекте карта хранится как локальный raster tileset.

## Найдено

- legacy tiles path: `/Users/ryzenovod/cancerMap/public/tileserver/tiles`
- tiles size: около 20 GB
- tiles format: z/x/y raster tile structure
- leaflet assets: `public/tileserver/leaflet.js`, `leaflet.css`, `leaflet-heat.js`, `images`
- map tools: `public/tileserver/download-tiles.js`, `download-tiles.ts`, `map-gen`

## Важно

Полный каталог `tiles` НЕ коммитится в git, потому что он слишком большой.

Для локального запуска карту нужно подключать через bind mount из локальной legacy-папки.

Ожидаемый URL-шаблон для Leaflet:

`/legacy-tiles/{z}/{x}/{y}.png`

или другой фактический шаблон после проверки расширений файлов.

## Геометрия

Автоматический поиск не нашёл GeoJSON / SHP / KML / MBTiles.

Это значит:
- legacy даёт только фоновую raster-подложку карты;
- территориальные границы районов/муниципалитетов нужно искать отдельно;
- полноценный choropleth невозможен без territorial geometry.

## Choropleth и GeoJSON

Backend ожидает реальные границы в локальном файле:

```text
data/boundaries/primorye_territories.geojson
```

Минимальные требования к FeatureCollection:
- `properties.territory_id` — основной ключ связи с агрегатами `row.territory_id`;
- `properties.territory_name` — отображаемое имя территории;
- `properties.level` — необязательный уровень территории;
- `geometry.type` — `Polygon` или `MultiPolygon`, сохраняется как `geometry(MultiPolygon, 4326)`.

Проверка endpoint:

```bash
curl http://localhost:8000/api/v1/map/territories.geojson
```

Если геометрии не загружены, endpoint возвращает пустой `FeatureCollection`. Frontend при этом продолжает показывать legacy raster layer и неблокирующее сообщение о том, что векторные границы пока не загружены.

## Что нужно реализовать

1. Добавить frontend-настройку `VITE_LEGACY_TILE_URL`.
2. Добавить локальный docker compose bind mount для tiles.
3. Подключить Leaflet tile layer.
4. Если tiles недоступны — показывать понятное русское сообщение.
5. Не имитировать территориальные полигоны, пока нет GeoJSON/геометрии.
