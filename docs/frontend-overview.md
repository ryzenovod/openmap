# Frontend overview (итерация MVP)

Frontend находится в `frontend/` и специально остаётся минимальным.

## Технологии
- TypeScript
- React + Vite
- React Router
- Leaflet / react-leaflet

## Страницы
- `/` (карта):
  - header + sidebar/filter panel + map + summary
  - backend health status
  - данные `GET /api/v1/map/aggregate`
- `/charts`:
  - yearly dynamics
  - structure sections
- `/cases`:
  - таблица cases
  - пагинация + сортировка
  - переход на `/cases/:id`

## Конфигурация
- `VITE_API_BASE_URL`
- `VITE_API_ROLE`
