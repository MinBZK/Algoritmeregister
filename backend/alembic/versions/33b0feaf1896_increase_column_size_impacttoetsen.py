"""increase_column_size_impacttoetsen

Revision ID: 33b0feaf1896
Revises: 729c45f8a00f
Create Date: 2024-10-29 11:58:07.316625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33b0feaf1896'
down_revision = '729c45f8a00f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "algoritme_version",
        "impacttoetsen",
        existing_type=sa.VARCHAR(length=1024),
        type_=sa.VARCHAR(length=5000),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "algoritme_version",
        "impacttoetsen",
        existing_type=sa.VARCHAR(length=5000),
        type_=sa.VARCHAR(length=1024),
        existing_nullable=True,
    )
