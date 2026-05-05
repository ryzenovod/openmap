# Frontend (русский интерфейс для врачей и аналитиков)

Frontend переведён на русский язык и переработан в более современный, сдержанный UI.

## Что изменено в этой итерации

- Полная русификация пользовательского интерфейса.
- Локализация через `react-i18next` (`src/i18n.ts`), тексты вынесены из компонентов.
- Обновлён layout: верхняя навигация, панель фильтров, карта, правая панель сводки, виджеты.
- Убраны developer-style формулировки и технический бейдж backend из обычного режима.
- Добавлены понятные пустые состояния и русские сообщения ошибок.

## Запуск

```bash
npm install
cp .env.example .env
npm run dev
```

## Debug mode

Включается через `.env`:

```env
VITE_DEBUG_MODE=true
```

В debug-режиме показывается статус backend в хедере.

## Как работает локализация

- Инициализация: `src/i18n.ts`
- Подключение: `src/main.tsx`
- Использование: `useTranslation()` в компонентах/страницах

Сейчас активен русский язык (`ru`) как основной.

## Legacy tiles

Legacy raster tiles подключаются как базовая подложка Leaflet через `VITE_LEGACY_TILE_URL`.
В `legacy_scan/tile_sample_files.txt` образцы имеют расширение `.png`, поэтому используется шаблон:

```env
VITE_LEGACY_TILE_URL=/tileserver/tiles/{z}/{x}/{y}.png
```

Если переменная пуста или tiles не отдаются браузеру, интерфейс показывает:

> «Локальная картографическая подложка не подключена»

Каталог tiles не хранится в репозитории. Локально он находится вне проекта:

```text
/Users/ryzenovod/cancerMap/public/tileserver/tiles
```

Для локального `npm run dev` можно подключить его symlink:

```bash
mkdir -p public/tileserver
ln -s /Users/ryzenovod/cancerMap/public/tileserver/tiles public/tileserver/tiles
```

Для Docker Compose используйте `docker-compose.override.example.yml` из корня проекта:

```bash
LEGACY_TILES_DIR=/Users/ryzenovod/cancerMap/public/tileserver/tiles \
  docker compose -f docker-compose.yml -f docker-compose.override.example.yml up --build
```

## Что нужно для полноценной тематической карты

Для реального choropleth/границ нужны территориальные геоданные (GeoJSON/polygons).

Если геометрии нет, UI честно показывает состояние:

> «Карта готова к работе, но не загружены территориальные границы/геоданные»

Флаг состояния:

```env
VITE_MAP_GEOMETRY_ENABLED=false
```
