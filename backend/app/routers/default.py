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
    response_model=list[schemas.algoritme.Algoritme],
)
async def get_all(db: Session = Depends(get_db)):
    return db.query(models.algoritme.Algoritme).all()


@router.get(
    "/algoritme/{slug}/",
    response_model=schemas.algoritme.Algoritme,
)
async def get_one(slug: str, db: Session = Depends(get_db)):
    x = (
        db.query(models.algoritme.Algoritme)
        .filter(models.algoritme.Algoritme.slug == slug)
        .first()
    )
    return x


@router.get("/algoritme-simple-list/")
async def get_simple_list(db: Session = Depends(get_db)):
    return db.query(
        models.algoritme.Algoritme.slug,
        models.algoritme.Algoritme.name,
        models.algoritme.Algoritme.organization,
    ).all()
