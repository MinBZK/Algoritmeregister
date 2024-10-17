"""increase column sizes of provider, lawful_basis_link and methods_and_models

Revision ID: e4dc5e7bafc3
Revises: 116c2febf399
Create Date: 2023-12-19 15:51:20.345004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e4dc5e7bafc3"
down_revision = "116c2febf399"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "algoritme_version",
        "provider",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.VARCHAR(length=5000),
        existing_nullable=True,
    )
    op.alter_column(
        "algoritme_version",
        "lawful_basis_link",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.VARCHAR(length=5000),
        existing_nullable=True,
    )
    op.alter_column(
        "algoritme_version",
        "methods_and_models",
        existing_type=sa.VARCHAR(length=5000),
        type_=sa.VARCHAR(length=10000),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "algoritme_version",
        "provider",
        existing_type=sa.VARCHAR(length=5000),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )
    op.alter_column(
        "algoritme_version",
        "lawful_basis_link",
        existing_type=sa.VARCHAR(length=5000),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )
    op.alter_column(
        "algoritme_version",
        "methods_and_models",
        existing_type=sa.VARCHAR(length=10000),
        type_=sa.VARCHAR(length=5000),
        existing_nullable=True,
    )
