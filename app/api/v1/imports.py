from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.schemas.common import PaginationQuery, envelope
from app.core.errors import ImportError
from app.db.models.staging import StgImportBatch
from app.security.access import require_roles
from app.security.roles import Role
from app.services.importer import import_cases_csv

router = APIRouter(prefix="/api/v1/imports", tags=["imports"])


@router.post("/cases", dependencies=[Depends(require_roles(Role.ADMIN, Role.DOCTOR, Role.MANAGER))])
async def import_cases(file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise ImportError("Only CSV files are supported", details={"filename": file.filename})
    payload = await file.read()
    if not payload:
        raise ImportError("Uploaded file is empty")
    result = import_cases_csv(db, filename=file.filename, payload_bytes=payload)
    return envelope(result.__dict__)


@router.get(
    "", dependencies=[Depends(require_roles(Role.ADMIN, Role.ANALYST, Role.MANAGER, Role.VIEWER))]
)
def list_imports(params: PaginationQuery = Depends(), db: Session = Depends(get_db)) -> dict:
    query = (
        select(StgImportBatch)
        .order_by(desc(StgImportBatch.id))
        .limit(params.limit)
        .offset(params.offset)
    )
    batches = db.execute(query).scalars().all()
    rows = [
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
    return envelope(rows, meta={"limit": params.limit, "offset": params.offset, "count": len(rows)})
