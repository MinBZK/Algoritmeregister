from sqlalchemy import text
from fastapi import BackgroundTasks, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from app import schemas
from app.controllers.action import get_available_actions_by_lars, update_state_by_lars
from app.controllers.algoritme import (
    get_archived_versions,
    get_algoritme_owner,
    get_algoritme_versions_by_id,
)
from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.authorisation.require_ownership import RequireOwnership
from app.middleware.authorisation.schemas import Permission
from app.middleware.keycloak_authenticator import get_current_user
from app.middleware.middleware import get_db
from app.schemas.action import (
    StateChangeActionOut,
)
from app.services.keycloak import KeycloakUser


router = APIRouter()


@router.get(
    "/organisations/{organisation_id}/algorithms/archived-versions",
    response_model=list[schemas.AlgoritmeVersionLastEdit],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.PUT_ALGORITHM_VERSION
            )
        ),
    ],
)
async def get_archived_algorithm_versions(
    organisation_id: str,
    db: Session = Depends(get_db),
):
    return get_archived_versions(db, organisation_id)


@router.get(
    "/algoritme/find/{algoritme_id}",
    response_model=schemas.OrganisationIn,
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def find_algoritme_owner(
    lars: str = Path(alias="algoritme_id"),
    db: Session = Depends(get_db),
    user: KeycloakUser = Depends(get_current_user),
):
    return get_algoritme_owner(db, user, lars)


@router.get(
    "/organisations/{organisation_id}/algorithms/{algorithm_id}/versions",
    response_model=list[schemas.AlgoritmeVersionLastEdit],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.GET_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def get_all_versions(
    lars: str = Path(alias="algorithm_id"),
    include_archived: bool = False,
    db: Session = Depends(get_db),
):
    return get_algoritme_versions_by_id(db, lars, include_archived)


@router.get(
    "/organisations/{organisation_id}/algorithms/{algorithm_id}/available-actions",
    response_model=list[StateChangeActionOut],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.GET_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def get_available_actions(
    lars: str = Path(alias="algorithm_id"),
    _: str = Path(alias="organisation_id"),
    user: KeycloakUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_available_actions_by_lars(db, user, lars)


@router.put(
    "/organisations/{organisation_id}/algorithms/{algorithm_id}/state/{action_name}",
    response_model=None,
    dependencies=[
        Depends(Authoriser(AuthType.OrgRightStateChange)),
        Depends(RequireOwnership),
    ],
)
async def update_state(
    background_tasks: BackgroundTasks,
    lars: str = Path(alias="algorithm_id"),
    as_org: str = Path(alias="organisation_id"),
    action_name: str = Path(alias="action_name"),
    user: KeycloakUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_state_by_lars(
        db=db,
        user=user,
        lars=lars,
        as_org=as_org,
        action_key=action_name,
        background_tasks=background_tasks,
    )


@router.get(
    "/algoritme/total-count", dependencies=[Depends(Authoriser(AuthType.BaseOnly))]
)
async def get_total_count(db: Session = Depends(get_db)) -> int:
    stmt = "SELECT count(id) FROM algoritme_version WHERE state = 'PUBLISHED' AND language='NLD'"
    return db.execute(text(stmt)).scalar_one()
