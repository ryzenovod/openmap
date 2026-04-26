# Frontend MVP (OpenMap)

Минимальный frontend для работы с backend API.

## Стек
- TypeScript
- React
- Vite
- React Router
- Leaflet (`react-leaflet`)

## Режим 1: запуск одной командой вместе со всем стеком

Из корня репозитория:

```bash
docker compose up --build
```

После запуска frontend доступен на http://localhost:5173.

## Режим 2: ручной запуск frontend для разработки

```bash
npm install
cp .env.example .env
npm run dev
```

Frontend будет доступен на http://localhost:5173.

### Требования к backend в ручном режиме

Frontend ожидает backend по `VITE_API_BASE_URL` (по умолчанию `http://localhost:8000`).
Если backend запущен на другом адресе — измените `.env`.

## Скрипты
- `npm run dev` — dev сервер с hot reload
- `npm run build` — production build
- `npm run lint` — eslint
- `npm run test` — vitest scaffold

## Переменные окружения
Файл `.env`:

- `VITE_API_BASE_URL=http://localhost:8000`
- `VITE_API_ROLE=viewer`
