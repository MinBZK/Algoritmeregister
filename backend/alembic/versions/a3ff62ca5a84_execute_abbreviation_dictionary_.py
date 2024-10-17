"""execute_abbreviation_dictionary_configuration

Revision ID: a3ff62ca5a84
Revises: 8420ea417658
Create Date: 2024-02-12 17:13:04.828637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a3ff62ca5a84"
down_revision = "d807befdcc18"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open(
        "alembic/scripts/execute_abbreviation_dictionairy_configuration.sql"
    ) as file:
        op.execute(file.read())


def downgrade() -> None:
    # No downgrade available.
    pass
