from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.core import Territory

router = APIRouter(prefix="/api/v1/territories", tags=["territories"])


@router.get("")
def list_territories(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.execute(select(Territory).order_by(Territory.id)).scalars().all()
    return [
        {
            "id": t.id,
            "parent_id": t.parent_id,
            "name": t.name,
            "territory_type_code": t.territory_type_code,
        }
        for t in rows
    ]


@router.get("/tree")
def territories_tree(db: Session = Depends(get_db)) -> list[dict]:
    rows = db.execute(select(Territory).order_by(Territory.id)).scalars().all()
    by_parent = defaultdict(list)
    items = {}
    for t in rows:
        item = {"id": t.id, "name": t.name, "territory_type_code": t.territory_type_code, "children": []}
        by_parent[t.parent_id].append(item)
        items[t.id] = item
    for t in rows:
        if t.parent_id in items:
            items[t.parent_id]["children"].append(items[t.id])
    return by_parent[None]
