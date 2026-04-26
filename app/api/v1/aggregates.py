from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.aggregates.charts import charts_structure, yearly_dynamics
from app.services.aggregates.common import parse_date
from app.services.aggregates.map import aggregate_map

router = APIRouter(prefix="/api/v1", tags=["aggregates"])


@router.get("/map/aggregate")
def map_aggregate(
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    level: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[dict]:
    return aggregate_map(
        db,
        date_from=parse_date(date_from),
        date_to=parse_date(date_to),
        level=level,
    )


@router.get("/charts/yearly")
def charts_yearly(
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[dict]:
    return yearly_dynamics(db, date_from=parse_date(date_from), date_to=parse_date(date_to))


@router.get("/charts/structure")
def charts_structure_endpoint(
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    return charts_structure(db, date_from=parse_date(date_from), date_to=parse_date(date_to))
