from __future__ import annotations

import sys
from pathlib import Path

from app.db.session import SessionLocal
from app.services.territory_geometry import (
    DEFAULT_BOUNDARIES_PATH,
    TerritoryGeoJsonImportError,
    import_territory_geojson,
)


def main() -> None:
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BOUNDARIES_PATH
    db = SessionLocal()
    try:
        summary = import_territory_geojson(db, source_path)
    except TerritoryGeoJsonImportError as exc:
        print(f"Ошибка импорта территориальных границ: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    finally:
        db.close()

    print(
        "Импорт территориальных границ завершён: "
        f"{summary.imported_features}/{summary.total_features} из {summary.source_path}"
    )


if __name__ == "__main__":
    main()
