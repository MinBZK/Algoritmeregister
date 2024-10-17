"""migrate data to org table

Revision ID: 42e58f22ba71
Revises: 2929cd63a048
Create Date: 2023-09-18 16:08:39.722690

"""
from alembic import op
import sqlalchemy as sa
from app.models import Organisation

# revision identifiers, used by Alembic.
revision = "42e58f22ba71"
down_revision = "2929cd63a048"
branch_labels = None
depends_on = None

name_mapping = {
    "provincie-noord-brabant": "Provincie Noord-Brabant",
    "provincie-noord-holland": "Provincie Noord-Holland",
    "provincie-zuid-holland": "Provincie Zuid-Holland",
    "ministerie-fin": "Ministerie van Financiën",
    "ministerie-ezk": "Ministerie van Economische Zaken en Klimaat",
    "ministerie-az": "Ministerie van Algemene Zaken",
    "ministerie-bzk": "Ministerie van Binnenlandse Zaken en Koninkrijksrelaties",
    "ministerie-bz": "Ministerie van Buitenlandse Zaken",
    "ministerie-def": "Ministerie van Defensie",
    "ministerie-ienw": "Ministerie van Infrastructuur en Waterstaat",
    "ministerie-jenv": "Ministerie van Justitie en Veiligheid",
    "ministerie-lnw": "Ministerie van Landbouw, Natuur en Voedselkwaliteit",
    "ministerie-ocw": "Ministerie van Onderwijs, Cultuur en Wetenschap",
    "ministerie-szw": "Ministerie van Sociale Zaken en Werkgelegenheid",
    "ministerie-vws": "Ministerie van Volksgezondheid, Welzijn en Sport",
    "justitiele-informatiedienst": "Justitiële Informatiedienst",
    "rvig": "Rijksdienst voor Identiteitsgegevens",
    "directie-financieel-economische-zaken": "Directie Financieel-Economische Zaken",
    "inspectie-van-het-onderwijs": "Inspectie van het Onderwijs (OCW)",
    "gemeente-sudwest-fryslan": "Gemeente Súdwest-Fryslân",
    "omgevingsdienst-west-brabant": "Omgevingsdienst Midden- en West-Brabant",
    "gemeente-goeree-overflakkee": "Gemeente Goeree-Overflakkee",
    "gemeente-ouder-amstel": "Gemeente Ouder-Amstel",
    "kamer-van-koophandel": "Kamer van Koophandel",
    "rijksdienst-voor-ondernemend-nederland": "Rijksdienst voor Ondernemend Nederland",
    "gemeente-shertogenbosch": "Gemeente 's-Hertogenbosch",
    "odmh": "Omgevingsdienst Midden-Holland",
    "SED-organisatie": "SED Organisatie (Gemeente Stede Broec, Enkhuizen, Drechterland)",
    "provincie-friesland": "Provinsje Fryslân",
    "gemeente-geldrop-mierlo": "Gemeente Geldrop-Mierlo",
    "gemeente-nuenen-gerwen-en-nederwetten": "Gemeente Nuenen, Gerwen en Nederwetten",
    "gemeente-son-en-breugel": "Gemeente Son en Breugel",
    "DCMR-milieudienst-rijnmond": "DCMR Milieudienst Rijnmond",
}


def upgrade() -> None:
    conn = op.get_bind()
    res = conn.execute(sa.text("select id, owner from algoritme"))
    if not res:
        raise ConnectionError
    results = res.fetchall()

    if len(results) == 0:
        return
    # Construct the rows for organisation table. Done in dict so it is easy to see unique orgs
    unique_orgs = {}
    for r in results:
        if r[1] in name_mapping.keys():
            name = name_mapping[r[1]]
        else:
            name = r[1].split("-")
            name = [word.capitalize() for word in name]
            name = " ".join(name)

        entry = {"code": r[1], "name": name}

        key = r[1]
        if key not in unique_orgs.keys():
            unique_orgs[key] = entry

    # insertion is done with list
    orgs = [unique_orgs[key] for key in unique_orgs.keys()]
    conn.execute(Organisation.__table__.insert().values(orgs))  # type: ignore

    # Get the new data, so that we have the id's.
    res = conn.execute(sa.text("select id, code from organisation"))
    if not res:
        raise ConnectionError
    organisations = res.fetchall()

    # new column in algoritme must have proper id's for references
    when_text = " ".join(
        [f"WHEN owner='{org[1]}' THEN {org[0]}" for org in organisations]
    )
    update_statement = sa.text(
        f"""
        UPDATE algoritme
        SET organisation_id =
            CASE
                {when_text}
            END;
        """
    )
    conn.execute(update_statement)

    # When done, remove owner column. Now uses organisation_id instead.
    op.drop_column("algoritme", "owner")


def downgrade() -> None:
    op.add_column(
        "algoritme",
        sa.Column("owner", sa.VARCHAR(length=1024), autoincrement=False, nullable=True),
    )

    conn = op.get_bind()
    res = conn.execute(sa.text("select id, code, name from organisation"))
    if not res:
        raise ConnectionError
    results = res.fetchall()

    when_text = " ".join(
        [f"WHEN organisation_id='{r[0]}' THEN '{r[1]}'" for r in results]
    )
    set_owner_statement = sa.text(
        f"""
        UPDATE algoritme
        SET owner =
            CASE
                {when_text}
            END;
        """
    )
    conn.execute(set_owner_statement)

    reset_organisation_id_statement = sa.text(
        """
        UPDATE algoritme
        SET organisation_id = NULL
        """
    )
    conn.execute(reset_organisation_id_statement)

    conn.execute(sa.text("DELETE FROM organisation"))
