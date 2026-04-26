# API endpoints (iteration 4)

## Access stub
- Header `X-Role` (optional) supports: `admin`, `analyst`, `doctor`, `manager`, `viewer`
- Default role: `viewer`
- Endpoints may require a role subset via dependency stub (no production auth yet)

## Response style
- Most business endpoints return envelope:
  - `data`: payload
  - `meta`: pagination/extra info where applicable

## Error format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Human readable message",
    "details": {}
  }
}
```

## System
- GET /health

## Imports
- POST /api/v1/imports/cases
  - multipart file upload (`.csv`)
- GET /api/v1/imports
  - query: `limit`, `offset`

## Dictionaries
- GET /api/v1/dictionaries/mkb10
  - query: `limit`, `offset`, `sort_by` (`id|code`), `sort_order` (`asc|desc`)

## Territories
- GET /api/v1/territories
  - query: `limit`, `offset`, `sort_by` (`id|name`), `sort_order` (`asc|desc`)
- GET /api/v1/territories/tree

## Cases
- GET /api/v1/cases
  - query: `limit`, `offset`, `sort_by` (`id|registration_date`), `sort_order` (`asc|desc`)
- GET /api/v1/cases/{id}

## Aggregates
- GET /api/v1/map/aggregate
  - query: `date_from`, `date_to`, `level`
- GET /api/v1/charts/yearly
  - query: `date_from`, `date_to`
- GET /api/v1/charts/structure
  - query: `date_from`, `date_to`
