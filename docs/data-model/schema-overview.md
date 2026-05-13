# Schema overview (iteration 3)

## Data layers

### staging
- stg_import_batch
- stg_case_row
- stg_file_mapping

### core
- dict_mkb10
- dict_territory_type
- dict_case_status_gdu
- dict_sign_status
- dict_geocode_status
- dict_case_type
- dict_location_role
- territory
- territory_geometry
- population_stat
- patient
- address
- patient_address
- medical_case
- case_event
- case_location

### mart
- mart_case_map_daily
- mart_case_map_monthly
- mart_chart_yearly
- mart_chart_structure
