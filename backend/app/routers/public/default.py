from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.config.settings import Keycloak, Settings
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from app.schemas.misc import Language
from app import models
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
env_settings = Settings()


@router.get("/sitemap-urls")
async def get_sitemap_urls(db: Session = Depends(get_db)):
    algorithms_nl = (
        db.query(models.Algoritme)
        .join(
            models.AlgoritmeVersion,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(models.AlgoritmeVersion.language == Language.NLD)
        .filter(models.AlgoritmeVersion.state == State.PUBLISHED)
        .order_by(models.Algoritme.lars)
        .all()
    )

    result_dict = []
    for algorithm in algorithms_nl:
        algo_dict = {
            "loc": "/nl/algoritme/" + algorithm.lars,
            "lastmod": algorithm.create_dt,
            "changefreq": "daily",
        }
        result_dict.append(algo_dict)

    algorithms_en = (
        db.query(models.Algoritme)
        .join(
            models.AlgoritmeVersion,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(models.AlgoritmeVersion.language == Language.ENG)
        .filter(models.AlgoritmeVersion.state == State.PUBLISHED)
        .order_by(models.Algoritme.lars)
        .all()
    )
    for algorithm in algorithms_en:
        algo_dict = {
            "loc": "/en/algoritme/" + algorithm.lars,
            "lastmod": algorithm.create_dt,
            "changefreq": "daily",
        }
        result_dict.append(algo_dict)

    return result_dict


@router.get("/health")
def healthcheck(db: Session = Depends(get_db)) -> str:
    """
    Check whether the database still responds
    """
    db.execute(text("SELECT 1"))  # random query
    return "OK"


@router.get("/config")
def get_config():
    """I cannot get variables in the frontend relating to differentiate between test, acc and prod"""
    settings = Keycloak()
    response = {
        "keycloak_uri": settings.KEYCLOAK_URI,
        "keycloak_realm": settings.KEYCLOAK_REALM,
        "keycloak_client": settings.KEYCLOAK_CLIENT,
    }
    return response
