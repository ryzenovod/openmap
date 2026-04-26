# Schema overview

## Data layers

### staging
Слой сырого импорта:
- stg_import_batch
- stg_case_row
- stg_file_mapping

### core
Нормализованные сущности:
- dict_mkb10
- dict_territory_type
- dict_case_status_gdu
- dict_sign_status
- dict_geocode_status
- dict_case_type
- dict_location_role
- territory
- population_stat
- patient
- address
- patient_address
- medical_case
- case_event
- case_location

### mart
Агрегаты:
- mart_case_map_daily
- mart_case_map_monthly
- mart_chart_yearly
- mart_chart_structure