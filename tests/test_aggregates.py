from __future__ import annotations

from datetime import date

from app.db.models.core import MedicalCase, Patient, PopulationStat, Territory
from app.services.aggregates.charts import charts_structure, yearly_dynamics
from app.services.aggregates.map import aggregate_map


def _seed_base(db_session):
    db_session.add_all(
        [
            Territory(id=1, name="Российская Федерация", parent_id=None, territory_type_code="country"),
            Territory(id=2, name="Приморский край", parent_id=1, territory_type_code="region"),
            Territory(id=10, name="Находка", parent_id=2, territory_type_code="municipality"),
        ]
    )
    db_session.add_all(
        [
            PopulationStat(territory_id=2, year=2025, population=1933308),
            PopulationStat(territory_id=10, year=2025, population=156649),
        ]
    )
    p1 = Patient(fio_raw="Иванов И", fio_norm="ИВАНОВ И", birth_year=1985)
    p2 = Patient(fio_raw="Петров П", fio_norm="ПЕТРОВ П", birth_year=2001)
    db_session.add_all([p1, p2])
    db_session.flush()

    db_session.add_all(
        [
            MedicalCase(
                patient_id=p1.id,
                legacy_case_num="1001",
                registration_date=date(2025, 4, 23),
                diagnosis_raw="A15.0 Владивосток",
                work_raw="работает Находка",
                gdu_code="IА+",
                cv_code="+",
                mbt_code="-",
                case_type_code="A",
            ),
            MedicalCase(
                patient_id=p2.id,
                legacy_case_num="1002",
                registration_date=date(2025, 5, 14),
                diagnosis_raw="A16.2 Уссурийск",
                work_raw="не работает Находка",
                gdu_code="IБ-",
                cv_code="-",
                mbt_code="+",
                case_type_code="B",
            ),
        ]
    )
    db_session.commit()


def test_map_aggregate_service(db_session):
    _seed_base(db_session)
    rows = aggregate_map(db_session, date_from=date(2025, 1, 1), date_to=date(2025, 12, 31))
    assert len(rows) == 2
    assert rows[0]["territory_id"] in {2, 10}
    assert rows[0]["case_count"] == 1


def test_charts_services(db_session):
    _seed_base(db_session)
    yearly = yearly_dynamics(db_session)
    assert yearly == [{"year": 2025, "case_count": 2}]

    structure = charts_structure(db_session)
    assert structure["by_mkb"]
    assert structure["by_age_group"]
    assert structure["by_sex"][0]["bucket"] == "unknown"
    assert structure["territorial_comparison"]
