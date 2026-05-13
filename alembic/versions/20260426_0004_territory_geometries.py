"""Add territory geometries for future choropleth layer

Revision ID: 20260426_0004
Revises: 20260426_0003
Create Date: 2026-04-26 02:00:00
"""

from alembic import op


revision = "20260426_0004"
down_revision = "20260426_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE core.territory_geometry (
            territory_id integer PRIMARY KEY REFERENCES core.territory(id) ON DELETE CASCADE,
            territory_name varchar(255) NOT NULL,
            level varchar(64),
            geom geometry(MultiPolygon, 4326) NOT NULL
        )
        """
    )
    op.execute(
        """
        CREATE INDEX ix_territory_geometry_geom
        ON core.territory_geometry
        USING GIST (geom)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS core.ix_territory_geometry_geom")
    op.execute("DROP TABLE IF EXISTS core.territory_geometry")
