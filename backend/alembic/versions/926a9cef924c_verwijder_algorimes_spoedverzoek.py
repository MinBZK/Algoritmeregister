"""verwijder algorimes (spoedverzoek)

Revision ID: 926a9cef924c
Revises: f35c8031d388
Create Date: 2022-12-05 12:23:43.539969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "926a9cef924c"
down_revision = "f35c8031d388"
branch_labels = None
depends_on = None


def upgrade() -> None:
    ids_to_be_removed = [46, 47, 48, 49, 50, 51, 52]
    query = sa.text("delete from algoritme where id in :ids_to_be_removed")
    connection = op.get_bind()
    connection.execute(query, ids_to_be_removed=tuple(ids_to_be_removed))


def downgrade() -> None:
    pass
