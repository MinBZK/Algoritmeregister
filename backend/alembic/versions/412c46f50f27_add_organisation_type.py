"""add organisation type

Revision ID: 412c46f50f27
Revises: d621bd490e48
Create Date: 2023-11-01 12:09:40.159758

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.schemas import OrgType

# revision identifiers, used by Alembic.
revision = "412c46f50f27"
down_revision = "b5ce4561c092"
branch_labels = None
depends_on = None


def upgrade() -> None:
    org_type = postgresql.ENUM(OrgType, name="type", create_type=False)
    org_type.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "organisation",
        sa.Column("type", org_type, nullable=True),
    )


def downgrade() -> None:
    # Results in loss of data!!!
    op.drop_column("organisation", "type")

    org_type = postgresql.ENUM(OrgType, name="type", create_type=False)
    org_type.drop(op.get_bind())
