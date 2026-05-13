from __future__ import annotations

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.core import MedicalCase, Patient
from app.db.models.staging import StgCaseRow
from app.services.importer import (
    import_cases_csv,
    map_geocode_status,
    map_sign_code,
    normalize_date,
)
from app.services.territory_geometry import (
    TerritoryGeoJsonImportError,
    load_territory_geojson_features,
)


def test_date_normalization() -> None:
    assert normalize_date("23.04.2025").isoformat() == "2025-04-23"
    assert normalize_date("2025-05-14").isoformat() == "2025-05-14"


def test_dictionary_mapping() -> None:
    assert map_sign_code("+") == "+"
    assert map_sign_code(" - ") == "-"
    assert map_sign_code("unknown") is None
    assert map_geocode_status("1") == "FOUND"
    assert map_geocode_status("?") == "NOT_FOUND"


def test_importer_and_dedup(db_session: Session) -> None:
    payload = (
        "nrec,addr,razdel,fio,godr,dreg,gdu,cv,mbt,work,diagnoz,found,address,shirota,dolgota\n"
        "1001,Addr 1,A,IVANOV IVAN,1985,23.04.2025,IА+,+,-,work,A15.0 TB,1,Addr 1,,\n"
        "1001,Addr 1,A,IVANOV IVAN,1985,2025-04-23,IА+,+,-,work,A15.0 TB,1,Addr 1,,\n"
    ).encode()

    summary = import_cases_csv(db_session, filename="cases.csv", payload_bytes=payload)

    assert summary.total_rows == 2
    assert summary.success_rows == 2

    patients = db_session.execute(select(Patient)).scalars().all()
    cases = db_session.execute(select(MedicalCase)).scalars().all()
    staged_rows = db_session.execute(select(StgCaseRow)).scalars().all()

    assert len(patients) == 1
    assert len(cases) == 1
    assert len(staged_rows) == 2
    assert all(row.error_text is None for row in staged_rows)


def test_importer_row_error(db_session: Session) -> None:
    payload = (
        "nrec,addr,razdel,fio,godr,dreg,gdu,cv,mbt,work,diagnoz,found,address,shirota,dolgota\n"
        "1002,Addr 2,A,PETROVA,1992,bad-date,IБ-,-,?,work,A16.2 TB,?,Addr 2,,\n"
    ).encode()

    summary = import_cases_csv(db_session, filename="cases_bad.csv", payload_bytes=payload)
    rows = db_session.execute(select(StgCaseRow)).scalars().all()

    assert summary.error_rows == 1
    assert rows[0].error_text is not None


def test_territory_geojson_empty_feature_collection(tmp_path) -> None:
    payload = '{"type": "FeatureCollection", "features": []}'
    path = tmp_path / "territories.geojson"
    path.write_text(payload, encoding="utf-8")

    features = load_territory_geojson_features(path)

    assert features == []


def test_territory_geojson_missing_file(tmp_path) -> None:
    with pytest.raises(TerritoryGeoJsonImportError, match="not found"):
        load_territory_geojson_features(tmp_path / "missing.geojson")


def test_territory_geojson_requires_feature_collection(tmp_path) -> None:
    path = tmp_path / "invalid.geojson"
    path.write_text('{"type": "Feature", "properties": {}, "geometry": null}', encoding="utf-8")

    with pytest.raises(TerritoryGeoJsonImportError, match="FeatureCollection"):
        load_territory_geojson_features(path)
