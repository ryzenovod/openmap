from __future__ import annotations

from collections import defaultdict
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.core import MedicalCase, Patient, Territory
from app.db.models.mart import MartChartStructure, MartChartYearly
from app.services.aggregates.common import age_group


def _resolve_territory_id(case: MedicalCase, territories: list[Territory]) -> int | None:
    haystack = f"{(case.diagnosis_raw or '').lower()} {(case.work_raw or '').lower()}"
    for territory in territories:
        token = territory.name.lower().replace("(город. округ)", "").strip()
        if token and token in haystack:
            return territory.id
    return 2 if territories else None


def yearly_dynamics(db: Session, date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    query = select(MedicalCase)
    if date_from:
        query = query.where(MedicalCase.registration_date >= date_from)
    if date_to:
        query = query.where(MedicalCase.registration_date <= date_to)

    counters = defaultdict(int)
    for case in db.execute(query).scalars().all():
        counters[case.registration_date.year] += 1

    db.execute(delete(MartChartYearly))
    for year, case_count in counters.items():
        db.add(MartChartYearly(year=year, territory_id=None, case_count=case_count))
    db.commit()

    return [{"year": year, "case_count": count} for year, count in sorted(counters.items())]


def structure_breakdown(
    db: Session,
    dimension: str,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[dict]:
    query = select(MedicalCase, Patient).join(Patient, Patient.id == MedicalCase.patient_id)
    if date_from:
        query = query.where(MedicalCase.registration_date >= date_from)
    if date_to:
        query = query.where(MedicalCase.registration_date <= date_to)

    territories = db.execute(select(Territory)).scalars().all()
    counters = defaultdict(int)

    for case, patient in db.execute(query).all():
        year = case.registration_date.year
        territory_id = _resolve_territory_id(case, territories)

        if dimension == "mkb":
            bucket = (case.diagnosis_raw or "").split(" ")[0] or "unknown"
        elif dimension == "sex":
            bucket = "unknown"
        elif dimension == "age_group":
            bucket = age_group(patient.birth_year, case.registration_date.year)
        elif dimension == "territory":
            bucket = str(territory_id) if territory_id is not None else "unknown"
        else:
            raise ValueError(f"unsupported dimension: {dimension}")

        counters[(year, bucket, territory_id)] += 1

    db.execute(delete(MartChartStructure).where(MartChartStructure.dimension == dimension))
    for (year, bucket, territory_id), case_count in counters.items():
        db.add(
            MartChartStructure(
                year=year,
                dimension=dimension,
                bucket=bucket,
                territory_id=territory_id,
                case_count=case_count,
            )
        )
    db.commit()

    output = []
    for (year, bucket, territory_id), case_count in sorted(counters.items()):
        output.append(
            {
                "year": year,
                "dimension": dimension,
                "bucket": bucket,
                "territory_id": territory_id,
                "case_count": case_count,
            }
        )
    return output


def charts_structure(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> dict:
    return {
        "by_mkb": structure_breakdown(db, "mkb", date_from=date_from, date_to=date_to),
        "by_sex": structure_breakdown(db, "sex", date_from=date_from, date_to=date_to),
        "by_age_group": structure_breakdown(db, "age_group", date_from=date_from, date_to=date_to),
        "territorial_comparison": structure_breakdown(db, "territory", date_from=date_from, date_to=date_to),
    }
