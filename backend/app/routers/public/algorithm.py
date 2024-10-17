from fastapi import APIRouter, HTTPException, status, Depends, Path, BackgroundTasks
from sqlalchemy import and_, func, desc, text
from sqlalchemy.orm import Session
from app.config.settings import Settings
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from app import repositories
from app.schemas.misc import Language
from app.schemas.organization import OrganisationMappingResult
from app.services.algoritme_version import db_list_to_python_list
from app import models, schemas, controllers
from app.controllers.smart_search import perform_smart_search, perform_suggestion_search
from app.config.org_name_mapping import org_name_mapping
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
env_settings = Settings()


@router.get("/algoritme/total-count")
async def get_total_count(db: Session = Depends(get_db)) -> int:
    stmt = "SELECT count(id) FROM algoritme_version WHERE state = 'PUBLISHED' AND language='NLD'"
    return db.execute(text(stmt)).scalar_one()


@router.post(
    "/algoritme/{language}",
    response_model=schemas.AlgoritmeQueryResponse,
)
async def get_all(
    algoritme_query: schemas.algoritme_version.AlgoritmeQuery,
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> schemas.AlgoritmeQueryResponse:
    return perform_smart_search(algoritme_query, db, language)


@router.get(
    "/suggestion/{language}/{search}", response_model=schemas.SearchSuggestionResponse
)
async def get_search_suggestion(
    search: str = "",
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> schemas.SearchSuggestionResponse:
    return perform_suggestion_search(search, db, language)


@router.get("/organisation/{language}/{search}")
async def get_elaborate_organisation(
    search: str = "",
    language: Language = Path(alias="language"),
    db: Session = Depends(get_db),
) -> schemas.OrganisationSearchSuggestionResponse | None:
    org_repo = repositories.OrganisationRepository(db)
    results = org_repo.get_overview_by_lang(language)
    organisation_details = [
        schemas.OrganisationMappingResult(code=result.code, name=result.name)
        for result in results
        if search.lower() in result.name.lower()
    ]
    results_from_mapping = org_name_mapping.get(language, {}).get(search.lower(), {})

    if results_from_mapping:
        mapped_org = OrganisationMappingResult(**results_from_mapping)
        return schemas.OrganisationSearchSuggestionResponse(organisations=[mapped_org])
    elif organisation_details:
        return schemas.OrganisationSearchSuggestionResponse(
            organisations=organisation_details
        )


@router.get(
    "/algoritme/{language}/{lars}",
    response_model=schemas.AlgoritmeVersionGetOne | None,
)
async def get_one(
    lars: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
):
    if lars[0] == "C":
        result = (
            db.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars[1:],
                models.AlgoritmeVersion.preview_active,
                models.AlgoritmeVersion.language == language,
            )
            .first()
        )

        background_tasks.add_task(
            controllers.disable_preview,
            lars=lars[1:],
            db=db,
            user="anonymous website visitor",
            reason=schemas.OperationEnum.preview_used,
        )
    else:
        result = (
            db.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.state == State.PUBLISHED,
                models.AlgoritmeVersion.language == language,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .first()
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kan algoritme niet vinden.",
        )

    result = db_list_to_python_list(result)
    return schemas.AlgoritmeVersionDB.from_orm(result)


@router.get(
    "/highlighted/{language}",
    response_model=list[schemas.HighlightedAlgorithmResponse],
)
async def get_highlighted(
    db: Session = Depends(get_db), language: Language = Path(alias="language")
) -> list[schemas.HighlightedAlgorithmResponse]:
    latest_upload_owner = (
        db.query(
            models.Algoritme.organisation_id,
            func.max(models.AlgoritmeVersion.create_dt).label("max_creation_dt"),
        )
        .join(
            models.Algoritme,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(
            models.AlgoritmeVersion.state == State.PUBLISHED,
            models.AlgoritmeVersion.language == language,
        )
        .group_by(models.Algoritme.organisation_id)
        .subquery()
    )

    latest_algo_owner = (
        db.query(models.AlgoritmeVersion)
        .join(
            latest_upload_owner,
            and_(
                latest_upload_owner.c.max_creation_dt
                == models.AlgoritmeVersion.create_dt
            ),
        )
        .filter(models.AlgoritmeVersion.language == language)
        .order_by(desc(models.AlgoritmeVersion.create_dt))
        .limit(3)
        .all()
    )
    for n, _ in enumerate(latest_algo_owner):
        latest_algo_owner[n] = db_list_to_python_list(latest_algo_owner[n])
    return [
        schemas.HighlightedAlgorithmResponse.from_orm(alg) for alg in latest_algo_owner
    ]
