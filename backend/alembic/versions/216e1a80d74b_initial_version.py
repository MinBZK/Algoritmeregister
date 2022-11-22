"""initial-version

Revision ID: 216e1a80d74b
Revises: Builds initial structure from init.sql
Create Date: 2022-11-22 10:11:29.745888

"""
from alembic import op
import os

# revision identifiers, used by Alembic.
revision = '216e1a80d74b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    structure_filepath = os.path.abspath("alembic/scripts/init.sql")
    with open(structure_filepath) as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")
    pass


def downgrade() -> None:
    op.drop_table("default")
