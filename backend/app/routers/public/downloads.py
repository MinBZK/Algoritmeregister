from fastapi import APIRouter, Path, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import middleware, schemas

from app.controllers import generate_excel_download

router = APIRouter()


@router.get(
    "/{language}",
    response_class=FileResponse,
)
async def get_file_all(
    db: Session = Depends(middleware.get_db),
    lang: schemas.Language = Path(alias="language"),
    filetype: str = Query(alias="filetype"),
):
    # if filetype == "word":
    #     return generate_word_download(db, lang, which_version="published")
    if filetype == "excel":
        return generate_excel_download(db, lang, which_version="published")


@router.get(
    "/algorithms/{algorithm_id}/{language}",
    response_class=FileResponse,
)
async def get_file_one(
    db: Session = Depends(middleware.get_db),
    lars: str = Path(alias="algorithm_id"),
    lang: schemas.Language = Path(alias="language"),
    filetype: str = Query(alias="filetype"),
):
    # if filetype == "word":
    #     return generate_word_download(db, lang, lars=lars, which_version="published")
    if filetype == "excel":
        return generate_excel_download(db, lang, lars=lars, which_version="published")
