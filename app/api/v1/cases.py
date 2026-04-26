from fastapi import APIRouter, Depends
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.common import PaginationQuery, SortingQuery, envelope
from app.core.errors import NotFoundError
from app.db.models.core import MedicalCase
from app.security.access import require_roles
from app.security.roles import Role

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])


@router.get(
    "",
    dependencies=[
        Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.DOCTOR, Role.MANAGER, Role.VIEWER))
    ],
)
def list_cases(
    pagination: PaginationQuery = Depends(),
    sorting: SortingQuery = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    order_column = (
        MedicalCase.registration_date if sorting.sort_by == "registration_date" else MedicalCase.id
    )
    order = desc(order_column) if sorting.sort_order == "desc" else asc(order_column)
    rows = (
        db.execute(
            select(MedicalCase).order_by(order).limit(pagination.limit).offset(pagination.offset)
        )
        .scalars()
        .all()
    )
    data = [
        {
            "id": c.id,
            "patient_id": c.patient_id,
            "legacy_case_num": c.legacy_case_num,
            "registration_date": c.registration_date.isoformat(),
            "diagnosis_raw": c.diagnosis_raw,
        }
        for c in rows
    ]
    return envelope(
        data, meta={"limit": pagination.limit, "offset": pagination.offset, "count": len(data)}
    )


@router.get(
    "/{case_id}",
    dependencies=[
        Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.DOCTOR, Role.MANAGER, Role.VIEWER))
    ],
)
def get_case(case_id: int, db: Session = Depends(get_db)) -> dict:
    c = db.get(MedicalCase, case_id)
    if not c:
        raise NotFoundError("Case not found", details={"case_id": case_id})
    return envelope(
        {
            "id": c.id,
            "patient_id": c.patient_id,
            "legacy_case_num": c.legacy_case_num,
            "registration_date": c.registration_date.isoformat(),
            "diagnosis_raw": c.diagnosis_raw,
            "gdu_code": c.gdu_code,
            "cv_code": c.cv_code,
            "mbt_code": c.mbt_code,
        }
    )
