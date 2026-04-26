"""Initial schemas and PostGIS extension

Revision ID: 20260426_0001
Revises:
Create Date: 2026-04-26 00:00:00
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260426_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.execute("CREATE SCHEMA IF NOT EXISTS staging")
    op.execute("CREATE SCHEMA IF NOT EXISTS core")
    op.execute("CREATE SCHEMA IF NOT EXISTS mart")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS mart CASCADE")
    op.execute("DROP SCHEMA IF EXISTS core CASCADE")
    op.execute("DROP SCHEMA IF EXISTS staging CASCADE")
    op.execute("DROP EXTENSION IF EXISTS postgis")
