from __future__ import annotations

from collections import defaultdict
from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models.core import MedicalCase, PopulationStat, Territory
from app.db.models.mart import MartCaseMapDaily, MartCaseMapMonthly


def _territory_lookup(db: Session) -> list[Territory]:
    return db.execute(select(Territory).order_by(Territory.id)).scalars().all()


def _resolve_territory(case: MedicalCase, territories: list[Territory]) -> int | None:
    diagnosis = (case.diagnosis_raw or "").lower()
    work = (case.work_raw or "").lower()
    haystack = f"{diagnosis} {work}"
    for territory in territories:
        name = territory.name.lower().replace("(город. округ)", "").strip()
        if name and name in haystack:
            return territory.id
    return 2 if territories else None


def _population_by_territory_year(db: Session) -> dict[tuple[int, int], int]:
    rows = db.execute(select(PopulationStat)).scalars().all()
    return {(x.territory_id, x.year): x.population for x in rows}


def _territory_children_count(territories: list[Territory]) -> dict[int, int]:
    children = defaultdict(int)
    for t in territories:
        if t.parent_id:
            children[t.parent_id] += 1
    return dict(children)


def aggregate_map(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
    level: str | None = None,
) -> list[dict]:
    territories = _territory_lookup(db)
    pop_map = _population_by_territory_year(db)
    children_count = _territory_children_count(territories)

    query = select(MedicalCase).order_by(MedicalCase.registration_date)
    if date_from:
        query = query.where(MedicalCase.registration_date >= date_from)
    if date_to:
        query = query.where(MedicalCase.registration_date <= date_to)

    cases = db.execute(query).scalars().all()

    daily = defaultdict(lambda: {"case_count": 0, "mbt_positive_count": 0, "cv_positive_count": 0})
    monthly = defaultdict(
        lambda: {"case_count": 0, "mbt_positive_count": 0, "cv_positive_count": 0}
    )

    territory_by_id = {t.id: t for t in territories}

    for case in cases:
        territory_id = _resolve_territory(case, territories)
        if territory_id is None:
            continue
        territory = territory_by_id.get(territory_id)
        if level and territory and territory.territory_type_code != level:
            continue

        day_key = (case.registration_date, territory_id)
        month_key = (case.registration_date.year, case.registration_date.month, territory_id)

        daily[day_key]["case_count"] += 1
        monthly[month_key]["case_count"] += 1
        if case.mbt_code == "+":
            daily[day_key]["mbt_positive_count"] += 1
            monthly[month_key]["mbt_positive_count"] += 1
        if case.cv_code == "+":
            daily[day_key]["cv_positive_count"] += 1
            monthly[month_key]["cv_positive_count"] += 1

    db.execute(delete(MartCaseMapDaily))
    db.execute(delete(MartCaseMapMonthly))

    response = []
    for (agg_date, territory_id), payload in daily.items():
        pop = pop_map.get((territory_id, agg_date.year))
        incidence = (payload["case_count"] * 100000.0 / pop) if pop else None
        db.add(
            MartCaseMapDaily(
                aggregation_date=agg_date,
                territory_id=territory_id,
                case_count=payload["case_count"],
                mbt_positive_count=payload["mbt_positive_count"],
                cv_positive_count=payload["cv_positive_count"],
                incidence_per_100k=incidence,
            )
        )
        t = territory_by_id.get(territory_id)
        response.append(
            {
                "aggregation_date": agg_date.isoformat(),
                "territory_id": territory_id,
                "territory_name": t.name if t else None,
                "territory_type_code": t.territory_type_code if t else None,
                "case_count": payload["case_count"],
                "mbt_positive_count": payload["mbt_positive_count"],
                "cv_positive_count": payload["cv_positive_count"],
                "children_count": children_count.get(territory_id, 0),
                "incidence_per_100k": incidence,
            }
        )

    for (year, month, territory_id), payload in monthly.items():
        pop = pop_map.get((territory_id, year))
        incidence = (payload["case_count"] * 100000.0 / pop) if pop else None
        db.add(
            MartCaseMapMonthly(
                year=year,
                month=month,
                territory_id=territory_id,
                case_count=payload["case_count"],
                mbt_positive_count=payload["mbt_positive_count"],
                cv_positive_count=payload["cv_positive_count"],
                incidence_per_100k=incidence,
            )
        )

    db.commit()
    return sorted(response, key=lambda x: (x["aggregation_date"], x["territory_id"]))
