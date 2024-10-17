from app.services.keycloak.repository import KeycloakRepository

from app.middleware import kc_settings
from etl.logger import get_logger

logger = get_logger()


def remove_all_fake_accounts():
    kc_repo_tst = KeycloakRepository(kc_settings)
    users = kc_repo_tst.get_all(q="fake-")
    for user in users:
        logger.info(f"Deleting user {user.username}")
        kc_repo_tst.delete_user(user.id)


if __name__ == "__main__":
    remove_all_fake_accounts()
