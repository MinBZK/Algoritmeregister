"""Convert DB action ENUM to VARCHAR

Revision ID: cbebdfcd0582
Revises: 59ae16a67b97
Create Date: 2024-06-24 15:50:18.051669

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.schemas import OperationEnum

# revision identifiers, used by Alembic.
revision = "cbebdfcd0582"
down_revision = "59ae16a67b97"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "action_history", "operation", type_=sa.VARCHAR(length=32), nullable=False
    )
    op.execute("DROP TYPE operation")


def downgrade() -> None:
    operation = postgresql.ENUM(OperationEnum, name="operation", create_type=False)
    operation.create(op.get_bind(), checkfirst=True)
    op.execute(
        "ALTER TABLE action_history ALTER COLUMN operation TYPE operation USING operation::text::operation"
    )
