"""adjust table name algemene_informatie

Revision ID: f35c8031d388
Revises: 9e7ff58ba2cd
Create Date: 2022-11-25 10:53:00.746239

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "f35c8031d388"
down_revision = "9e7ff58ba2cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("algemene_informatie", "algoritme")


def downgrade() -> None:
    op.rename_table("algoritme", "algemene_informatie")
