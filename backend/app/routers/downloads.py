from fastapi import Depends, HTTPException, Path, Query, APIRouter
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.controllers import (
    generate_word_download,
    generate_download_file,
    generate_pdf_download,
)
from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.keycloak_authenticator import get_current_user
from app.middleware.middleware import get_db
from app.repositories.algoritme import AlgoritmeRepository
from app.repositories.organisation import OrganisationRepository
from app.services.keycloak import KeycloakUser


router = APIRouter()


@router.get(
    "/organizations/{organisation_name}",
    response_class=FileResponse,
    dependencies=[Depends(Authoriser(AuthType.OrgOnly))],
)
async def get_file_many(
    db: Session = Depends(get_db),
    as_org: str = Path(alias="organisation_name"),
    filetype: str = Query(alias="filetype"),
    user: KeycloakUser = Depends(get_current_user),
):
    if not filetype or filetype == "word":
        return generate_word_download(db, org_name=as_org)
    if filetype == "excel":
        return generate_download_file(db, org_name=as_org, which_version="latest")
    if filetype == "pdf":
        return generate_pdf_download(db, org_name=as_org)


@router.get(
    "/organizations/{organisation_name}/algorithms/{algorithm_id}",
    response_class=FileResponse,
    dependencies=[Depends(Authoriser(AuthType.OrgOnly))],
)
async def get_file_one(
    db: Session = Depends(get_db),
    lars: str = Path(alias="algorithm_id"),
    as_org: str = Path(alias="organisation_name"),
    filetype: str = Query(alias="filetype"),
):
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_code(as_org)
    algoritme_repo = AlgoritmeRepository(db)
    algoritme = algoritme_repo.get_by_lars(lars)
    if not org or not algoritme or algoritme.owner != org.code:
        return HTTPException(404)
    if not filetype or filetype == "word":
        return generate_word_download(db, lars=lars)
    if filetype == "excel":
        return generate_download_file(db, lars=lars, which_version="latest")
    if filetype == "pdf":
        return generate_pdf_download(db, lars=lars)
