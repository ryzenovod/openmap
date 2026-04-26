from fastapi import APIRouter, Depends
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.common import PaginationQuery, SortingQuery, envelope
from app.db.models.core import DictMkb10
from app.security.access import require_roles
from app.security.roles import Role

router = APIRouter(prefix="/api/v1/dictionaries", tags=["dictionaries"])


@router.get(
    "/mkb10",
    dependencies=[
        Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.DOCTOR, Role.MANAGER, Role.VIEWER))
    ],
)
def list_mkb10(
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    order_column = DictMkb10.code if sorting.sort_by == "code" else DictMkb10.id
    order = desc(order_column) if sorting.sort_order == "desc" else asc(order_column)
    rows = (
        db.execute(
            select(DictMkb10).order_by(order).limit(pagination.limit).offset(pagination.offset)
        )
        .scalars()
        .all()
    )
    payload = [{"id": x.id, "parent_id": x.parent_id, "code": x.code, "name": x.name} for x in rows]
    return envelope(
        payload,
        meta={"limit": pagination.limit, "offset": pagination.offset, "count": len(payload)},
    )
