from app.services.keycloak import KeycloakRepository
from app.middleware import kc_settings
from app.database.database import SessionLocal
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import (
    select
)
from app.util.logger import get_logger

# python -m scripts.archive.keycloak_add_org_id_to_groups_attribute

# initialize new independent logger
logger = get_logger(__name__)

def main(db: Session):
    kc_repo = KeycloakRepository(kc_settings)
    users: list[dict] = kc_repo.client.get_users()
    stmt = (select(models.Organisation.code,
                models.Organisation.org_id))
    results = db.execute(stmt)
    organisations = [{"code": row.code, "org_id": row.org_id} for row in results]
    
    for user in users:
        user_id = user.get("id", None)
        if not user_id:
            logger.warning(f"User ID not found for user: {user}")
            continue
        
        attributes = user.get("attributes", {})
        groups = attributes.get("groups", [])
                
        if len(groups):
            logger.info(f"Groups found for user {user.get('username')}: {groups}")
            for group in groups:
                for org in organisations:
                    if group == org["code"] and org["org_id"] not in groups:
                        logger.info(f"Found group: {group}")
                        logger.info(f"Corresponding org_id: {org['org_id']}")
                        logger.info(f"Current attributes before adding org_id: {attributes}")
                        logger.info(f"Adding org_id {org['org_id']} to user {user.get('username')}")
                        attributes["groups"].append(org["org_id"])
                        logger.info(f"Current attributes after adding org_id: {attributes}")
                        user["attributes"] = attributes
                        kc_repo.client.update_user(user_id, user)
            # break

if __name__ == "__main__":
    logger.info("Starting updating groups attribute in keycloak with org_id.")
    db = SessionLocal()
    main(db)
    logger.info("Finished updating groups attribute in keycloak with org_id.")
    db.close()
