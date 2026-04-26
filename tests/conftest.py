from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.db.base import Base
from app.db.models.core import (
    DictCaseStatusGdu,
    DictCaseType,
    DictGeocodeStatus,
    DictLocationRole,
    DictSignStatus,
    DictTerritoryType,
)
from app.main import app


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    with engine.connect() as conn:
        conn.execute(text("ATTACH DATABASE ':memory:' AS core"))
        conn.execute(text("ATTACH DATABASE ':memory:' AS staging"))
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    session.add_all(
        [
            DictTerritoryType(code="country", name="Country"),
            DictTerritoryType(code="region", name="Region"),
            DictTerritoryType(code="municipality", name="Municipality"),
            DictCaseStatusGdu(code="IА+", name="IА+"),
            DictCaseStatusGdu(code="IА-", name="IА-"),
            DictCaseStatusGdu(code="IБ-", name="IБ-"),
            DictSignStatus(code="+", name="plus"),
            DictSignStatus(code="-", name="minus"),
            DictSignStatus(code="?", name="unknown"),
            DictGeocodeStatus(code="FOUND", name="Found"),
            DictGeocodeStatus(code="NOT_FOUND", name="Not found"),
            DictCaseType(code="A", name="A"),
            DictCaseType(code="B", name="B"),
            DictCaseType(code="C", name="C"),
            DictCaseType(code="UNKNOWN", name="UNKNOWN"),
            DictLocationRole(code="residence", name="Residence"),
        ]
    )
    session.commit()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
