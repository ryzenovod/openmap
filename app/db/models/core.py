from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DictMkb10(Base):
    __tablename__ = "dict_mkb10"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("core.dict_mkb10.id"), nullable=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)


class DictTerritoryType(Base):
    __tablename__ = "dict_territory_type"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class DictCaseStatusGdu(Base):
    __tablename__ = "dict_case_status_gdu"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class DictSignStatus(Base):
    __tablename__ = "dict_sign_status"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class DictGeocodeStatus(Base):
    __tablename__ = "dict_geocode_status"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(16), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class DictCaseType(Base):
    __tablename__ = "dict_case_type"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class DictLocationRole(Base):
    __tablename__ = "dict_location_role"
    __table_args__ = {"schema": "core"}

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)


class Territory(Base):
    __tablename__ = "territory"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("core.territory.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    territory_type_code: Mapped[str] = mapped_column(
        ForeignKey("core.dict_territory_type.code"), nullable=False, default="municipality"
    )


class PopulationStat(Base):
    __tablename__ = "population_stat"
    __table_args__ = (
        UniqueConstraint("territory_id", "year", name="uq_population_stat_territory_year"),
        {"schema": "core"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    territory_id: Mapped[int] = mapped_column(ForeignKey("core.territory.id"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=False)


class Patient(Base):
    __tablename__ = "patient"
    __table_args__ = (
        UniqueConstraint("fio_norm", "birth_year", name="uq_patient_fio_norm_birth_year"),
        {"schema": "core"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fio_raw: Mapped[str] = mapped_column(String(255), nullable=False)
    fio_norm: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Address(Base):
    __tablename__ = "address"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    geocode_status_code: Mapped[str | None] = mapped_column(
        ForeignKey("core.dict_geocode_status.code"), nullable=True
    )


class PatientAddress(Base):
    __tablename__ = "patient_address"
    __table_args__ = (
        UniqueConstraint("patient_id", "address_id", name="uq_patient_address_pair"),
        {"schema": "core"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("core.patient.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("core.address.id"), nullable=False)


class MedicalCase(Base):
    __tablename__ = "medical_case"
    __table_args__ = (
        UniqueConstraint(
            "patient_id",
            "registration_date",
            "diagnosis_raw",
            "legacy_case_num",
            name="uq_medical_case_dedup_key",
        ),
        {"schema": "core"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("core.patient.id"), nullable=False)
    legacy_case_num: Mapped[str | None] = mapped_column(String(64), nullable=True)
    registration_date: Mapped[date] = mapped_column(Date, nullable=False)
    diagnosis_raw: Mapped[str] = mapped_column(Text, nullable=False)
    work_raw: Mapped[str | None] = mapped_column(Text, nullable=True)

    gdu_code: Mapped[str | None] = mapped_column(
        ForeignKey("core.dict_case_status_gdu.code"), nullable=True
    )
    cv_code: Mapped[str | None] = mapped_column(
        ForeignKey("core.dict_sign_status.code"), nullable=True
    )
    mbt_code: Mapped[str | None] = mapped_column(
        ForeignKey("core.dict_sign_status.code"), nullable=True
    )
    case_type_code: Mapped[str | None] = mapped_column(
        ForeignKey("core.dict_case_type.code"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class CaseEvent(Base):
    __tablename__ = "case_event"
    __table_args__ = {"schema": "core"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medical_case_id: Mapped[int] = mapped_column(ForeignKey("core.medical_case.id"), nullable=False)
    event_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, default="created")
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)


class CaseLocation(Base):
    __tablename__ = "case_location"
    __table_args__ = (
        UniqueConstraint("medical_case_id", "address_id", name="uq_case_location_pair"),
        {"schema": "core"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    medical_case_id: Mapped[int] = mapped_column(ForeignKey("core.medical_case.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("core.address.id"), nullable=False)
    location_role_code: Mapped[str] = mapped_column(
        ForeignKey("core.dict_location_role.code"), nullable=False, default="residence"
    )
