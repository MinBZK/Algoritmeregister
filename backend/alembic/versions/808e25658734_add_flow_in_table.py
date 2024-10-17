"""add flow in table

Revision ID: 808e25658734
Revises: dc89dfa5c832
Create Date: 2024-05-29 14:20:48.811051

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "808e25658734"
down_revision = "dc89dfa5c832"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "organisation",
        sa.Column("flow", sa.VARCHAR(), server_default="ictu_last", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("organisation", "flow")
