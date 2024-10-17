"""execute full text search configuration for frisian language

Revision ID: dc89dfa5c832
Revises: 3a08d0a0aede
Create Date: 2024-04-02 16:30:43.079651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dc89dfa5c832"
down_revision = "3a08d0a0aede"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # pass
    with open(
        "alembic/scripts/create_frysian_full_text_search_configuration.sql"
    ) as file:
        op.execute(file.read())


def downgrade() -> None:
    # No downgrade available.
    pass
