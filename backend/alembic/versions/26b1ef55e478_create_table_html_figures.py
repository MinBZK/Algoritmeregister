"""create_table_html_figures

Revision ID: 26b1ef55e478
Revises: 59ae16a67b97
Create Date: 2024-06-12 14:40:23.906428

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "26b1ef55e478"
down_revision = "cbebdfcd0582"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "html_figures",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("html", sa.TEXT, nullable=False),
        sa.Column("most_recent", sa.Boolean, nullable=False),
        sa.Column("static_data", sa.JSON, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("html_figures")
