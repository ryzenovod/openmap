from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import text

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BOUNDARIES_PATH = ROOT / "data" / "boundaries" / "primorye_territories.geojson"

EMPTY_FEATURE_COLLECTION = {"type": "FeatureCollection", "features": []}


class TerritoryGeoJsonImportError(ValueError):
    pass


@dataclass(frozen=True)
class TerritoryGeometryFeature:
    territory_id: int
    territory_name: str
    level: str | None
    geometry: dict[str, Any]


@dataclass(frozen=True)
class TerritoryGeometryImportSummary:
    source_path: str
    total_features: int
    imported_features: int


def map_territories_geojson(db: Session) -> dict[str, Any]:
    bind = db.get_bind()
    if bind.dialect.name != "postgresql":
        return EMPTY_FEATURE_COLLECTION

    rows = db.execute(
        text(
            """
            SELECT
                territory_id,
                territory_name,
                level,
                ST_AsGeoJSON(geom)::json AS geometry
            FROM core.territory_geometry
            ORDER BY level NULLS LAST, territory_name, territory_id
            """
        )
    ).mappings()

    features: list[dict[str, Any]] = []
    for row in rows:
        geometry = row["geometry"]
        if isinstance(geometry, str):
            geometry = json.loads(geometry)
        features.append(
            {
                "type": "Feature",
                "properties": {
                    "territory_id": row["territory_id"],
                    "territory_name": row["territory_name"],
                    "level": row["level"],
                },
                "geometry": geometry,
            }
        )

    return {"type": "FeatureCollection", "features": features}


def load_territory_geojson_features(
    path: str | Path = DEFAULT_BOUNDARIES_PATH,
) -> list[TerritoryGeometryFeature]:
    source_path = Path(path)
    if not source_path.exists():
        raise TerritoryGeoJsonImportError(f"GeoJSON file not found: {source_path}")
    if not source_path.is_file():
        raise TerritoryGeoJsonImportError(f"GeoJSON path is not a file: {source_path}")

    try:
        payload = json.loads(source_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TerritoryGeoJsonImportError(f"Invalid GeoJSON JSON: {exc.msg}") from exc

    if not isinstance(payload, dict):
        raise TerritoryGeoJsonImportError("GeoJSON root must be an object")
    if payload.get("type") != "FeatureCollection":
        raise TerritoryGeoJsonImportError("GeoJSON root type must be FeatureCollection")

    raw_features = payload.get("features")
    if not isinstance(raw_features, list):
        raise TerritoryGeoJsonImportError("GeoJSON FeatureCollection.features must be a list")

    features: list[TerritoryGeometryFeature] = []
    seen_ids: set[int] = set()
    for idx, feature in enumerate(raw_features, start=1):
        features.append(_validate_feature(feature, idx, seen_ids))

    return features


def import_territory_geojson(
    db: Session,
    path: str | Path = DEFAULT_BOUNDARIES_PATH,
) -> TerritoryGeometryImportSummary:
    features = load_territory_geojson_features(path)
    bind = db.get_bind()
    if bind.dialect.name != "postgresql":
        raise TerritoryGeoJsonImportError(
            "PostgreSQL/PostGIS database is required for GeoJSON import"
        )

    statement = text(
        """
        INSERT INTO core.territory_geometry (territory_id, territory_name, level, geom)
        VALUES (
            :territory_id,
            :territory_name,
            :level,
            ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geometry_json), 4326))
        )
        ON CONFLICT (territory_id) DO UPDATE
        SET
            territory_name = EXCLUDED.territory_name,
            level = EXCLUDED.level,
            geom = EXCLUDED.geom
        """
    )

    for feature in features:
        db.execute(
            statement,
            {
                "territory_id": feature.territory_id,
                "territory_name": feature.territory_name,
                "level": feature.level,
                "geometry_json": json.dumps(feature.geometry, ensure_ascii=False),
            },
        )
    db.commit()

    source_path = Path(path)
    return TerritoryGeometryImportSummary(
        source_path=str(source_path),
        total_features=len(features),
        imported_features=len(features),
    )


def _validate_feature(
    feature: Any,
    idx: int,
    seen_ids: set[int],
) -> TerritoryGeometryFeature:
    if not isinstance(feature, dict):
        raise TerritoryGeoJsonImportError(f"Feature #{idx} must be an object")
    if feature.get("type") != "Feature":
        raise TerritoryGeoJsonImportError(f"Feature #{idx} type must be Feature")

    properties = feature.get("properties")
    if not isinstance(properties, dict):
        raise TerritoryGeoJsonImportError(f"Feature #{idx} properties must be an object")

    territory_id = _parse_territory_id(properties.get("territory_id"), idx)
    if territory_id in seen_ids:
        raise TerritoryGeoJsonImportError(f"Duplicate territory_id in GeoJSON: {territory_id}")
    seen_ids.add(territory_id)

    territory_name = properties.get("territory_name")
    if not isinstance(territory_name, str) or not territory_name.strip():
        raise TerritoryGeoJsonImportError(f"Feature #{idx} properties.territory_name is required")

    level = properties.get("level")
    if level is not None and not isinstance(level, str):
        raise TerritoryGeoJsonImportError(f"Feature #{idx} properties.level must be a string")

    geometry = feature.get("geometry")
    if not isinstance(geometry, dict):
        raise TerritoryGeoJsonImportError(f"Feature #{idx} geometry is required")
    geometry_type = geometry.get("type")
    if geometry_type not in {"Polygon", "MultiPolygon"}:
        raise TerritoryGeoJsonImportError(
            f"Feature #{idx} geometry.type must be Polygon or MultiPolygon"
        )
    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or not coordinates:
        raise TerritoryGeoJsonImportError(
            f"Feature #{idx} geometry.coordinates must be a non-empty list"
        )

    return TerritoryGeometryFeature(
        territory_id=territory_id,
        territory_name=territory_name.strip(),
        level=level.strip() if isinstance(level, str) and level.strip() else None,
        geometry=geometry,
    )


def _parse_territory_id(value: Any, idx: int) -> int:
    if value is None:
        raise TerritoryGeoJsonImportError(f"Feature #{idx} properties.territory_id is required")
    try:
        territory_id = int(value)
    except (TypeError, ValueError) as exc:
        raise TerritoryGeoJsonImportError(
            f"Feature #{idx} properties.territory_id must be an integer"
        ) from exc
    if territory_id <= 0:
        raise TerritoryGeoJsonImportError(
            f"Feature #{idx} properties.territory_id must be positive"
        )
    return territory_id
