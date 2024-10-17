"""add organisation_details

Revision ID: 79c11dd82bc1
Revises: f3c9f5768daf
Create Date: 2023-12-06 14:12:24.554285

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import Language

# revision identifiers, used by Alembic.
revision = "79c11dd82bc1"
down_revision = "f3c9f5768daf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "organisation",
        sa.Column("show_page", sa.Boolean(), nullable=False, server_default="False"),
    )

    language = postgresql.ENUM(Language, name="language", create_type=False)

    op.create_table(
        "organisation_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organisation_id", sa.Integer(), nullable=False),
        sa.Column("language", language, nullable=False),
        sa.Column("name", sa.VARCHAR(length=1024), nullable=False),
        sa.Column("email", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("about", sa.VARCHAR(length=2500), nullable=True),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organisation_id"], ["organisation.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "language", "organisation_id", name="language_organisation_id_uc"
        ),
    )
    op.create_index(
        op.f("ix_organisation_details_id"), "organisation_details", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_organisation_details_id"), table_name="organisation_details")
    op.drop_table("organisation_details")

    op.drop_column("organisation", "show_page")
