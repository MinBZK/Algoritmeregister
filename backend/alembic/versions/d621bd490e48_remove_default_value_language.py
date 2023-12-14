"""remove default value language

Revision ID: d621bd490e48
Revises: c6bff8b8c900
Create Date: 2023-10-02 14:55:10.969871

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "d621bd490e48"
down_revision = "c6bff8b8c900"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "algoritme_version", "language", server_default=None, nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "algoritme_version", "language", server_default="NLD", nullable=True
    )
