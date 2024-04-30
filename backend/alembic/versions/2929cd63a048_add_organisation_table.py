"""add organisation table

Revision ID: 2929cd63a048
Revises: ba4ce1f66866
Create Date: 2023-09-18 16:00:07.290568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2929cd63a048"
down_revision = "ba4ce1f66866"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organisation",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("name", sa.VARCHAR(length=1024), nullable=False),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_organisation_id"), "organisation", ["id"], unique=False)
    op.add_column(
        "algoritme",
        sa.Column("organisation_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "algoritme_organisation_fkey",
        "algoritme",
        "organisation",
        ["organisation_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("algoritme_organisation_fkey", "algoritme", type_="foreignkey")
    op.drop_column("algoritme", "organisation_id")
    op.drop_index(op.f("ix_organisation_id"), table_name="organisation")
    op.drop_table("organisation")
