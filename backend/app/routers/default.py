from fastapi import APIRouter
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get(
    "/algemene-informatie",
    response_model=list[schemas.algemene_informatie.AlgemeneInformatie],
)
async def project(db: Session = Depends(get_db)):
    return db.query(models.algemene_informatie.AlgemeneInformatie).all()
