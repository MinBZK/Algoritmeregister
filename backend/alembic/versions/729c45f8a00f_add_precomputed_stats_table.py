"""add_precomputed_values_table

Revision ID: 729c45f8a00f
Revises: fd3c6095627b
Create Date: 2024-09-13 17:18:48.551788

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import Language


# revision identifiers, used by Alembic.
revision = '729c45f8a00f'
down_revision = 'fd3c6095627b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    language = postgresql.ENUM(Language, name="language", create_type=False)
    op.create_table(
        "precomputed_values", 
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("language", language, nullable=False),
        sa.Column("key", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("value", sa.JSON(), nullable=False),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("precomputed_values")
