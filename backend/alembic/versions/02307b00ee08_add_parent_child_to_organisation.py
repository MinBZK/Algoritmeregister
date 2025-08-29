"""add_parent_child_to_organisation

Revision ID: 02307b00ee08
Revises: ab94ba0fb1e1
Create Date: 2025-05-14 13:10:30.757847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02307b00ee08'
down_revision = 'ab94ba0fb1e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('organisation', sa.Column('parent_id', sa.VARCHAR(), nullable=True))
    op.add_column('organisation', sa.Column('child_id', sa.VARCHAR(), nullable=True))


def downgrade() -> None:
    op.drop_column('organisation', 'parent_id')
    op.drop_column('organisation', 'child_id')
