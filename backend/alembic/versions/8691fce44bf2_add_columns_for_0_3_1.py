"""add columns for 0.3.1

Revision ID: 8691fce44bf2
Revises: 6ce739d70f55
Create Date: 2023-04-18 13:28:26.382907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8691fce44bf2"
down_revision = "6ce739d70f55"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "algoritme_version",
        sa.Column("provider", sa.VARCHAR(length=100), nullable=True),
    )
    op.add_column(
        "algoritme_version",
        sa.Column("process_index_url", sa.VARCHAR(length=500), nullable=True),
    )
    op.add_column(
        "algoritme_version", sa.Column("tags", sa.VARCHAR(length=2500), nullable=True)
    )
    op.add_column(
        "algoritme_version",
        sa.Column("source_id", sa.VARCHAR(length=100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("algoritme_version", "tags")
    op.drop_column("algoritme_version", "process_index_url")
    op.drop_column("algoritme_version", "provider")
    op.drop_column("algoritme_version", "source_id")
