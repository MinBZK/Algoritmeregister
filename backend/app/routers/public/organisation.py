from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app import schemas, controllers
from app.middleware.middleware import get_db
from app.schemas.misc import Language


router = APIRouter()


@router.post("/organisation/{language}")
async def get_some_orgs_overview(
    query: schemas.OrganisationQuery,
    language: Language = Path(alias="language"),
    db: Session = Depends(get_db),
) -> schemas.OrganisationQueryResponse:
    return controllers.get_orgs_by_query(db, query, language)


@router.get("/organisation-count/{language}")
async def get_orgs_count(
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> int:
    return controllers.get_orgs_count(db, language)
