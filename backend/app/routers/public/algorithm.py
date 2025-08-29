from fastapi import APIRouter, HTTPException, status, Depends, Path, BackgroundTasks
from sqlalchemy import desc, text
from sqlalchemy.orm import Session
from app import models, schemas, controllers
from app.config.settings import Settings
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from app.schemas.misc import Language
from app.services.algoritme_version import db_list_to_python_list
from app.controllers.smart_search import perform_smart_search, perform_suggestion_search
from app.controllers.vector_search import search_similar
from app.controllers.precomputed_values import calc_highlighted_algorithms
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
    "/algoritme/{language}/similar/{lars}",
    response_model=schemas.AlgoritmeSimilarQueryResponse,
)
async def get_similar(
    lars: str,
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> schemas.AlgoritmeSimilarQueryResponse:
    return search_similar(
        lars,
        db,
        language,
        model=models.AlgoritmeVersion.embedding_nfi,
        min_score=45,
    )


@router.get(
    "/suggestion/{language}/{search}", response_model=schemas.SearchSuggestionResponse
)
async def get_search_suggestion(
    search: str = "",
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> schemas.SearchSuggestionResponse:
    return perform_suggestion_search(search, db, language)


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
    return schemas.AlgoritmeVersionDB.model_validate(result)


@router.get(
    "/highlighted/{language}",
    response_model=list[schemas.HighlightedAlgorithmResponse],
)
async def get_highlighted(
    db: Session = Depends(get_db), language: Language = Path(alias="language")
) -> list[schemas.HighlightedAlgorithmResponse]:
    return calc_highlighted_algorithms(db, language)
