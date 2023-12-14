"""Create words table for algoritme version

Revision ID: b5ce4561c092
Revises: 94bf47cb75fb
Create Date: 2023-11-13 12:18:23.132668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b5ce4561c092"
down_revision = "94bf47cb75fb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("alembic/scripts/create_words_table.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    with open("alembic/scripts/remove_words_table.sql") as file:
        op.execute(file.read())
