from typing import Annotated
from fastapi import BackgroundTasks, Depends, APIRouter, Path, Query
from sqlalchemy.orm import Session
from app.controllers import remove_org, get_alternative_values_from_columns
from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.authorisation.schemas import Role
from app.middleware.keycloak_authenticator import get_current_user
from app.middleware.middleware import get_db
from app.schemas.flow import FlowStructure
from app.schemas.organization import (
    GetOrganisationsResponse,
    OrganisationConfig,
    OrganisationConfigIn,
)
from app.controllers import flow as flow_controller
from app.services.keycloak import KeycloakUser
from app.controllers import get_orgs, create_org, update_org, update_org_show_page

router = APIRouter()


@router.get(
    "/organisation",
    response_model=GetOrganisationsResponse,
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_all_orgs(
    db: Session = Depends(get_db),
    user: KeycloakUser = Depends(get_current_user),
    limit: int = Query(ge=1, le=10000, default=10000),
    skip: int = Query(ge=0, default=0),
    q: str | None = Query(max_length=50, default=None),
):
    return get_orgs(db, user=user, limit=limit, skip=skip, q=q)


@router.post(
    "/organisation",
    response_model=OrganisationConfig,
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator))],
)
async def post_org(
    background_tasks: BackgroundTasks,
    body: OrganisationConfigIn,
    db: Session = Depends(get_db),
) -> OrganisationConfig:
    return create_org(background_tasks, db, body)


@router.put(
    "/organisation/{organisation_id}",
    response_model=OrganisationConfig,
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator))],
)
async def put_org(
    background_tasks: BackgroundTasks,
    body: OrganisationConfigIn,
    as_org: str = Path(alias="organisation_id"),
    db: Session = Depends(get_db),
) -> OrganisationConfig:
    return update_org(background_tasks, db, as_org, body)


@router.delete(
    "/organisation/{organisation_id}",
    response_model=None,
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator))],
)
async def delete_org(
    as_org: str = Path(alias="organisation_id"),
    db: Session = Depends(get_db),
) -> None:
    return remove_org(db, as_org)


@router.put(
    "/organisation/{organisation_id}/show_page/{change_to}",
    response_model=OrganisationConfig,
    dependencies=[Depends(Authoriser(AuthType.OrgRole, role=Role.OrgDetail))],
)
async def put_org_show_page(
    as_org: str = Path(alias="organisation_id"),
    show_page: bool = Path(alias="change_to"),
    db: Session = Depends(get_db),
) -> OrganisationConfig:
    return update_org_show_page(db, as_org, show_page)


@router.get(
    "/organisation/{organisation_id}/flow",
    dependencies=[Depends(Authoriser(AuthType.OrgRole, role=Role.Administrator))],
)
async def get_one_flow(
    db: Annotated[Session, Depends(get_db)],
    as_org: str = Path(alias="organisation_id"),
) -> FlowStructure:
    return flow_controller.get_one(db, as_org)


@router.get(
    "/organisation/{organisation_name}/altnames",
    dependencies=[Depends(Authoriser(AuthType.OrgRole, role=Role.Administrator))],
)
async def get_alt_names(
    db: Annotated[Session, Depends(get_db)],
    as_org: str = Path(alias="organisation_name"),
) -> list[str]:
    return get_alternative_values_from_columns(db, as_org)
