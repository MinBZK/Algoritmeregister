"""rename schema to standard_version

Revision ID: 04b904159980
Revises: 845b0b6e654f
Create Date: 2023-04-05 11:57:40.883818

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "04b904159980"
down_revision = "845b0b6e654f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "algoritme_version", "schema", nullable=True, new_column_name="standard_version"
    )


def downgrade() -> None:
    op.alter_column(
        "algoritme_version", "standard_version", nullable=True, new_column_name="schema"
    )
