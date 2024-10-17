from app.middleware.authorisation.schemas import Role
from app.services.keycloak import KeycloakRepository
from app.middleware import kc_settings


def migrate_roles():
    kc_repo = KeycloakRepository(kc_settings)
    # Use raw method to get all attributes
    users: list[dict] = kc_repo.client.get_users()  # type: ignore
    for user in users:
        print(user.get("username", ""))

        user_id: str | None = user.get("id", None)
        old_role = user.get("attributes", {}).get("role", None)
        if not user_id:
            print("role assignment failed for", user)
            continue

        # Manually handle update because we want to preserve the attribute role as well as roles.
        attributes = user.get("attributes", {})

        # Add role from 'role' attribute to 'roles' attribute, make them a unique set.
        new_roles = [*attributes.get("roles", []), "orgdetail", "role_1"]
        try:
            # Add the old role if it is a legitimate current role
            if old_role:
                Role(old_role[0])
                new_roles = [*old_role, *new_roles]
        except ValueError:
            pass

        # Users get orgdetail and role_1 by default, to mirror current rights of users.
        attributes["roles"] = list(set(new_roles))

        user["attributes"] = attributes
        kc_repo.client.update_user(user_id, user)


if __name__ == "__main__":
    migrate_roles()
