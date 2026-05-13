# Import + aggregation flow (iteration 4 MVP)

1. Client uploads synthetic CSV to `POST /api/v1/imports/cases`.
2. API validates request-level constraints (file exists, CSV extension).
3. `staging.stg_import_batch` is created.
4. Every CSV row is stored in `staging.stg_case_row.raw_payload`.
5. Per-row pipeline:
   - date normalization (`dd.mm.yyyy` / `yyyy-mm-dd`)
   - mapping legacy values `gdu/cv/mbt/found`
   - conservative dedup:
     - patient: `fio_norm + birth_year`
     - case: `patient_id + registration_date + diagnosis_raw + legacy_case_num`
   - write/update `core.patient`, `core.address`, `core.medical_case`, `core.case_location`
6. Row errors are captured in `staging.stg_case_row.error_text`.
7. Batch counters are finalized (`total_rows/success_rows/error_rows`).
8. Aggregate endpoints recompute mart slices on request:
   - map: `mart_case_map_daily`, `mart_case_map_monthly`
   - charts: `mart_chart_yearly`, `mart_chart_structure`

## Territory geometry import

Territory boundaries are imported separately from medical case CSV files.

Expected local path:

```text
data/boundaries/primorye_territories.geojson
```

Importer entry point:

```bash
python -m app.scripts.import_boundaries
```

Docker Compose entry point:

```bash
docker compose exec api python -m app.scripts.import_boundaries
```

The importer requires:
- GeoJSON root `type: "FeatureCollection"`;
- every feature must have `properties.territory_id`;
- every feature must have `properties.territory_name`;
- `properties.level` is optional;
- geometry must be `Polygon` or `MultiPolygon`;
- imported geometry is stored in SRID 4326 as `MultiPolygon`.

The importer does not download data and does not generate synthetic polygons.
