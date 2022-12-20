"""algoritme uuid

Revision ID: 995060402de4
Revises: 926a9cef924c
Create Date: 2022-12-05 21:33:36.143948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "995060402de4"
down_revision = "926a9cef924c"
branch_labels = None
depends_on = None

tables = ["algoritme", "inzet", "juridisch", "metadata", "toepassing", "toezicht"]


def upgrade() -> None:
    op.add_column(
        table_name="algoritme",
        column=sa.Column(
            "uuid",
            UUID(as_uuid=True),
            nullable=False,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    op.create_index(
        index_name="index_uuid", table_name="algoritme", columns=["uuid"], unique=True
    )

    for table in tables:
        op.add_column(
            table_name=table,
            column=sa.Column(
                "toegevoegd_op",
                sa.DateTime(timezone=True),
                server_default=sa.sql.func.now(),
                nullable=False,
            ),
        )


def downgrade() -> None:
    for table in tables:
        op.drop_column(table_name=table, column_name="toegevoegd_op")
    op.drop_column(table_name="algoritme", column_name="uuid")
