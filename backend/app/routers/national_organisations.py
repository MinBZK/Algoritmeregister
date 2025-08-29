from fastapi import APIRouter, Depends, Path
from app import repositories
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from app import schemas
from app.schemas.misc import Language
from app.middleware.authorisation.authoriser import AuthType, Authoriser


router = APIRouter()


@router.get(
    "/algorithm/national-organisations/{lang}",
    response_model=list[schemas.NationalOrganisationsCount],
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_national_organisations(
    db: Session = Depends(get_db),
    lang: Language = Path(),
):
    org_repo = repositories.OrganisationRepository(db)
    return org_repo.get_overview_published_nat_org(lang)
