from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session
from app import schemas, middleware
from app.controllers import get_algoritme_owner

router = APIRouter()


@router.get(
    "/algoritme/find/{algoritme_id}",
    response_model=schemas.OrganisationIn,
)
async def find_algoritme_owner(
    lars: str = Path(alias="algoritme_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(middleware.get_current_user),
):
    return get_algoritme_owner(db, user, lars)
