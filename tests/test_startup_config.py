from __future__ import annotations

from pathlib import Path


def test_alembic_version_table_not_forced_to_core_schema() -> None:
    content = Path("alembic/env.py").read_text(encoding="utf-8")
    assert "version_table_schema" not in content


def test_compose_api_startup_fail_fast_chain() -> None:
    content = Path("docker-compose.yml").read_text(encoding="utf-8")
    assert "python -m app.scripts.wait_for_db" in content
    assert "alembic upgrade head" in content
    assert "exec uvicorn app.main:app" in content
