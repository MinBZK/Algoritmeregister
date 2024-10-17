from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.controllers.user import get_from_keycloak_users
from app.middleware.authorisation.config._base import load_flow_configurations
from app.middleware.authorisation.schemas import Role
from app.repositories.organisation import OrganisationRepository
from app.schemas.flow import FlowStructure, FlowStructureRole
from app.services.keycloak.repository import KeycloakRepository
from app.middleware import kc_settings


def get_one(db: Session, org_code: str) -> FlowStructure:
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_code(org_code)
    if not org:
        raise HTTPException(404)

    flow = load_flow_configurations()[org.flow]

    # Gets all users and groups them by roles.
    kc_repo = KeycloakRepository(kc_settings)
    keycloak_users = kc_repo.get_all(group=org_code)
    # Users that have access to all groups are added.
    keycloak_users_all_groups = kc_repo.get_all(role=Role.AllGroups)
    users = get_from_keycloak_users(db, [*keycloak_users, *keycloak_users_all_groups])
    roles: list[FlowStructureRole] = []
    for role in flow["role_label_mapping"]:
        members = [u for u in users if role in u.roles]
        role_structure = FlowStructureRole(
            key=role,
            alias=flow["role_label_mapping"][role],
            min_required=1,
            members=members,
        )
        roles.append(role_structure)
    return FlowStructure(key=org.flow, alias=flow["alias"], roles=roles)
