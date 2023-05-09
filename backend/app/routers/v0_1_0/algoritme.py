from fastapi import Depends, Path, FastAPI, APIRouter, BackgroundTasks, routing
from sqlalchemy.orm import Session
from app import schemas, models, middleware, controllers
from app.middleware.decorators import authorized_user_only, publisher_only, admin_only
from app.middleware.keycloak_authenticator import get_current_user
from app.config.api import api_text, responses

version = __name__.split(".")[-2]
input_schema = schemas.create_algorithm_in_schema(version)
output_schemas = schemas.get_all_output_schemas_union()

version_str = version[1:].replace("_", ".")
api = FastAPI(
    docs_url="/api-docs",
    title=f"Algoritmeregister aanlevering API, versie {version_str} ",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
    },
)

router = APIRouter()
published_router = APIRouter()
action_router = APIRouter()


@router.get(
    "/organizations/{organization_name}/algorithms",
    response_model=list[schemas.AlgorithmSummary],
    responses=responses["get_all"],
    summary=api_text["get_all"]["summary"],
    description=api_text["get_all"]["description"],
)
@authorized_user_only
async def get_all_algorithms(
    as_org: str = Path(alias="organization_name"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(middleware.get_current_user),
) -> list[schemas.AlgorithmSummary]:
    result = controllers.algoritme_version.get_all_newest(
        as_org=as_org,
        db=db,
        user=user,
    )
    return result


@router.get(
    "/organizations/{organization_name}/algorithms/{algorithm_id}",
    response_model=output_schemas | None,
    responses=responses["get_one"],
    summary=api_text["get_one"]["summary"],
    description=api_text["get_one"]["description"],
)
@authorized_user_only
async def get_one_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> models.AlgoritmeVersion:
    return controllers.algoritme_version.get_one_newest(lars=lars, db=db, user=user)


@router.post(
    "/organizations/{organization_name}/algorithms",
    response_model=schemas.NewAlgorithmResponse,
    responses=responses["post"],
    summary=api_text["post"]["summary"],
    description=api_text["post"]["description"],
)
@authorized_user_only
async def create_one_algorithm(
    body: input_schema,
    as_org: str = Path(alias="organization_name"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.NewAlgorithmResponse:
    # The standard_version can not be required, because it isn't according to BZK.
    if body.standard_version is None:  # type: ignore
        body.standard_version = version_str

    return controllers.algoritme_version.post_one(
        as_org=as_org, body=body, db=db, user=user
    )


@router.put(
    "/organizations/{organization_name}/algorithms/{algorithm_id}",
    responses=responses["put"],
    summary=api_text["put"]["summary"],
    description=api_text["put"]["description"],
)
@authorized_user_only
async def update_one_algorithm(
    body: input_schema,
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    # The standard_version can not be required, because it isn't according to BZK.
    if body.standard_version is None:  # type: ignore
        body.standard_version = version_str

    return controllers.algoritme_version.update_new_version(
        body=body, lars=lars, db=db, user=user
    )


@action_router.get(
    "/organizations/{organization_name}/algorithms/{algorithm_id}/preview",
    response_model=schemas.PreviewUrl,
    responses=responses["preview"],
    summary=api_text["preview"]["summary"],
    description=api_text["preview"]["description"],
)
@authorized_user_only
async def get_one_preview_url(
    background_tasks: BackgroundTasks,
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.PreviewUrl:
    background_tasks.add_task(
        controllers.algoritme_version.wait_then_disable_preview, lars=lars, db=db
    )
    return controllers.algoritme_version.get_preview_link(lars=lars, db=db, user=user)


@published_router.get(
    "/organizations/{organization_name}/published-algorithms/{algorithm_id}",
    response_model=output_schemas | None,
    responses=responses["get_one_published"],
    summary=api_text["get_one_published"]["summary"],
    description=api_text["get_one_published"]["description"],
)
@authorized_user_only
async def get_one_published_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> models.AlgoritmeVersion:
    return controllers.algoritme_version.get_one_published(lars=lars, db=db, user=user)


@action_router.delete(
    "/organizations/{organization_name}/published-algorithms/{algorithm_id}/retract",
    responses=responses["delete"],
    summary=api_text["delete"]["summary"],
    description=api_text["delete"]["description"],
)
@authorized_user_only
async def retract_one_published_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> None:
    return controllers.algoritme_version.retract_one(lars=lars, db=db, user=user)


@action_router.put(
    "/organizations/{organization_name}/algorithms/{algorithm_id}/release",
    responses=responses["release"],
    summary=api_text["release"]["summary"],
    description=api_text["release"]["description"],
)
@authorized_user_only
async def release_one_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    return controllers.algoritme_version.release_one(lars=lars, db=db, user=user)


@action_router.put(
    "/organizations/{organization_name}/algorithms/{algorithm_id}/publish",
    responses=responses["publish"],
    summary=api_text["publish"]["summary"],
    description=api_text["publish"]["description"],
)
@publisher_only
@authorized_user_only
async def publish_one_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    return controllers.algoritme_version.publish_one(lars=lars, db=db, user=user)


@action_router.delete(
    "/organizations/{organization_name}/algorithms/{algorithm_id}/remove",
    responses=responses["remove"],
    summary=api_text["remove"]["summary"],
    description=api_text["remove"]["description"],
    include_in_schema=False,
)
@admin_only
@authorized_user_only
async def remove_one_algorithm(
    as_org: str = Path(alias="organization_name"),
    lars: str = Path(alias="algorithm_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(get_current_user),
) -> schemas.AlgorithmActionResponse | None:
    return controllers.algoritme_version.remove_one(lars=lars, db=db, user=user)


api.include_router(router, tags=["Algoritmes in ontwikkeling"])
api.include_router(published_router, tags=["Gepubliceerde algoritmes"])
api.include_router(action_router, tags=["Acties"])

# Rename all the operation_id's  in the schema to the name of the corresponding route.
for route in api.routes:
    if isinstance(route, routing.APIRoute):
        route.operation_id = route.name
