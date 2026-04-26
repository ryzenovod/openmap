from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.security.roles import Role


class AccessStubMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.role = request.headers.get("X-Role", Role.VIEWER.value).lower()
        return await call_next(request)
