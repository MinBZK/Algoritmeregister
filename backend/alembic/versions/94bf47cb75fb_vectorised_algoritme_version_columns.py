"""vectorised algoritme version columns

Revision ID: 94bf47cb75fb
Revises: 3de4ce027fe0
Create Date: 2023-10-30 11:08:48.176935

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "94bf47cb75fb"
down_revision = "3de4ce027fe0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("alembic/scripts/create_vectorized_column.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    with open("alembic/scripts/remove_vectorized_column.sql") as file:
        op.execute(file.read())
