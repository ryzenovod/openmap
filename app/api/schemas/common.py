from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field


class PaginationQuery(BaseModel):
    limit: int = Field(default=100, ge=1, le=500)
    offset: int = Field(default=0, ge=0)


class SortingQuery(BaseModel):
    sort_by: str = "id"
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$")


class PeriodFilterQuery(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


def envelope(data, meta: dict | None = None) -> dict:
    return {"data": data, "meta": meta or {}}
