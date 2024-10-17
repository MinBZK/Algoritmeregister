"""vectorised_organisation_details_column

Revision ID: 243d3a6d2320
Revises: a3ff62ca5a84
Create Date: 2024-03-25 16:39:43.425389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "243d3a6d2320"
down_revision = "a3ff62ca5a84"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("alembic/scripts/create_vectorized_column_org.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    with open("alembic/scripts/remove_vectorized_column_org.sql") as file:
        op.execute(file.read())
