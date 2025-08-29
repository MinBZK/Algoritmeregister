from sqlalchemy.orm import Session
from app.middleware.authorisation.schemas import Role
from app.repositories.organisation_details import OrganisationDetailsRepository
from app.schemas.misc import Language
from app.schemas.user import GetUsersResponse, User
from app.services.keycloak.repository import KeycloakRepository

from app.middleware import kc_settings
from app.services.keycloak.schemas import (
    KeycloakUser,
    KeycloakUserFromRepo,
    KeycloakUserNew,
    KeycloakUserUpdate,
)


def get_user_from_keycloak_data(db: Session, keycloak_user: KeycloakUser) -> User:
    org_details_repo = OrganisationDetailsRepository(db)
    if Role.AllGroups in keycloak_user.roles:
        orgs = org_details_repo.get_org_configs_by_lang(Language.NLD)
    else:
        orgs = org_details_repo.get_org_configs_by_org_id_list_by_lang(
            keycloak_user.groups, Language.NLD
        )
    return User(**keycloak_user.model_dump(), organisations=orgs)


def get_all_users(
    db: Session,
    limit: int,
    skip: int,
    q: str | None,
    role: str | None = None,
    org: str | None = None,
) -> GetUsersResponse:
    kc_repo = KeycloakRepository(kc_settings)
    keycloak_users = kc_repo.get_all(limit=limit, skip=skip, role=role, group=org, q=q)
    users = get_from_keycloak_users(db, keycloak_users)
    count = kc_repo.get_count(limit=limit, skip=skip, role=role, group=org, q=q)

    return GetUsersResponse(users=users, count=count)


def get_from_keycloak_users(
    db: Session, keycloak_users: list[KeycloakUserFromRepo]
) -> list[User]:
    # Collects all the group names so only 1 DB call is needed.
    all_group_codes = []
    for user in keycloak_users:
        all_group_codes.extend(user.groups)
    all_group_codes = list(set(all_group_codes))

    org_repo = OrganisationDetailsRepository(db)
    includes_all_groups_user = any(Role.AllGroups in u.roles for u in keycloak_users)
    if includes_all_groups_user:
        all_groups = org_repo.get_org_configs_by_lang(Language.NLD)
    else:
        all_groups = org_repo.get_org_configs_by_org_id_list_by_lang(
            all_group_codes, Language.NLD
        )

    users: list[User] = []
    for user in keycloak_users:
        groups_for_this_user = [
            g for g in all_groups if g.code in user.groups or g.org_id in user.groups
        ]
        users.append(User(**user.model_dump(), organisations=groups_for_this_user))
    return users


def get_from_keycloak_user(db: Session, keycloak_user: KeycloakUser) -> User:
    if Role.AllGroups in keycloak_user.roles:
        groups = OrganisationDetailsRepository(db).get_org_configs_by_lang(Language.NLD)
    else:
        groups = OrganisationDetailsRepository(
            db
        ).get_org_configs_by_org_id_list_by_lang(keycloak_user.groups, Language.NLD)
    return User(**keycloak_user.model_dump(), organisations=groups)


def create_user(db: Session, body: KeycloakUserNew) -> User:
    kc_repo = KeycloakRepository(kc_settings)
    new_keycloak_user = kc_repo.create_user(body)
    return get_user_from_keycloak_data(db, new_keycloak_user)


def get_user(db: Session, user_id: str) -> User:
    kc_repo = KeycloakRepository(kc_settings)
    keycloak_user = kc_repo.get_user(user_id)
    return get_user_from_keycloak_data(db, keycloak_user)


def update_user(db: Session, user_id: str, body: KeycloakUserUpdate) -> User:
    kc_repo = KeycloakRepository(kc_settings)
    keycloak_user = kc_repo.update_user(user_id, body)
    return get_user_from_keycloak_data(db, keycloak_user)


def delete_user(user_id: str) -> None:
    kc_repo = KeycloakRepository(kc_settings)
    kc_repo.delete_user(user_id)
