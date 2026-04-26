# Frontend MVP (OpenMap)

Минимальный frontend для работы с текущим backend API.

## Стек
- TypeScript
- React
- Vite
- React Router
- Leaflet (`react-leaflet`)

## Быстрый запуск

```bash
npm install
cp .env.example .env
npm run dev
```

Приложение будет доступно на http://localhost:5173.

## Скрипты
- `npm run dev` — dev сервер с hot reload
- `npm run build` — production build
- `npm run lint` — eslint
- `npm run test` — vitest scaffold

## Переменные окружения
Файл `.env`:

- `VITE_API_BASE_URL=http://localhost:8000`
- `VITE_API_ROLE=viewer`

## Запуск в составе полного стека
Из корня репозитория:

```bash
docker compose up --build
```

В этом режиме frontend также запускается в dev-контейнере с volume mount для кода.
