import io
import json
from typing import Literal

from fastapi import APIRouter, Path, Depends, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from app import schemas

from app.controllers import generate_download_file
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.repositories.organisation_details import OrganisationDetailsRepository
from app.schemas.misc import Language

router = APIRouter()


@router.get(
    "/downloads/{language}",
    response_class=FileResponse,
)
async def get_file_all(
    db: Session = Depends(get_db),
    lang: Language = Path(alias="language"),
    filetype: Literal["excel", "csv"] = Query(alias="filetype"),
):
    if filetype not in ["excel", "csv"]:
        raise HTTPException(
            status_code=400,
            detail="Filetype must be excel or csv",
        )
    return generate_download_file(
        db, lang, which_version="published", file_type=filetype
    )


@router.get(
    "/downloads/history/{language}",
    response_class=FileResponse,
)
async def get_file_all_published_history(
    db: Session = Depends(get_db),
    lang: Language = Path(alias="language"),
    filetype: Literal["excel", "csv"] = Query(alias="filetype"),
):
    if filetype not in ["excel", "csv"]:
        raise HTTPException(
            status_code=400,
            detail="Filetype must be excel or csv",
        )
    return generate_download_file(
        db, lang, which_version="published_history", file_type=filetype
    )


@router.get(
    "/downloads/algorithms/{algorithm_id}/{language}",
    response_class=FileResponse,
)
async def get_file_one(
    db: Session = Depends(get_db),
    lars: str = Path(alias="algorithm_id"),
    lang: Language = Path(alias="language"),
    filetype: Literal["excel", "csv"] = Query(alias="filetype"),
):
    if filetype not in ["excel", "csv"]:
        raise HTTPException(
            status_code=400,
            detail="Filetype must be excel or csv",
        )
    return generate_download_file(
        db, lang, lars=lars, which_version="published", file_type=filetype
    )


@router.get(
    "/downloads/history/algorithms/{algorithm_id}/{language}",
    response_class=FileResponse,
)
async def get_file_one_published_history(
    db: Session = Depends(get_db),
    lars: str = Path(alias="algorithm_id"),
    lang: Language = Path(alias="language"),
    filetype: Literal["excel", "csv"] = Query(alias="filetype"),
):
    if filetype not in ["excel", "csv"]:
        raise HTTPException(
            status_code=400,
            detail="Filetype must be excel or csv",
        )
    return generate_download_file(
        db, lang, lars=lars, which_version="published_history", file_type=filetype
    )


@router.get(
    "/downloads/site-data/json",
    response_model=schemas.SiteData,
)
async def export_site_data_json(db: Session = Depends(get_db)):
    org_details_repo = OrganisationDetailsRepository(db)
    algo_version_repo = AlgoritmeVersionRepository(db)

    algos = algo_version_repo.get_all_published()
    parsed_algos = [
        schemas.AlgoritmeVersionExport(**dict(algo))
        for algo in algos
        if algo.owner != "sandbox"
    ]
    published_owners = list(
        set([algo.owner for algo in algos if algo.state == State.PUBLISHED])
    )

    org_details = org_details_repo.get_all()
    parsed_org_details = []
    for org_detail in org_details:
        if org_detail.code == "sandbox":
            continue
        if org_detail.org_id not in published_owners:
            continue
        if not org_detail.show_page:
            org_detail.about = None
            org_detail.contact_info = None
        parsed_org_detail = schemas.OrganisationDetailsExport(**dict(org_detail))
        parsed_org_details.append(parsed_org_detail)

    site_data = schemas.SiteData(
        algoritme_versions=parsed_algos, organisation_details=parsed_org_details
    )
    site_data_json = jsonable_encoder(site_data)

    stream = io.BytesIO()
    stream.write(json.dumps(site_data_json).encode())
    response = StreamingResponse(iter([stream.getvalue()]), media_type="json")

    response.headers["Content-Disposition"] = "attachment; filename=pub_data.json"

    return response
