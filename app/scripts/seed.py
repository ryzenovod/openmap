from __future__ import annotations

import csv
from pathlib import Path

from sqlalchemy import delete

from app.db.models.core import (
    DictCaseStatusGdu,
    DictCaseType,
    DictGeocodeStatus,
    DictLocationRole,
    DictMkb10,
    DictSignStatus,
    DictTerritoryType,
    PopulationStat,
    Territory,
)
from app.db.session import SessionLocal

ROOT = Path(__file__).resolve().parents[2]
DICT_DIR = ROOT / "legacy_assets" / "dictionaries"


def seed_reference_dicts() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(DictTerritoryType))
        db.execute(delete(DictCaseStatusGdu))
        db.execute(delete(DictSignStatus))
        db.execute(delete(DictGeocodeStatus))
        db.execute(delete(DictCaseType))
        db.execute(delete(DictLocationRole))

        db.add_all(
            [
                DictTerritoryType(code="country", name="Страна"),
                DictTerritoryType(code="region", name="Регион"),
                DictTerritoryType(code="municipality", name="Муниципалитет"),
                DictCaseStatusGdu(code="IА+", name="IА+"),
                DictCaseStatusGdu(code="IА-", name="IА-"),
                DictCaseStatusGdu(code="IБ-", name="IБ-"),
                DictSignStatus(code="+", name="Положительно"),
                DictSignStatus(code="-", name="Отрицательно"),
                DictSignStatus(code="?", name="Неизвестно"),
                DictGeocodeStatus(code="FOUND", name="Найдено"),
                DictGeocodeStatus(code="NOT_FOUND", name="Не найдено"),
                DictCaseType(code="A", name="Раздел A"),
                DictCaseType(code="B", name="Раздел B"),
                DictCaseType(code="C", name="Раздел C"),
                DictCaseType(code="UNKNOWN", name="Неизвестно"),
                DictLocationRole(code="residence", name="Место проживания"),
            ]
        )
        db.commit()
    finally:
        db.close()


def seed_mkb10() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(DictMkb10))
        records: list[tuple[int, int | None, str, str]] = []
        with (DICT_DIR / "mkb10Codes.csv").open("r", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter=";")
            for row in reader:
                if not row:
                    continue
                records.append(
                    (
                        int(row[0]),
                        int(row[1]) if row[1] else None,
                        row[2].strip(),
                        row[3].strip(),
                    )
                )

        items = {
            row_id: DictMkb10(id=row_id, parent_id=None, code=code, name=name)
            for row_id, _, code, name in records
        }
        missing_parent_ids = sorted(
            {parent_id for _, parent_id, _, _ in records if parent_id and parent_id not in items}
        )
        if missing_parent_ids:
            raise ValueError(f"mkb10 parent ids are missing: {missing_parent_ids}")

        db.add_all(items.values())
        db.flush()
        for row_id, parent_id, _, _ in records:
            items[row_id].parent_id = parent_id
        db.commit()
    finally:
        db.close()


def seed_territories() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(Territory))
        with (DICT_DIR / "territories.csv").open("r", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter=";")
            for row in reader:
                if not row:
                    continue
                territory_id = int(row[0])
                parent_id = int(row[2]) if len(row) > 2 and row[2] else None
                ttype = (
                    "country"
                    if territory_id == 1
                    else ("region" if territory_id == 2 else "municipality")
                )
                db.add(
                    Territory(
                        id=territory_id,
                        parent_id=parent_id,
                        name=row[1].strip(),
                        territory_type_code=ttype,
                    )
                )
        db.commit()
    finally:
        db.close()


def seed_populations() -> None:
    db = SessionLocal()
    try:
        db.execute(delete(PopulationStat))
        with (DICT_DIR / "populations.csv").open("r", encoding="utf-8") as handle:
            reader = csv.reader(handle, delimiter=";")
            for row in reader:
                if not row:
                    continue
                db.add(
                    PopulationStat(
                        territory_id=int(row[0]),
                        year=int(row[1]),
                        population=int(row[2]),
                    )
                )
        db.commit()
    finally:
        db.close()


def run_all() -> None:
    seed_reference_dicts()
    seed_mkb10()
    seed_territories()
    seed_populations()


if __name__ == "__main__":
    run_all()
