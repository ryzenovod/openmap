from fastapi import FastAPI

from app.api.error_handlers import register_error_handlers
from app.api.v1.aggregates import router as aggregates_router
from app.api.v1.cases import router as cases_router
from app.api.v1.dictionaries import router as dictionaries_router
from app.api.v1.health import router as health_router
from app.api.v1.imports import router as imports_router
from app.api.v1.territories import router as territories_router
from app.config import settings
from app.security.middleware import AccessStubMiddleware

app = FastAPI(title=settings.app_name)
app.add_middleware(AccessStubMiddleware)
register_error_handlers(app)

app.include_router(health_router)
app.include_router(imports_router)
app.include_router(dictionaries_router)
app.include_router(territories_router)
app.include_router(cases_router)
app.include_router(aggregates_router)
