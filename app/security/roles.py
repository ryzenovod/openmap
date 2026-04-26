from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    ANALYST = "analyst"
    DOCTOR = "doctor"
    MANAGER = "manager"
    VIEWER = "viewer"


ALL_ROLES = {role.value for role in Role}
