"""remove leverancier_id

Revision ID: 0a1b6fc81205
Revises: 0a0ff83803b0
Create Date: 2023-04-19 17:06:04.283044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0a1b6fc81205"
down_revision = "0a0ff83803b0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("algoritme", "leverancier_id")


def downgrade() -> None:
    op.add_column(
        "algoritme",
        sa.Column(
            "leverancier_id",
            sa.VARCHAR(length=1024),
            autoincrement=False,
            nullable=True,
        ),
    )
