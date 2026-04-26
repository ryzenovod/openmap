# ADR 0002: Data layering

## Status
Accepted

## Decision
Adopt 3-layer data architecture:
- `staging` for raw imports and row-level errors
- `core` for normalized operational entities
- `mart` for aggregate/query-optimized projections

## Rationale
- Keeps importer traceability and replay safety.
- Isolates domain model from reporting/aggregation concerns.
- Enables iterative analytics evolution without breaking ingest pipeline.
