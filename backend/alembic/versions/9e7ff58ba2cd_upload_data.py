"""upload data

Revision ID: 9e7ff58ba2cd
Revises: 216e1a80d74b
Create Date: 2022-11-22 11:53:02.393973

"""
from alembic import op
import os

# revision identifiers, used by Alembic.
revision = '9e7ff58ba2cd'
down_revision = '216e1a80d74b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    structure_filepath = os.path.abspath("alembic/scripts/init_testdata.sql")
    with open(structure_filepath) as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")
    pass


def downgrade() -> None:
    tables = ["algemene_informatie", "inzet", "juridisch", "toepassing", "toezicht", "metadata"]
    for table in tables:
        op.execute(f"drop table {table} cascade")
