from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.common import PaginationQuery, SortingQuery, envelope
from app.db.models.core import Territory
from app.security.access import require_roles
from app.security.roles import Role

router = APIRouter(prefix="/api/v1/territories", tags=["territories"])


@router.get(
    "",
    dependencies=[
        Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.DOCTOR, Role.MANAGER, Role.VIEWER))
    ],
)
def list_territories(
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    order_column = Territory.name if sorting.sort_by == "name" else Territory.id
    order = desc(order_column) if sorting.sort_order == "desc" else asc(order_column)
    rows = (
        db.execute(
            select(Territory).order_by(order).limit(pagination.limit).offset(pagination.offset)
        )
        .scalars()
        .all()
    )
    data = [
        {
            "id": t.id,
            "parent_id": t.parent_id,
            "name": t.name,
            "territory_type_code": t.territory_type_code,
        }
        for t in rows
    ]
    return envelope(
        data, meta={"limit": pagination.limit, "offset": pagination.offset, "count": len(data)}
    )


@router.get(
    "/tree",
    dependencies=[
        Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.DOCTOR, Role.MANAGER, Role.VIEWER))
    ],
)
def territories_tree(db: Session = Depends(get_db)) -> dict:
    rows = db.execute(select(Territory).order_by(Territory.id)).scalars().all()
    by_parent = defaultdict(list)
    items = {}
    for t in rows:
        item = {
            "id": t.id,
            "name": t.name,
            "territory_type_code": t.territory_type_code,
            "children": [],
        }
        by_parent[t.parent_id].append(item)
        items[t.id] = item
    for t in rows:
        if t.parent_id in items:
            items[t.parent_id]["children"].append(items[t.id])
    return envelope(by_parent[None], meta={"count": len(by_parent[None])})
