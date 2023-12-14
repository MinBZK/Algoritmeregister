from fastapi import Depends, Path, Query, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import schemas, middleware
from app.controllers import (
    generate_word_download,
    generate_excel_download,
    generate_pdf_download,
)
from app.middleware.decorators import authorized_user_only

router = APIRouter()


@router.get(
    "/organizations/{organization_name}",
    response_class=FileResponse,
)
@authorized_user_only
async def get_file_many(
    db: Session = Depends(middleware.get_db),
    as_org: str = Path(alias="organization_name"),
    filetype: str = Query(alias="filetype"),
    user: schemas.User = Depends(middleware.get_current_user),
):
    if not filetype or filetype == "word":
        return generate_word_download(db, org_name=as_org)
    if filetype == "excel":
        return generate_excel_download(db, org_name=as_org, which_version="latest")
    if filetype == "pdf":
        return generate_pdf_download(db, org_name=as_org)


@router.get(
    "/organizations/{organization_name}/algorithms/{algorithm_id}",
    response_class=FileResponse,
)
@authorized_user_only
async def get_file_one(
    db: Session = Depends(middleware.get_db),
    lars: str = Path(alias="algorithm_id"),
    as_org: str = Path(alias="organization_name"),
    filetype: str = Query(alias="filetype"),
    user: schemas.User = Depends(middleware.get_current_user),
):
    if not filetype or filetype == "word":
        return generate_word_download(db, lars=lars)
    if filetype == "excel":
        return generate_excel_download(db, lars=lars, which_version="latest")
    if filetype == "pdf":
        return generate_pdf_download(db, lars=lars)
