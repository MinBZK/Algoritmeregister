"""add language dependency

Revision ID: c6bff8b8c900
Revises: 42e58f22ba71
Create Date: 2023-10-02 14:50:06.490302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import Language

# revision identifiers, used by Alembic.
revision = "c6bff8b8c900"
down_revision = "42e58f22ba71"
branch_labels = None
depends_on = None


def upgrade() -> None:
    language = postgresql.ENUM(Language, name="language", create_type=False)
    language.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "algoritme_version",
        sa.Column("language", language, server_default="NLD", nullable=True),
    )


def downgrade() -> None:
    op.drop_column("algoritme_version", "language")

    language_enum = postgresql.ENUM(Language, name="language", create_type=False)
    language_enum.drop(op.get_bind())
