"""add preferred name

Revision ID: ab94ba0fb1e1
Revises: 0c2d4ffb07ff
Create Date: 2025-04-09 15:14:24.431678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab94ba0fb1e1'
down_revision = '0c2d4ffb07ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('organisation', sa.Column('preferred_name', sa.VARCHAR(), nullable=True))
    op.alter_column('organisation', 'kvk_number', existing_type=sa.Integer(), type_=sa.VARCHAR(length=8), nullable=True)

def downgrade() -> None:
    op.drop_column('organisation', 'preferred_name')
    op.alter_column('organisation', 'kvk_number', existing_type=sa.VARCHAR(length=8), type_=sa.Integer(), nullable=True)