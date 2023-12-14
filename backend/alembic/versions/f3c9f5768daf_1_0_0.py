"""1.0.0

Revision ID: f3c9f5768daf
Revises: 412c46f50f27
Create Date: 2023-11-28 14:51:58.879670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f3c9f5768daf"
down_revision = "412c46f50f27"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "algoritme_version",
        sa.Column("publication_category", sa.VARCHAR(length=1000), nullable=True),
    )
    op.add_column(
        "algoritme_version",
        sa.Column("lawful_basis_grouping", sa.JSON(), nullable=True),
    )
    op.add_column(
        "algoritme_version",
        sa.Column("impacttoetsen_grouping", sa.JSON(), nullable=True),
    )
    op.add_column(
        "algoritme_version", sa.Column("source_data_grouping", sa.JSON(), nullable=True)
    )

    with open("alembic/scripts/upgrade_vector_1_0_0.sql") as file:
        op.execute(file.read())


def downgrade() -> None:
    with open("alembic/scripts/downgrade_vector_1_0_0.sql") as file:
        op.execute(file.read())
    op.drop_column("algoritme_version", "source_data_grouping")
    op.drop_column("algoritme_version", "impacttoetsen_grouping")
    op.drop_column("algoritme_version", "lawful_basis_grouping")
    op.drop_column("algoritme_version", "publication_category")
