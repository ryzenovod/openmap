"""Create staging and core tables for iteration 2

Revision ID: 20260426_0002
Revises: 20260426_0001
Create Date: 2026-04-26 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260426_0002"
down_revision = "20260426_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stg_import_batch",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_filename", sa.Text(), nullable=False),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        schema="staging",
    )
    op.create_table(
        "stg_case_row",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("row_num", sa.Integer(), nullable=False),
        sa.Column("raw_payload", sa.Text(), nullable=False),
        sa.Column("normalized_payload", sa.Text(), nullable=True),
        sa.Column("error_text", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["batch_id"], ["staging.stg_import_batch.id"]),
        schema="staging",
    )
    op.create_table(
        "stg_file_mapping",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("file_name", sa.Text(), nullable=False),
        sa.Column("source_column", sa.Text(), nullable=False),
        sa.Column("target_field", sa.Text(), nullable=False),
        schema="staging",
    )

    op.create_table(
        "dict_mkb10",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["core.dict_mkb10.id"]),
        schema="core",
    )
    op.create_index("ix_dict_mkb10_code", "dict_mkb10", ["code"], unique=False, schema="core")

    for table_name, code_len in [
        ("dict_territory_type", 32),
        ("dict_case_status_gdu", 32),
        ("dict_sign_status", 16),
        ("dict_geocode_status", 16),
        ("dict_case_type", 32),
        ("dict_location_role", 32),
    ]:
        op.create_table(
            table_name,
            sa.Column("code", sa.String(length=code_len), primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            schema="core",
        )

    op.create_table(
        "territory",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("territory_type_code", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["core.territory.id"]),
        sa.ForeignKeyConstraint(["territory_type_code"], ["core.dict_territory_type.code"]),
        schema="core",
    )

    op.create_table(
        "population_stat",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("territory_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("population", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["territory_id"], ["core.territory.id"]),
        sa.UniqueConstraint("territory_id", "year", name="uq_population_stat_territory_year"),
        schema="core",
    )

    op.create_table(
        "patient",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("fio_raw", sa.String(length=255), nullable=False),
        sa.Column("fio_norm", sa.String(length=255), nullable=False),
        sa.Column("birth_year", sa.Integer(), nullable=True),
        sa.UniqueConstraint("fio_norm", "birth_year", name="uq_patient_fio_norm_birth_year"),
        schema="core",
    )

    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("normalized_text", sa.Text(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=True),
        sa.Column("lon", sa.Float(), nullable=True),
        sa.Column("geocode_status_code", sa.String(length=16), nullable=True),
        sa.ForeignKeyConstraint(["geocode_status_code"], ["core.dict_geocode_status.code"]),
        schema="core",
    )

    op.create_table(
        "patient_address",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["core.patient.id"]),
        sa.ForeignKeyConstraint(["address_id"], ["core.address.id"]),
        sa.UniqueConstraint("patient_id", "address_id", name="uq_patient_address_pair"),
        schema="core",
    )

    op.create_table(
        "medical_case",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("legacy_case_num", sa.String(length=64), nullable=True),
        sa.Column("registration_date", sa.Date(), nullable=False),
        sa.Column("diagnosis_raw", sa.Text(), nullable=False),
        sa.Column("work_raw", sa.Text(), nullable=True),
        sa.Column("gdu_code", sa.String(length=32), nullable=True),
        sa.Column("cv_code", sa.String(length=16), nullable=True),
        sa.Column("mbt_code", sa.String(length=16), nullable=True),
        sa.Column("case_type_code", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["patient_id"], ["core.patient.id"]),
        sa.ForeignKeyConstraint(["gdu_code"], ["core.dict_case_status_gdu.code"]),
        sa.ForeignKeyConstraint(["cv_code"], ["core.dict_sign_status.code"]),
        sa.ForeignKeyConstraint(["mbt_code"], ["core.dict_sign_status.code"]),
        sa.ForeignKeyConstraint(["case_type_code"], ["core.dict_case_type.code"]),
        sa.UniqueConstraint(
            "patient_id",
            "registration_date",
            "diagnosis_raw",
            "legacy_case_num",
            name="uq_medical_case_dedup_key",
        ),
        schema="core",
    )

    op.create_table(
        "case_event",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("medical_case_id", sa.Integer(), nullable=False),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["medical_case_id"], ["core.medical_case.id"]),
        schema="core",
    )

    op.create_table(
        "case_location",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("medical_case_id", sa.Integer(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.Column("location_role_code", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["medical_case_id"], ["core.medical_case.id"]),
        sa.ForeignKeyConstraint(["address_id"], ["core.address.id"]),
        sa.ForeignKeyConstraint(["location_role_code"], ["core.dict_location_role.code"]),
        sa.UniqueConstraint("medical_case_id", "address_id", name="uq_case_location_pair"),
        schema="core",
    )


def downgrade() -> None:
    for name in [
        "case_location",
        "case_event",
        "medical_case",
        "patient_address",
        "address",
        "patient",
        "population_stat",
        "territory",
        "dict_location_role",
        "dict_case_type",
        "dict_geocode_status",
        "dict_sign_status",
        "dict_case_status_gdu",
        "dict_territory_type",
    ]:
        op.drop_table(name, schema="core")
    op.drop_index("ix_dict_mkb10_code", table_name="dict_mkb10", schema="core")
    op.drop_table("dict_mkb10", schema="core")

    for name in ["stg_file_mapping", "stg_case_row", "stg_import_batch"]:
        op.drop_table(name, schema="staging")
