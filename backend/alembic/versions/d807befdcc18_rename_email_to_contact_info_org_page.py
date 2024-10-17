"""rename_email_to_contact_info_org_page

Revision ID: d807befdcc18
Revises: 8420ea417658
Create Date: 2024-02-15 17:22:18.045561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d807befdcc18"
down_revision = "8420ea417658"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "organisation_details", "email", nullable=True, new_column_name="contact_info"
    )


def downgrade() -> None:
    op.alter_column(
        "organisation_details", "contact_info", nullable=True, new_column_name="email"
    )
