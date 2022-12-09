"""iama column

Revision ID: 4fa08b56de37
Revises: 995060402de4
Create Date: 2022-12-09 08:57:39.343415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4fa08b56de37"
down_revision = "995060402de4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute("delete from algoritme")
    op.add_column(
        table_name="juridisch",
        column=sa.Column("iama", sa.VARCHAR(128), nullable=False),
    )
    op.add_column(
        table_name="juridisch",
        column=sa.Column("iama_description", sa.VARCHAR(5000), nullable=False),
    )


def downgrade() -> None:
    [
        op.drop_column(table_name="juridisch", column_name=column_name)
        for column_name in ["iama", "iama_description"]
    ]
