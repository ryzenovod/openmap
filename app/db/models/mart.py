from __future__ import annotations

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MartCaseMapDaily(Base):
    __tablename__ = "mart_case_map_daily"
    __table_args__ = (
        UniqueConstraint("aggregation_date", "territory_id", name="uq_mart_case_map_daily_key"),
        {"schema": "mart"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aggregation_date: Mapped[date] = mapped_column(Date, nullable=False)
    territory_id: Mapped[int] = mapped_column(ForeignKey("core.territory.id"), nullable=False)
    case_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mbt_positive_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cv_positive_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incidence_per_100k: Mapped[float | None] = mapped_column(Float, nullable=True)


class MartCaseMapMonthly(Base):
    __tablename__ = "mart_case_map_monthly"
    __table_args__ = (
        UniqueConstraint("year", "month", "territory_id", name="uq_mart_case_map_monthly_key"),
        {"schema": "mart"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    territory_id: Mapped[int] = mapped_column(ForeignKey("core.territory.id"), nullable=False)
    case_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mbt_positive_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cv_positive_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    incidence_per_100k: Mapped[float | None] = mapped_column(Float, nullable=True)


class MartChartYearly(Base):
    __tablename__ = "mart_chart_yearly"
    __table_args__ = (
        UniqueConstraint("year", "territory_id", name="uq_mart_chart_yearly_key"),
        {"schema": "mart"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    territory_id: Mapped[int | None] = mapped_column(ForeignKey("core.territory.id"), nullable=True)
    case_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class MartChartStructure(Base):
    __tablename__ = "mart_chart_structure"
    __table_args__ = (
        UniqueConstraint("year", "dimension", "bucket", "territory_id", name="uq_mart_chart_structure_key"),
        {"schema": "mart"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    dimension: Mapped[str] = mapped_column(String(32), nullable=False)
    bucket: Mapped[str] = mapped_column(String(64), nullable=False)
    territory_id: Mapped[int | None] = mapped_column(ForeignKey("core.territory.id"), nullable=True)
    case_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
