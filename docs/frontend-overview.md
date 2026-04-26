# Frontend overview (iteration 5 MVP)

Frontend app lives in `frontend/` and is intentionally minimal.

## Stack
- TypeScript
- React + Vite
- React Router
- Leaflet / react-leaflet

## Pages
- `/` map page:
  - header + sidebar filter panel + map + summary panel
  - backend health status
  - map aggregate data from backend
- `/charts`:
  - yearly dynamics
  - structure snippets (MKB, age groups)
- `/cases`:
  - cases table
  - pagination + sorting
  - details page `/cases/:id`

## Runtime config
- `VITE_API_BASE_URL`
- `VITE_API_ROLE`
