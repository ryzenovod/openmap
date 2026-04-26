# ADR 0001: Technology stack

## Status
Accepted

## Decision
Use Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL/PostGIS, pytest, Docker Compose.

## Rationale
- FastAPI gives fast API iteration and typed contracts.
- SQLAlchemy + Alembic fits schema-first controlled migrations.
- PostgreSQL/PostGIS supports geo analytics needs.
- pytest and Docker Compose simplify deterministic local workflow.
