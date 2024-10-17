"""Increase the about column of the organisation_details table

Revision ID: 8420ea417658
Revises: e4dc5e7bafc3
Create Date: 2024-01-29 19:12:12.627372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8420ea417658"
down_revision = "e4dc5e7bafc3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "organisation_details",
        "about",
        existing_type=sa.VARCHAR(length=2500),
        type_=sa.VARCHAR(length=10000),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "organisation_details",
        "about",
        existing_type=sa.VARCHAR(length=10000),
        type_=sa.VARCHAR(length=2500),
        existing_nullable=True,
    )
