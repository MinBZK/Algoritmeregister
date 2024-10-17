from app.services.keycloak import KeycloakRepository
from app.middleware import kc_settings


def migrate_roles():
    kc_repo = KeycloakRepository(kc_settings)
    # Use raw method to get all attributes
    users: list[dict] = kc_repo.client.get_users()  # type: ignore
    for user in users:
        user_id: str | None = user.get("id", None)
        if not user_id:
            print("email assignment failed for", user)
            continue
        if user.get("email", None):
            continue

        print(user.get("username", ""), user.get("email", "no email"))

        user["email"] = user["username"]
        try:
            kc_repo.client.update_user(user_id, user)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    migrate_roles()
