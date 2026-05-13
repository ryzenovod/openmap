# API endpoints (iteration 5)

## Access stub
- Header `X-Role` optional: `admin|analyst|doctor|manager|viewer`
- Default role: `viewer`

## Envelope conventions
- Success envelope for most business endpoints:
  - `data`
  - `meta` (optional)
- Error envelope:
  - `error.code`
  - `error.message`
  - `error.details`

## Endpoints used by frontend MVP
- GET /health
- GET /api/v1/map/aggregate
  - query currently used by UI: `date_from`, `date_to`, `level`
- GET /api/v1/map/territories.geojson
  - returns a raw GeoJSON `FeatureCollection`, not an envelope
  - returns `{"type":"FeatureCollection","features":[]}` when no territory geometries are loaded
- GET /api/v1/charts/yearly
- GET /api/v1/charts/structure
- GET /api/v1/cases
  - query currently used by UI: `limit`, `offset`, `sort_by`, `sort_order`
- GET /api/v1/cases/{id}
- GET /api/v1/territories
- GET /api/v1/territories/tree
- GET /api/v1/dictionaries/mkb10
- POST /api/v1/imports/cases
- GET /api/v1/imports
