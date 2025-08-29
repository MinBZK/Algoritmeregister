"""
This module assigns a type to each organisation.
It is meant to be run as a script once, and will not be used in the actual application.
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models import Organisation
from app.schemas import OrgType
from app.util.logger import get_logger

# initialize new independent logger
logger = get_logger(__name__)

mapping: dict[str, OrgType] = {
    "rijksdienst-voor-ondernemend-nederland": OrgType.agentschap,
    "rijksdienst-voor-identiteitsgegevens": OrgType.agentschap,
    "kadaster": OrgType.zelfstandig_bestuursorgaan,
    "uitvoeringsinstituut-werknemersverzekeringen": OrgType.zelfstandig_bestuursorgaan,
    "sociale-verzekeringsbank": OrgType.zelfstandig_bestuursorgaan,
    "belastingdienst": OrgType.organisatieonderdeel,
    "centraal-justitieel-incassobureau": OrgType.zelfstandig_bestuursorgaan,
    "centraal-bureau-rijvaardigheidsbewijzen": OrgType.zelfstandig_bestuursorgaan,
    "nederlands-forensisch-instituut": OrgType.agentschap,
    "inspectie-van-het-onderwijs": OrgType.organisatieonderdeel,
    "DCMR-milieudienst-rijnmond": OrgType.regionaal_samenwerkingsorgaan,
    "kamer-van-koophandel": OrgType.zelfstandig_bestuursorgaan,
    "odmh": OrgType.regionaal_samenwerkingsorgaan,
    "stichting-inlichtingenbureau": OrgType.organisatie_met_overheidsbemoeienis,
    "autoriteit-persoonsgegevens": OrgType.zelfstandig_bestuursorgaan,
    "rijkswaterstaat": OrgType.agentschap,
    "sandbox": OrgType.overig,
    "justitiele-informatiedienst": OrgType.agentschap,
    "logius": OrgType.agentschap,
    "SED-organisatie": OrgType.regionaal_samenwerkingsorgaan,
    "dordrecht": OrgType.gemeente,
    "rivm": OrgType.agentschap,
    "toeslagen": OrgType.organisatieonderdeel,
    "cibg": OrgType.agentschap,
    "igj": OrgType.organisatieonderdeel,
    "dji": OrgType.agentschap,
    "stichting-mijnbouwschade-groningen": OrgType.zelfstandig_bestuursorgaan,
    "politie": OrgType.politie,
    "ind": OrgType.agentschap,
    "grsk": OrgType.regionaal_samenwerkingsorgaan,
    "raad-voor-de-rechtsbijstand": OrgType.zelfstandig_bestuursorgaan,
    "alliander": OrgType.overig,
    "hh-delfland": OrgType.waterschap,
    "raad-kinderbescherming": OrgType.organisatieonderdeel,
}


def get_orgs(db: Session) -> list[Organisation]:
    return db.query(Organisation).filter(Organisation.type.is_(None)).all()


def assign_type(db: Session, org: Organisation):
    """
    Translate all algorithms to English.
    """
    assigned_type = None

    if org.code.startswith("gemeente"):
        assigned_type = OrgType.gemeente
    elif org.code.startswith("provincie"):
        assigned_type = OrgType.provincie
    elif org.code.startswith("waterschap"):
        assigned_type = OrgType.waterschap
    elif org.code.startswith("ministerie"):
        assigned_type = OrgType.ministerie
    elif org.code.startswith("omgevingsdienst"):
        assigned_type = OrgType.regionaal_samenwerkingsorgaan
    elif org.code.startswith("veiligheidsregio"):
        assigned_type = OrgType.regionaal_samenwerkingsorgaan
    else:
        assigned_type = mapping.get(org.code)

    if assigned_type == None:
        logger.info(f"Could not assign {org.code} a type")
        return

    logger.info(f"Assigned {org.code} as {assigned_type}")
    db.query(Organisation).filter(Organisation.id == org.id).update(
        {Organisation.type: assigned_type}, synchronize_session=False
    )
    db.commit()


if __name__ == "__main__":
    logger.info("Starting assigning types to orgs.")
    db = SessionLocal()
    orgs = get_orgs(db)
    for org in orgs:
        assign_type(db, org)
    logger.info("Finished assigning types to orgs.")
    db.close()
