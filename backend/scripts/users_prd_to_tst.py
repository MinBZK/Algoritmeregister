from hashlib import md5
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
)
from app.services.keycloak.repository import KeycloakRepository
from app.middleware import kc_settings
from app.services.keycloak.repository import ConnectionSettings
from app.services.keycloak.schemas import KeycloakUserFromRepo
from app.util.logger import get_logger


class KeycloakPRDSettings(BaseSettings):
    KEYCLOAK_REALM_PRD: str = Field(default="algreg")
    KEYCLOAK_API_URI_PRD: str = Field(default="")
    KEYCLOAK_API_CLIENT_PRD: str = Field(default="service-client")
    KEYCLOAK_API_SECRET_PRD: str = Field(default="")


env_prd_settings = KeycloakPRDSettings()

kc_settings_prd: ConnectionSettings = {
    "realm_name": env_prd_settings.KEYCLOAK_REALM_PRD,
    "server_url": env_prd_settings.KEYCLOAK_API_URI_PRD,
    "client_id": env_prd_settings.KEYCLOAK_API_CLIENT_PRD,
    "client_secret_key": env_prd_settings.KEYCLOAK_API_SECRET_PRD,
}

logger = get_logger(__name__)


def jumble_email(email: str) -> str | None:
    """
    Returns anonymous version of email. Must contain an @.
    """
    try:
        if not "@" in email:
            logger.error(f"Can't jumble {email}, not an e-mailadres. (MISSING AT SIGN)")
            return
        username, domain = email.split("@")

        if not "." in domain:
            logger.error(f"Can't jumble {email}, not an e-mailadres. (MISSING PERIOD)")
            return
        domain_name, domain_extension = domain.split(".")
    except Exception as e:
        logger.error(f"Can't jumble {email}, not an e-mailadres. (UNKNOWN)")
        return

    hashed_username = md5(username.encode()).hexdigest()
    hashed_domain = md5(domain_name.encode()).hexdigest()
    return f"fake-{hashed_username}@{hashed_domain}.{domain_extension}"


def create_old_user(kc_repo: KeycloakRepository, user: KeycloakUserFromRepo) -> None:
    """
    Creates a regular user, with an old timestamp
    """
    payload = {
        "username": user.username,
        "attributes": {"groups": user.groups or [], "roles": user.roles or []},
        "enabled": True,
        "firstName": "Not available",
        "lastName": "Not available",
        "emailVerified": True,
        "createdTimestamp": int(user.created_at.timestamp() * 1000),
    }
    logger.info(f"Creating user {user.username}")
    kc_repo.client.create_user(payload)


def main():
    """
    Retrieves user accounts from PRD and inserts them in the TST environment.
    Personal information is hashed or removed. The hash is used to ensure that accounts
    don't get posted on TST twice.
    """

    kc_repo_prd = KeycloakRepository(kc_settings_prd)
    prd_users = kc_repo_prd.get_all()
    kc_repo_tst = KeycloakRepository(kc_settings)
    tst_users = kc_repo_tst.get_all()

    # Email and username is the same.
    current_emails = [u.username for u in tst_users]
    for user in prd_users:
        # if user.username.startswith("fake-"):
        #     continue

        if not (new_email := jumble_email(user.username)):
            continue

        if new_email in current_emails:
            logger.info("This fake account already exists.")
            continue
        user.username = new_email
        create_old_user(kc_repo_tst, user)


if __name__ == "__main__":
    main()
