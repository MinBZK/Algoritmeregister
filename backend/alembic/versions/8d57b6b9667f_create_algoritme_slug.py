"""create algoritme slug

Revision ID: 8d57b6b9667f
Revises: 4fa08b56de37
Create Date: 2022-12-09 09:42:25.407514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8d57b6b9667f"
down_revision = "4fa08b56de37"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute("delete from algoritme")
    slug_column_name = "slug"
    table_name = "algoritme"
    op.add_column(
        table_name=table_name,
        column=sa.Column(slug_column_name, sa.VARCHAR(128), nullable=False),
    )
    op.create_index(
        index_name="index_slug",
        table_name=table_name,
        columns=[slug_column_name],
        unique=True,
    )


def downgrade() -> None:
    op.drop_column(table_name="algoritme", column_name="slug")
