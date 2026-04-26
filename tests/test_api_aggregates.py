from __future__ import annotations

from datetime import date

from app.db.models.core import MedicalCase, Patient, PopulationStat, Territory


def _seed(db_session):
    db_session.add_all(
        [
            Territory(id=1, name="Российская Федерация", parent_id=None, territory_type_code="country"),
            Territory(id=2, name="Приморский край", parent_id=1, territory_type_code="region"),
            Territory(id=10, name="Находка", parent_id=2, territory_type_code="municipality"),
        ]
    )
    db_session.add(PopulationStat(territory_id=2, year=2025, population=1933308))
    patient = Patient(fio_raw="ТЕСТ ТЕСТ", fio_norm="ТЕСТ ТЕСТ", birth_year=1978)
    db_session.add(patient)
    db_session.flush()
    db_session.add(
        MedicalCase(
            patient_id=patient.id,
            legacy_case_num="2001",
            registration_date=date(2025, 3, 15),
            diagnosis_raw="A15.7 Находка",
            work_raw="Находка",
            gdu_code="IА-",
            cv_code="+",
            mbt_code="+",
            case_type_code="A",
        )
    )
    db_session.commit()


def test_map_aggregate_api(client, db_session):
    _seed(db_session)
    response = client.get("/api/v1/map/aggregate?date_from=2025-01-01&date_to=2025-12-31")
    assert response.status_code == 200
    assert response.json()
    assert "incidence_per_100k" in response.json()[0]


def test_charts_yearly_api(client, db_session):
    _seed(db_session)
    response = client.get("/api/v1/charts/yearly")
    assert response.status_code == 200
    assert response.json()[0]["year"] == 2025


def test_charts_structure_api(client, db_session):
    _seed(db_session)
    response = client.get("/api/v1/charts/structure")
    assert response.status_code == 200
    payload = response.json()
    assert "by_mkb" in payload
    assert "by_sex" in payload
    assert "by_age_group" in payload
    assert "territorial_comparison" in payload
