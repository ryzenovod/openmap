# AGENTS.md

## Цель проекта
Собрать новый backend внутренней медицинской геоаналитической системы с нуля.
Это НЕ рефакторинг legacy AngularJS-приложения.

## Что нужно сделать в MVP
Сначала реализовать только:
1. backend skeleton
2. PostgreSQL + PostGIS schema
3. Alembic migrations
4. seed scripts для словарей
5. importer MVP для CSV
6. API для cases / territories / aggregates
7. tests
8. docs

## Стек
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- PostGIS
- pytest
- Docker / docker-compose

## Архитектура данных
Использовать 3 слоя:
- staging
- core
- mart

## Что НЕ делать сейчас
- frontend
- AngularJS migration
- forecasting
- AI
- production auth
- external geocoding
- публичную выдачу точных адресов

## Правила по данным
- Не коммитить реальные медицинские данные
- Не коммитить секреты, .env, пароли, внутренние хосты
- В тестах использовать только синтетические CSV
- Legacy использовать только как reference:
  - dictionaries
  - field semantics
  - import logic reference
  - geo reference

## Минимальные сущности
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

## Минимальные endpoints
- POST /api/v1/imports/cases
- GET /api/v1/imports
- GET /api/v1/territories
- GET /api/v1/territories/tree
- GET /api/v1/dictionaries/mkb10
- GET /api/v1/cases
- GET /api/v1/cases/{id}
- GET /api/v1/map/aggregate
- GET /api/v1/charts/yearly
- GET /api/v1/charts/structure
- GET /health

## Порядок работы
Всегда двигаться так:
1. skeleton
2. migrations
3. seed
4. importer
5. API
6. tests
7. docs

## Критерий готовности
Задача не считается завершённой, пока:
- docker-compose не стартует
- миграции не применяются
- seed не работает
- synthetic CSV import не работает
- /health не отвечает
- README не обновлён