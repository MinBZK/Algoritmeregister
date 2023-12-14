"""execute full text search database configuration

Revision ID: 3de4ce027fe0
Revises: d621bd490e48
Create Date: 2023-11-14 11:46:16.008798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3de4ce027fe0"
down_revision = "d621bd490e48"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("alembic/scripts/execute_full_text_search_configuration.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    pass
