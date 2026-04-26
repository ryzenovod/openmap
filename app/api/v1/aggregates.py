from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.common import PeriodFilterQuery, envelope
from app.security.access import require_roles
from app.security.roles import Role
from app.services.aggregates.charts import charts_structure, yearly_dynamics
from app.services.aggregates.map import aggregate_map

router = APIRouter(prefix="/api/v1", tags=["aggregates"])


@router.get(
    "/map/aggregate",
    dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.VIEWER))],
)
def map_aggregate(
    filters: PeriodFilterQuery = Depends(),
    level: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    rows = aggregate_map(db, date_from=filters.date_from, date_to=filters.date_to, level=level)
    return envelope(rows, meta={"count": len(rows), "level": level})


@router.get(
    "/charts/yearly",
    dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.VIEWER))],
)
def charts_yearly(filters: PeriodFilterQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    rows = yearly_dynamics(db, date_from=filters.date_from, date_to=filters.date_to)
    return envelope(rows, meta={"count": len(rows)})


@router.get(
    "/charts/structure",
    dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.VIEWER))],
)
def charts_structure_endpoint(
    filters: PeriodFilterQuery = Depends(), db: Session = Depends(get_db)
) -> dict:
    rows = charts_structure(db, date_from=filters.date_from, date_to=filters.date_to)
    return envelope(rows)
