from fastapi import APIRouter
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/algoritme/",
    response_model=list[schemas.algemene_informatie.AlgemeneInformatie],
)
async def get_all(db: Session = Depends(get_db)):
    return db.query(models.algemene_informatie.AlgemeneInformatie).all()


@router.get(
    "/algoritme/{id}/",
    response_model=schemas.algemene_informatie.AlgemeneInformatie,
)
async def get_one(id: str, db: Session = Depends(get_db)):
    return (
        db.query(models.algemene_informatie.AlgemeneInformatie)
        .filter(models.algemene_informatie.AlgemeneInformatie.id == id)
        .first()
    )
