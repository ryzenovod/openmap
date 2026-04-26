from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.core import DictMkb10

router = APIRouter(prefix="/api/v1/dictionaries", tags=["dictionaries"])


@router.get("/mkb10")
def list_mkb10(limit: int = 200, offset: int = 0, db: Session = Depends(get_db)) -> list[dict]:
    rows = db.execute(select(DictMkb10).order_by(DictMkb10.id).limit(limit).offset(offset)).scalars().all()
    return [{"id": x.id, "parent_id": x.parent_id, "code": x.code, "name": x.name} for x in rows]
