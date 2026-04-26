# Import flow

1. Пользователь загружает CSV
2. Создаётся запись в stg_import_batch
3. Каждая строка пишется в stg_case_row
4. Выполняется валидация и нормализация
5. Нормализованные данные загружаются в:
   - patient
   - address
   - medical_case
   - case_location
6. Ошибки сохраняются в staging
7. Дальше данные агрегируются в mart