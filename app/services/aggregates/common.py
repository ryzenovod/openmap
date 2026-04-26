from __future__ import annotations

from datetime import date


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def age_group(birth_year: int | None, case_year: int) -> str:
    if not birth_year:
        return "unknown"
    age = case_year - birth_year
    if age < 18:
        return "0-17"
    if age < 35:
        return "18-34"
    if age < 50:
        return "35-49"
    if age < 65:
        return "50-64"
    return "65+"
