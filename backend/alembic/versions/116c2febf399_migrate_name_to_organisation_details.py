"""migrate name to organisation_details

Revision ID: 116c2febf399
Revises: 79c11dd82bc1
Create Date: 2023-12-06 14:24:53.014796

"""
from alembic import op
import sqlalchemy as sa
from app.models import OrganisationDetails

# revision identifiers, used by Alembic.
revision = "116c2febf399"
down_revision = "79c11dd82bc1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    res = conn.execute(sa.text("select id, name from organisation"))
    if not res:
        raise ConnectionError
    organisations = res.fetchall()

    if len(organisations):
        organisation_details = []
        for org in organisations:
            entry = {"organisation_id": org[0], "language": "NLD", "name": org[1]}
            organisation_details.append(entry)

        conn.execute(
            OrganisationDetails.__table__.insert().values(organisation_details)
        )

    op.drop_column("organisation", "name")


def downgrade() -> None:
    op.add_column(
        "organisation",
        sa.Column("name", sa.VARCHAR(length=1024), nullable=True),
    )

    conn = op.get_bind()
    res = conn.execute(
        sa.text(
            "select name, organisation_id from organisation_details where language='NLD'"
        )
    )
    if not res:
        raise ConnectionError
    organisation_details = res.fetchall()

    if len(organisation_details):
        when_text = " ".join(
            [f"WHEN id='{r[1]}' THEN '{r[0]}'" for r in organisation_details]
        )
        set_owner_statement = sa.text(
            f"""
            UPDATE organisation
            SET name =
                CASE
                    {when_text}
                END;
            """
        )
        conn.execute(set_owner_statement)

        conn.execute(sa.text("DELETE FROM organisation_details"))

    op.alter_column("organisation", "name", server_default=None, nullable=False)
