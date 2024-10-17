"""add state in algoritme_version

Revision ID: 59ae16a67b97
Revises: 808e25658734
Create Date: 2024-05-31 11:53:10.552962

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59ae16a67b97"
down_revision = "808e25658734"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "algoritme_version",
        sa.Column("state", sa.VARCHAR(), server_default="STATE_1", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("algoritme_version", "state")
