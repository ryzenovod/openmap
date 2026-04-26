# Import flow (iteration 2 MVP)

1. Пользователь загружает synthetic CSV через `POST /api/v1/imports/cases`.
2. Создаётся запись в `staging.stg_import_batch`.
3. Каждая строка пишется в `staging.stg_case_row` как `raw_payload`.
4. Выполняются проверки и нормализация:
   - даты (`dd.mm.yyyy` и `yyyy-mm-dd`)
   - маппинг `gdu/cv/mbt/found` в словари
5. Выполняется conservative deduplication v0.1:
   - patient: `fio_norm + birth_year`
   - medical_case: `patient_id + registration_date + diagnosis_raw + legacy_case_num`
6. Пишутся сущности `patient/address/medical_case/case_location`.
7. Ошибки строки сохраняются в `error_text` в `staging.stg_case_row`.
