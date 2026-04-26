from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.core import (
    Address,
    CaseLocation,
    DictCaseStatusGdu,
    DictCaseType,
    DictGeocodeStatus,
    DictLocationRole,
    DictSignStatus,
    MedicalCase,
    Patient,
    PatientAddress,
)
from app.db.models.staging import StgCaseRow, StgImportBatch


@dataclass
class ImportSummary:
    batch_id: int
    total_rows: int
    success_rows: int
    error_rows: int


def normalize_fio(value: str) -> str:
    return " ".join(value.strip().upper().split())


def normalize_date(raw: str) -> date:
    raw = raw.strip()
    if not raw:
        raise ValueError("dreg is empty")
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unsupported date format: {raw}")


def map_sign_code(raw: str) -> str | None:
    value = raw.strip().replace('"', "")
    if value in {"+", "-", "?"}:
        return value
    return None


def map_geocode_status(raw: str) -> str | None:
    value = raw.strip().replace('"', "")
    if value == "1":
        return "FOUND"
    if value in {"0", "?", ""}:
        return "NOT_FOUND"
    return None


def map_case_type(raw: str) -> str:
    value = raw.strip().upper().replace('"', "")
    if value in {"A", "B", "C"}:
        return value
    return "UNKNOWN"


def _get_or_create_patient(db: Session, fio_raw: str, birth_year: int | None) -> Patient:
    fio_norm = normalize_fio(fio_raw)
    patient = db.execute(
        select(Patient).where(Patient.fio_norm == fio_norm, Patient.birth_year == birth_year)
    ).scalar_one_or_none()
    if patient:
        return patient
    patient = Patient(fio_raw=fio_raw.strip(), fio_norm=fio_norm, birth_year=birth_year)
    db.add(patient)
    db.flush()
    return patient


def _get_or_create_address(
    db: Session,
    raw_text: str,
    normalized_text: str | None,
    lat: float | None,
    lon: float | None,
    geocode_status_code: str | None,
) -> Address:
    address = db.execute(
        select(Address).where(
            Address.raw_text == raw_text,
            Address.normalized_text == normalized_text,
            Address.lat == lat,
            Address.lon == lon,
        )
    ).scalar_one_or_none()
    if address:
        return address
    address = Address(
        raw_text=raw_text,
        normalized_text=normalized_text,
        lat=lat,
        lon=lon,
        geocode_status_code=geocode_status_code,
    )
    db.add(address)
    db.flush()
    return address


def _get_or_create_case(
    db: Session,
    patient_id: int,
    registration_date: date,
    diagnosis_raw: str,
    legacy_case_num: str | None,
    work_raw: str | None,
    gdu_code: str | None,
    cv_code: str | None,
    mbt_code: str | None,
    case_type_code: str | None,
) -> MedicalCase:
    case = db.execute(
        select(MedicalCase).where(
            MedicalCase.patient_id == patient_id,
            MedicalCase.registration_date == registration_date,
            MedicalCase.diagnosis_raw == diagnosis_raw,
            MedicalCase.legacy_case_num == legacy_case_num,
        )
    ).scalar_one_or_none()
    if case:
        return case
    case = MedicalCase(
        patient_id=patient_id,
        registration_date=registration_date,
        diagnosis_raw=diagnosis_raw,
        legacy_case_num=legacy_case_num,
        work_raw=work_raw,
        gdu_code=gdu_code,
        cv_code=cv_code,
        mbt_code=mbt_code,
        case_type_code=case_type_code,
    )
    db.add(case)
    db.flush()
    return case


def _ensure_patient_address(db: Session, patient_id: int, address_id: int) -> None:
    db.flush()
    existing = db.execute(
        select(PatientAddress).where(
            PatientAddress.patient_id == patient_id, PatientAddress.address_id == address_id
        )
    ).scalar_one_or_none()
    if not existing:
        db.add(PatientAddress(patient_id=patient_id, address_id=address_id))


def _ensure_case_location(db: Session, case_id: int, address_id: int, role_code: str = "residence") -> None:
    db.flush()
    existing = db.execute(
        select(CaseLocation).where(
            CaseLocation.medical_case_id == case_id, CaseLocation.address_id == address_id
        )
    ).scalar_one_or_none()
    if not existing:
        db.add(CaseLocation(medical_case_id=case_id, address_id=address_id, location_role_code=role_code))


def import_cases_csv(db: Session, filename: str, payload_bytes: bytes) -> ImportSummary:
    batch = StgImportBatch(source_filename=filename)
    db.add(batch)
    db.flush()

    decoded = payload_bytes.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))

    total = success = errors = 0
    for row_num, row in enumerate(reader, start=1):
        total += 1
        error_text = None
        normalized_payload = None
        try:
            registration_date = normalize_date(row.get("dreg", ""))
            fio_raw = row.get("fio", "").strip()
            if not fio_raw:
                raise ValueError("fio is empty")

            birth_year = int(str(row.get("godr", "")).strip()) if str(row.get("godr", "")).strip() else None
            gdu_code = str(row.get("gdu", "")).strip().replace('"', "") or None
            cv_code = map_sign_code(str(row.get("cv", "")))
            mbt_code = map_sign_code(str(row.get("mbt", "")))
            geocode_status_code = map_geocode_status(str(row.get("found", "")))
            case_type_code = map_case_type(str(row.get("razdel", "")))

            if gdu_code and not db.get(DictCaseStatusGdu, gdu_code):
                raise ValueError(f"unknown gdu code: {gdu_code}")
            if cv_code and not db.get(DictSignStatus, cv_code):
                raise ValueError(f"unknown cv code: {cv_code}")
            if mbt_code and not db.get(DictSignStatus, mbt_code):
                raise ValueError(f"unknown mbt code: {mbt_code}")
            if geocode_status_code and not db.get(DictGeocodeStatus, geocode_status_code):
                raise ValueError(f"unknown geocode status: {geocode_status_code}")
            if case_type_code and not db.get(DictCaseType, case_type_code):
                raise ValueError(f"unknown case type: {case_type_code}")
            if not db.get(DictLocationRole, "residence"):
                raise ValueError("missing location role residence")

            lat_raw = str(row.get("shirota", "")).strip()
            lon_raw = str(row.get("dolgota", "")).strip()
            lat = float(lat_raw) if lat_raw else None
            lon = float(lon_raw) if lon_raw else None

            patient = _get_or_create_patient(db, fio_raw=fio_raw, birth_year=birth_year)
            address = _get_or_create_address(
                db,
                raw_text=str(row.get("addr", "")).strip(),
                normalized_text=str(row.get("address", "")).strip() or None,
                lat=lat,
                lon=lon,
                geocode_status_code=geocode_status_code,
            )
            med_case = _get_or_create_case(
                db,
                patient_id=patient.id,
                registration_date=registration_date,
                diagnosis_raw=str(row.get("diagnoz", "")).strip(),
                legacy_case_num=str(row.get("nrec", "")).strip() or None,
                work_raw=str(row.get("work", "")).strip() or None,
                gdu_code=gdu_code,
                cv_code=cv_code,
                mbt_code=mbt_code,
                case_type_code=case_type_code,
            )
            _ensure_patient_address(db, patient.id, address.id)
            _ensure_case_location(db, med_case.id, address.id)

            normalized_payload = json.dumps(
                {
                    "patient_id": patient.id,
                    "address_id": address.id,
                    "medical_case_id": med_case.id,
                    "registration_date": registration_date.isoformat(),
                },
                ensure_ascii=False,
            )
            success += 1
        except Exception as exc:  # noqa: BLE001
            error_text = str(exc)
            errors += 1

        db.add(
            StgCaseRow(
                batch_id=batch.id,
                row_num=row_num,
                raw_payload=json.dumps(row, ensure_ascii=False),
                normalized_payload=normalized_payload,
                error_text=error_text,
            )
        )

    batch.total_rows = total
    batch.success_rows = success
    batch.error_rows = errors

    db.commit()
    return ImportSummary(batch_id=batch.id, total_rows=total, success_rows=success, error_rows=errors)
