"""add action_history table

Revision ID: 0a0ff83803b0
Revises: 6ce739d70f55
Create Date: 2023-04-13 15:12:33.051656

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import OperationEnum

# revision identifiers, used by Alembic.
revision = "0a0ff83803b0"
down_revision = "8691fce44bf2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    operation = postgresql.ENUM(OperationEnum, name="operation", create_type=False)
    operation.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "action_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("algoritme_version_id", sa.Integer(), nullable=False),
        sa.Column(
            "operation",
            operation,
            nullable=False,
        ),
        sa.Column("user_id", sa.VARCHAR(length=1024), nullable=False),
        sa.Column(
            "create_dt",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["algoritme_version_id"],
            ["algoritme_version.id"],
            name="action_history_algoritme_version_fkey",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_action_history_id"), "action_history", ["id"], unique=False
    )
    op.drop_column("algoritme_version", "end_dt")
    op.drop_column("algoritme_version", "created_by")


def downgrade() -> None:
    op.add_column(
        "algoritme_version",
        sa.Column(
            "created_by",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
            server_default="Unknown due to alembic downgrade",
        ),
    )
    op.add_column(
        "algoritme_version",
        sa.Column(
            "end_dt",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_index(op.f("ix_action_history_id"), table_name="action_history")
    op.drop_table("action_history")

    new_type = postgresql.ENUM(OperationEnum, name="operation", create_type=False)
    new_type.drop(op.get_bind())
