# OpenMap Frontend MVP

## Quick start

```bash
npm install
cp .env.example .env
npm run dev
```

## Scripts
- `npm run dev` - start dev server
- `npm run build` - production build
- `npm run lint` - eslint check
- `npm run test` - vitest scaffold

## Backend connection
Frontend expects backend on `VITE_API_BASE_URL` (default `http://localhost:8000`).
Set optional role header with `VITE_API_ROLE`.
