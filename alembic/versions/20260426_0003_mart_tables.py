"""Create mart tables and indexes

Revision ID: 20260426_0003
Revises: 20260426_0002
Create Date: 2026-04-26 01:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260426_0003"
down_revision = "20260426_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mart_case_map_daily",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("aggregation_date", sa.Date(), nullable=False),
        sa.Column("territory_id", sa.Integer(), nullable=False),
        sa.Column("case_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mbt_positive_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cv_positive_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("incidence_per_100k", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["territory_id"], ["core.territory.id"]),
        sa.UniqueConstraint("aggregation_date", "territory_id", name="uq_mart_case_map_daily_key"),
        schema="mart",
    )
    op.create_index(
        "ix_mart_case_map_daily_date_territory",
        "mart_case_map_daily",
        ["aggregation_date", "territory_id"],
        schema="mart",
    )

    op.create_table(
        "mart_case_map_monthly",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("territory_id", sa.Integer(), nullable=False),
        sa.Column("case_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mbt_positive_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cv_positive_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("incidence_per_100k", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["territory_id"], ["core.territory.id"]),
        sa.UniqueConstraint("year", "month", "territory_id", name="uq_mart_case_map_monthly_key"),
        schema="mart",
    )
    op.create_index(
        "ix_mart_case_map_monthly_year_month_territory",
        "mart_case_map_monthly",
        ["year", "month", "territory_id"],
        schema="mart",
    )

    op.create_table(
        "mart_chart_yearly",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("territory_id", sa.Integer(), nullable=True),
        sa.Column("case_count", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["territory_id"], ["core.territory.id"]),
        sa.UniqueConstraint("year", "territory_id", name="uq_mart_chart_yearly_key"),
        schema="mart",
    )
    op.create_index("ix_mart_chart_yearly_year", "mart_chart_yearly", ["year"], schema="mart")

    op.create_table(
        "mart_chart_structure",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("dimension", sa.String(length=32), nullable=False),
        sa.Column("bucket", sa.String(length=64), nullable=False),
        sa.Column("territory_id", sa.Integer(), nullable=True),
        sa.Column("case_count", sa.Integer(), nullable=False, server_default="0"),
        sa.ForeignKeyConstraint(["territory_id"], ["core.territory.id"]),
        sa.UniqueConstraint(
            "year",
            "dimension",
            "bucket",
            "territory_id",
            name="uq_mart_chart_structure_key",
        ),
        schema="mart",
    )
    op.create_index(
        "ix_mart_chart_structure_year_dimension",
        "mart_chart_structure",
        ["year", "dimension"],
        schema="mart",
    )


def downgrade() -> None:
    op.drop_index("ix_mart_chart_structure_year_dimension", table_name="mart_chart_structure", schema="mart")
    op.drop_table("mart_chart_structure", schema="mart")

    op.drop_index("ix_mart_chart_yearly_year", table_name="mart_chart_yearly", schema="mart")
    op.drop_table("mart_chart_yearly", schema="mart")

    op.drop_index(
        "ix_mart_case_map_monthly_year_month_territory",
        table_name="mart_case_map_monthly",
        schema="mart",
    )
    op.drop_table("mart_case_map_monthly", schema="mart")

    op.drop_index("ix_mart_case_map_daily_date_territory", table_name="mart_case_map_daily", schema="mart")
    op.drop_table("mart_case_map_daily", schema="mart")
