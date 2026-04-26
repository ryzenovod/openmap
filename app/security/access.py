from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, Request

from app.core.errors import ForbiddenError
from app.security.roles import ALL_ROLES, Role


def get_request_role(request: Request) -> str:
    role = request.headers.get("X-Role", Role.VIEWER.value).lower()
    if role not in ALL_ROLES:
        raise ForbiddenError(
            message=f"Unknown role: {role}", details={"allowed_roles": sorted(ALL_ROLES)}
        )
    request.state.role = role
    return role


def require_roles(*required_roles: Role) -> Callable:
    allowed = {role.value for role in required_roles}

    def checker(role: str = Depends(get_request_role)) -> str:
        if role not in allowed:
            raise ForbiddenError(
                message="Role is not allowed for this endpoint",
                details={"required_roles": sorted(allowed), "provided_role": role},
            )
        return role

    return checker
