# Frontend overview (русский redesign MVP)

Frontend расположен в `frontend/` и ориентирован на врачей/аналитиков.

## Технологии
- TypeScript
- React + Vite
- Tailwind CSS
- React Router
- react-i18next
- Leaflet / react-leaflet

## Структура интерфейса
- Верхняя русская навигация: «Карта», «Аналитика», «Случаи»
- Левая панель фильтров
- Центральная зона карты
- Правая панель сводки по выбранной территории
- Summary widgets для ключевых метрик

## Локализация
- Инициализация: `frontend/src/i18n.ts`
- Все пользовательские тексты берутся через `useTranslation`
- Текущий базовый язык: русский

## Режимы
- Обычный режим: без технических dev-плашек
- Debug mode (`VITE_DEBUG_MODE=true`): показывает статус backend в хедере

## Карта и геоданные
- Базовая подложка:
  - `VITE_LEGACY_TILE_URL` (если задан)
  - иначе OpenStreetMap
- Если геометрия территорий не подключена (`VITE_MAP_GEOMETRY_ENABLED=false`), UI показывает честное состояние готовности без имитации choropleth.
