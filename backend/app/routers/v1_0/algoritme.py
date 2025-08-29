from typing import Annotated
from fastapi import Depends, Path, FastAPI, APIRouter, BackgroundTasks, routing
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from app import schemas, controllers
from app.controllers.action import update_state_by_lars
from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.authorisation.require_ownership import RequireOwnership
from app.middleware.authorisation.schemas import Permission, Role
from app.middleware.keycloak_authenticator import get_current_user
from app.config.api import api_text, responses
from app.middleware.middleware import get_db
from app.services.keycloak import KeycloakUser

version = __name__.split(".")[-2]
input_schema = schemas.create_algorithm_in_schema(version)
output_schemas = schemas.get_all_output_schemas_union()

version_str = version[1:].replace("_", ".")
deprecation_notice = """
<h3>⚠️ Belangrijke mededeling</h3>
De API versies 0.1.0,  0.4.0 en 1.0.0 worden voortaan verkort naar respectievelijk 0.1, 0.4 en 1.0.
<br>
Grebruik in de API URLs dus aanleverapi/<b>v0_1</b>, aanleverapi/<b>v0_4</b> en aanleverapi/<b>v1_0</b>.
"""
api = FastAPI(
    docs_url="/api-docs",
    title=f"Algoritmeregister aanlevering API, versie {version_str} ",
    description=deprecation_notice,
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
    },
)
limiter = Limiter(key_func=get_remote_address, default_limits=["25/minute"])
api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
api.add_middleware(SlowAPIMiddleware)

router = APIRouter()
published_router = APIRouter()
action_router = APIRouter()


@router.get(
    "/organizations/{organisation_id}/algorithms",
    response_model=list[schemas.AlgorithmSummary],
    responses=responses["get_all"],
    summary=api_text["get_all"]["summary"],
    description=api_text["get_all"]["description"],
    dependencies=[Depends(Authoriser(AuthType.OrgOnly))],
)
async def get_all_algorithms(
    db: Annotated[Session, Depends(get_db)],
    _: str = Path(alias="organisation_id"),
    as_org: str = Path(alias="organisation_id"),
) -> list[schemas.AlgorithmSummary]:
    result = controllers.algoritme_version.get_algorithm_summary(
        as_org=as_org,
        db=db,
    )
    return result


@router.get(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}",
    response_model=output_schemas | None,
    responses=responses["get_one"],
    summary=api_text["get_one"]["summary"],
    description=api_text["get_one"]["description"],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.GET_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def get_one_algorithm(
    db: Annotated[Session, Depends(get_db)],
    _: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
) -> schemas.AlgoritmeVersionDB:
    return controllers.algoritme_version.get_one_newest(lars=lars, db=db)


@router.post(
    "/organizations/{organisation_id}/algorithms",
    response_model=schemas.NewAlgorithmResponse,
    responses=responses["post"],
    summary=api_text["post"]["summary"],
    description=api_text["post"]["description"],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.POST_ALGORITHM_VERSION
            )
        ),
    ],
)
async def create_one_algorithm(
    db: Annotated[Session, Depends(get_db)],
    body: input_schema,  # type: ignore
    _: str = Path(alias="organisation_id"),
    as_org: str = Path(alias="organisation_id"),
    user: KeycloakUser = Depends(get_current_user),
) -> schemas.NewAlgorithmResponse:
    # The standard_version can not be required, because it isn't according to BZK.
    if body.standard_version is None:  # type: ignore
        body.standard_version = version_str

    algoritme_version = schemas.AlgoritmeVersionContent(**body.dict())
    return controllers.algoritme_version.post_one(
        as_org=as_org, body=algoritme_version, db=db, user=user
    )


@router.put(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}",
    responses=responses["put"],
    summary=api_text["put"]["summary"],
    description=api_text["put"]["description"],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.PUT_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def update_one_algorithm(
    db: Annotated[Session, Depends(get_db)],
    body: input_schema,  # type: ignore
    _: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    algoritme_version = schemas.AlgoritmeVersionContent(**body.dict())
    return controllers.algoritme_version.update_new_version(
        body=algoritme_version, lars=lars, db=db, user=user
    )


@action_router.get(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/preview",
    response_model=schemas.PreviewUrl,
    responses=responses["preview"],
    summary=api_text["preview"]["summary"],
    description=api_text["preview"]["description"],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.GET_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def get_one_preview_url(
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
    _: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
) -> schemas.PreviewUrl:
    background_tasks.add_task(
        controllers.algoritme_version.wait_then_disable_preview, lars=lars, db=db
    )
    return controllers.algoritme_version.get_preview_link(lars=lars, db=db, user=user)


@published_router.get(
    "/organizations/{organisation_id}/published-algorithms/{algorithm_id}",
    response_model=output_schemas | None,
    responses=responses["get_one_published"],
    summary=api_text["get_one_published"]["summary"],
    description=api_text["get_one_published"]["description"],
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.GET_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def get_one_published_algorithm(
    db: Annotated[Session, Depends(get_db)],
    _: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
) -> schemas.AlgoritmeVersionDB:
    return controllers.algoritme_version.get_one_published(lars=lars, db=db)


@action_router.delete(
    "/organizations/{organisation_id}/published-algorithms/{algorithm_id}/retract",
    responses=responses["delete"],
    summary=api_text["delete"]["summary"],
    description=api_text["delete"]["description"],
    dependencies=[
        Depends(
            Authoriser(AuthType.OrgRightStateChange, legacy_action_key="retract"),
        ),
        Depends(RequireOwnership),
    ],
)
async def retract_one_published_algorithm(
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
    as_org: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
) -> None:
    """
    Legacy endpoint, to be used only by ictu_last flows.
    Equal to moving from PUBLISHED TO STATE_1.
    """
    response = update_state_by_lars(
        db=db,
        user=user,
        lars=lars,
        as_org=as_org,
        action_key="retract",
        background_tasks=background_tasks,
    )
    return response


@action_router.put(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/release",
    responses=responses["release"],
    summary=api_text["release"]["summary"],
    description=api_text["release"]["description"],
    dependencies=[
        Depends(
            Authoriser(AuthType.OrgRightStateChange, legacy_action_key="release"),
        ),
        Depends(RequireOwnership),
    ],
)
async def release_one_algorithm(
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
    as_org: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    """
    Legacy endpoint, to be used only by ictu_last flows.
    Equal to moving from STATE_1 to STATE_2.
    """
    response = update_state_by_lars(
        db=db,
        user=user,
        lars=lars,
        as_org=as_org,
        action_key="release",
        background_tasks=background_tasks,
    )
    return response


@action_router.put(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/publish",
    responses=responses["publish"],
    summary=api_text["publish"]["summary"],
    description=api_text["publish"]["description"],
    include_in_schema=False,
    dependencies=[
        Depends(Authoriser(AuthType.OrgRightStateChange, legacy_action_key="publish")),
        Depends(RequireOwnership),
    ],
)
async def publish_one_algorithm(
    background_tasks: BackgroundTasks,
    lars: str = Path(alias="algorithm_id"),
    as_org: str = Path(alias="organisation_id"),
    db: Session = Depends(get_db),
    user: KeycloakUser = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    """
    Legacy endpoint, to be used only by ictu_last flows.
    Equal to moving from STATE_2 to PUBLISHED.
    """
    return update_state_by_lars(
        db=db,
        user=user,
        lars=lars,
        action_key="publish",
        as_org=as_org,
        background_tasks=background_tasks,
    )


@action_router.delete(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/remove",
    responses=responses["remove"],
    summary=api_text["remove"]["summary"],
    description=api_text["remove"]["description"],
    include_in_schema=False,
    dependencies=[
        Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator)),
        Depends(RequireOwnership),
    ],
)
async def remove_one_algorithm(
    db: Annotated[Session, Depends(get_db)],
    _: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
) -> schemas.AlgorithmActionResponse | None:
    return controllers.algoritme_version.remove_one(lars=lars, db=db)


@router.put(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/archive_version",
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.PUT_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def archive_algorithm_version(
    archive_request: schemas.ArchiveVersionRequest,
    as_org: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    return controllers.algoritme_version.set_archive_status(
        version_id=archive_request.algorithm_version_id,
        db=db,
        archived=True,
        user_id=user.username,
    )


@router.put(
    "/organizations/{organisation_id}/algorithms/{algorithm_id}/unarchive_version",
    dependencies=[
        Depends(
            Authoriser(
                AuthType.OrgPermission, permission=Permission.PUT_ALGORITHM_VERSION
            )
        ),
        Depends(RequireOwnership),
    ],
)
async def unarchive_algorithm_version(
    archive_request: schemas.ArchiveVersionRequest,
    as_org: str = Path(alias="organisation_id"),
    lars: str = Path(alias="algorithm_id"),
    user: KeycloakUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    return controllers.algoritme_version.set_archive_status(
        version_id=archive_request.algorithm_version_id,
        db=db,
        archived=False,
        user_id=user.username,
    )


api.include_router(router, tags=["Algoritmes in ontwikkeling"])
api.include_router(published_router, tags=["Gepubliceerde algoritmes"])
api.include_router(action_router, tags=["Acties"])

# Rename all the operation_id's  in the schema to the name of the corresponding route.
for route in api.routes:
    if isinstance(route, routing.APIRoute):
        route.operation_id = route.name
