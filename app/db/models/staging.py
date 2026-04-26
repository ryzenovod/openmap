from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class StgImportBatch(Base):
    __tablename__ = "stg_import_batch"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source_filename: Mapped[str] = mapped_column(Text, nullable=False)
    total_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    success_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class StgCaseRow(Base):
    __tablename__ = "stg_case_row"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(ForeignKey("staging.stg_import_batch.id"), nullable=False)
    row_num: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_payload: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_text: Mapped[str | None] = mapped_column(Text, nullable=True)


class StgFileMapping(Base):
    __tablename__ = "stg_file_mapping"
    __table_args__ = {"schema": "staging"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_name: Mapped[str] = mapped_column(Text, nullable=False)
    source_column: Mapped[str] = mapped_column(Text, nullable=False)
    target_field: Mapped[str] = mapped_column(Text, nullable=False)
