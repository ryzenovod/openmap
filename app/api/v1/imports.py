from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.models.staging import StgImportBatch
from app.services.importer import import_cases_csv

router = APIRouter(prefix="/api/v1/imports", tags=["imports"])


@router.post("/cases")
async def import_cases(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    payload = await file.read()
    result = import_cases_csv(db, filename=file.filename or "upload.csv", payload_bytes=payload)
    return result.__dict__


@router.get("")
def list_imports(db: Session = Depends(get_db)) -> list[dict]:
    batches = db.execute(select(StgImportBatch).order_by(desc(StgImportBatch.id))).scalars().all()
    return [
        {
            "id": b.id,
            "source_filename": b.source_filename,
            "total_rows": b.total_rows,
            "success_rows": b.success_rows,
            "error_rows": b.error_rows,
            "created_at": b.created_at.isoformat(),
        }
        for b in batches
    ]
