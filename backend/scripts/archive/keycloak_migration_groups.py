from app.services.keycloak import KeycloakRepository
from app.middleware import kc_settings
from app.services.keycloak.schemas import KeycloakUserUpdate


def migrate_groups():
    kc_repo = KeycloakRepository(kc_settings)
    groups = kc_repo.get_groups()
    for n, group in enumerate(groups):
        print(group, f"progress: {n/len(groups)}")
        members = kc_repo.get_group_members(group.id)
        for member in members:
            groups = list(set([*member.groups, group.name]))
            kc_repo.update_user(member.id, KeycloakUserUpdate(groups=groups))
        # Optionally, remove the group. Doesn't hurt to keep it for now.
        # kc_repo.client.delete_group(group.id)


if __name__ == "__main__":
    migrate_groups()
