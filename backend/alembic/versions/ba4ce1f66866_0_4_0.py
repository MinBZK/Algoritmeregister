"""0.4.0

Revision ID: ba4ce1f66866
Revises: 0a1b6fc81205
Create Date: 2023-05-30 11:29:29.903615

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ba4ce1f66866"
down_revision = "0a1b6fc81205"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "algoritme_version",
        sa.Column("begin_date", sa.VARCHAR(length=7), nullable=True),
    )
    op.add_column(
        "algoritme_version", sa.Column("end_date", sa.VARCHAR(length=7), nullable=True)
    )
    op.add_column(
        "algoritme_version",
        sa.Column("lawful_basis_link", sa.VARCHAR(length=200), nullable=True),
    )
    op.add_column(
        "algoritme_version",
        sa.Column("impacttoetsen", sa.VARCHAR(length=1024), nullable=True),
    )
    op.add_column(
        "algoritme_version",
        sa.Column("source_data_link", sa.VARCHAR(length=500), nullable=True),
    )
    op.alter_column(
        "algoritme_version",
        "provider",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "algoritme_version",
        "provider",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.drop_column("algoritme_version", "source_data_link")
    op.drop_column("algoritme_version", "impacttoetsen")
    op.drop_column("algoritme_version", "lawful_basis_link")
    op.drop_column("algoritme_version", "end_date")
    op.drop_column("algoritme_version", "begin_date")
