import io
import json
import logging
import pandas as pd
from fastapi import APIRouter, HTTPException, status, Depends, Path, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy import and_, func, desc
from sqlalchemy.orm import Session
from app.config.settings import Settings
from app.middleware.middleware import get_db
from app.services.algoritme_version import db_list_to_python_list
from app import models, schemas, controllers
from app.controllers.smart_search import perform_smart_search, perform_suggestion_search

router = APIRouter()
logger = logging.getLogger(__name__)

env_settings = Settings()


# 'Get' version of the endpoint, but does not appear to work with frontend.
# @router.get(
#     "/algoritme/",
#     response_model=schemas.AlgoritmeQueryResponse,
# )
# async def get_all(
#     searchtext: str | None = None,
#     organisation: str | None = None,
#     page: int = 1,
#     limit: int = 10,
#     db: Session = Depends(get_db),
# ) -> schemas.AlgoritmeQueryResponse:


@router.post(
    "/algoritme/{language}",
    response_model=schemas.AlgoritmeQueryResponse,
)
async def get_all(
    algoritme_query: schemas.algoritme_version.AlgoritmeQuery,
    db: Session = Depends(get_db),
    language: schemas.Language = Path(alias="language"),
) -> schemas.AlgoritmeQueryResponse:
    return perform_smart_search(algoritme_query, db, language)


@router.get(
    "/suggestion/{language}/{search}", response_model=schemas.SearchSuggestionResponse
)
async def get_search_suggestion(
    search: str = "",
    db: Session = Depends(get_db),
    language: schemas.Language = Path(alias="language"),
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
    language: schemas.Language = Path(alias="language"),
):
    if lars[0] == "C":
        result = (
            db.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.lars == lars[1:],
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
            .filter(
                models.AlgoritmeVersion.lars == lars,
                models.AlgoritmeVersion.published,
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

    result = schemas.AlgoritmeVersionDB.from_orm(result)
    return result


@router.get(
    "/highlighted/{language}",
    response_model=list[schemas.HighlightedAlgorithmResponse],
)
async def get_highlighted(
    db: Session = Depends(get_db), language: schemas.Language = Path(alias="language")
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
            models.AlgoritmeVersion.published,
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


json_schema = schemas.get_algorithm_export_schema(truncated=False)


@router.get(
    "/json/algoritme",
    response_model=list[json_schema],
)
async def export_algoritme_json(db: Session = Depends(get_db)):
    result = (
        db.query(models.algoritme_version.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.published)
        .order_by(models.AlgoritmeVersion.algoritme_id)
        .all()
    )

    if len(result) == 0:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="DATA_NOT_FOUND")

    data = [json_schema.from_orm(r).dict() for r in result]
    df = pd.DataFrame(data)
    if len(df.index) > 0:
        df["create_dt"] = df["create_dt"].astype(str)

        df = df[(df["owner"] != "sandbox")]

    data_out = df.to_dict(orient="records")

    stream = io.BytesIO()
    stream.write(json.dumps(data_out).encode())
    response = StreamingResponse(iter([stream.getvalue()]), media_type="json")

    response.headers["Content-Disposition"] = "attachment; filename=pub_data.json"

    return response


@router.get("/sitemap-urls")
async def get_sitemap_urls(db: Session = Depends(get_db)):
    algorithms_nl = (
        db.query(models.Algoritme)
        .join(
            models.AlgoritmeVersion,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(models.AlgoritmeVersion.language == schemas.Language.NLD)
        .order_by(models.Algoritme.lars)
        .all()
    )

    result_dict = []
    for algorithm in algorithms_nl:
        algo_dict = {
            "loc": "/nl/algoritme/" + algorithm.lars,
            "lastmod": algorithm.create_dt,
            "changefreq": "daily",
        }
        result_dict.append(algo_dict)

    algorithms_en = (
        db.query(models.Algoritme)
        .join(
            models.AlgoritmeVersion,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(models.AlgoritmeVersion.language == schemas.Language.ENG)
        .order_by(models.Algoritme.lars)
        .all()
    )
    for algorithm in algorithms_en:
        algo_dict = {
            "loc": "/en/algoritme/" + algorithm.lars,
            "lastmod": algorithm.create_dt,
            "changefreq": "daily",
        }
        result_dict.append(algo_dict)

    return result_dict
