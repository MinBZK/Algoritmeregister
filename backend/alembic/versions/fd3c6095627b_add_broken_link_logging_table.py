"""add_broken_link_logging_table

Revision ID: fd3c6095627b
Revises: 59ae16a67b97
Create Date: 2024-06-17 16:14:30.271900

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import Language


# revision identifiers, used by Alembic.
revision = "fd3c6095627b"
down_revision = "26b1ef55e478"
branch_labels = None
depends_on = None


def upgrade() -> None:
    language = postgresql.ENUM(Language, name="language", create_type=False)
    language.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "broken_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("lars", sa.String(length=8), nullable=True),
        sa.Column("name", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("organisation", sa.VARCHAR(length=1024), nullable=True),
        sa.Column("language", language, server_default=None, nullable=True),
        sa.Column("broken_links", sa.JSON, nullable=True),
        sa.Column("batch", sa.Integer(), nullable=True),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_broken_links_id"), "broken_links", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_broken_links_id"), table_name="broken_links")
    op.drop_table("broken_links")
