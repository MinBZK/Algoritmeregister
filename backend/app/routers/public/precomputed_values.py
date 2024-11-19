from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app import controllers
from app.middleware.middleware import get_db
from app.schemas.misc import Language


router = APIRouter()


@router.get("/precomputed/{language}")
async def get_precomputed_values(
    language: Language = Path(alias="language"),
    db: Session = Depends(get_db),
):
    return controllers.get_precomputed_values_by_lang(db, language)
