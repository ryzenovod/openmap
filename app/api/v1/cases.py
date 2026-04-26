from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.core import MedicalCase

router = APIRouter(prefix="/api/v1/cases", tags=["cases"])


@router.get("")
def list_cases(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)) -> list[dict]:
    rows = db.execute(select(MedicalCase).order_by(MedicalCase.id).limit(limit).offset(offset)).scalars().all()
    return [
        {
            "id": c.id,
            "patient_id": c.patient_id,
            "legacy_case_num": c.legacy_case_num,
            "registration_date": c.registration_date.isoformat(),
            "diagnosis_raw": c.diagnosis_raw,
        }
        for c in rows
    ]


@router.get("/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)) -> dict:
    c = db.get(MedicalCase, case_id)
    if not c:
        raise HTTPException(status_code=404, detail="case not found")
    return {
        "id": c.id,
        "patient_id": c.patient_id,
        "legacy_case_num": c.legacy_case_num,
        "registration_date": c.registration_date.isoformat(),
        "diagnosis_raw": c.diagnosis_raw,
        "gdu_code": c.gdu_code,
        "cv_code": c.cv_code,
        "mbt_code": c.mbt_code,
    }
