from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app import schemas, controllers
from app.middleware.middleware import get_db
from app.schemas.misc import Language


router = APIRouter()


@router.get("/{org_id}/{language}", response_model=schemas.OrganisationDetailsPage)
async def get_org_page_info(
    db: Session = Depends(get_db),
    org_id: str = Path(alias="org_id"),
    lang: Language = Path(alias="language"),
) -> schemas.OrganisationDetailsPage:
    """
    This endpoint is used for the organisation page on the public frontend
    """
    return controllers.get_org_page_info(db, org_id, lang)
