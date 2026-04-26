# Field mapping

## Legacy CSV fields
- nrec
- addr
- razdel
- fio
- godr
- dreg
- gdu
- cv
- mbt
- work
- diagnoz
- found
- address
- shirota
- dolgota

## Proposed mapping v0.1

### patient
- fio -> fio_raw / fio_norm
- godr -> birth_year

### medical_case
- nrec -> legacy_case_num
- dreg -> registration_date
- gdu -> gdu_code
- cv -> cv_code
- mbt -> mbt_code
- diagnoz -> diagnosis_raw
- work -> work_raw

### address
- addr -> raw_text
- address -> normalized_text
- shirota -> lat
- dolgota -> lon
- found -> geocode_status_code