from app.database.database import SessionLocal
from sqlalchemy.orm import Session

from app.middleware import kc_settings
from app.models.organisation import Organisation
from app.services.keycloak.repository import KeycloakRepository
from app.util.logger import get_logger


# initialize new independent logger
logger = get_logger(__name__)


def migrate_groups(db: Session):
    db_orgs = db.query(Organisation).all()
    db_org_codes = [o.code for o in db_orgs]

    kc_repo = KeycloakRepository(kc_settings)
    keycloak_orgs = kc_repo.get_groups()
    for orgs in keycloak_orgs:
        if orgs.name not in db_org_codes:
            users = kc_repo.get_group_members(orgs.id)
            print(orgs.name, "members: ", [u.username for u in users])


if __name__ == "__main__":
    logger.info(
        "Checking groups. reporting when an unknown group is found in keycloak."
    )
    db = SessionLocal()
    migrate_groups(db)
    logger.info("Finished checking groups.")
    db.close()
