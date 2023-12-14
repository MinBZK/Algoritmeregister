"""
This module translates all existing algorithms in the database.
It is meant to be run as a script once, and will not be used in the actual application.
"""
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
import logging
from app.models import AlgoritmeVersion
from app import schemas
from app.controllers.algoritme_version.endpoints import apply_translation
from app.services.algoritme_version import db_list_to_python_list

# initialize new independent logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_all_published_versions(db):
    """
    Get all algorithm versions from the database.
    """
    model_list = (
        db.query(AlgoritmeVersion)
        .filter(AlgoritmeVersion.language == schemas.Language.NLD)
        .filter(AlgoritmeVersion.published)
        .all()
    )
    model_list = [db_list_to_python_list(model) for model in model_list]
    return model_list


def apply(db: Session, algos: list[AlgoritmeVersion]):
    """
    Translate all algorithms to English.
    """
    for algo in algos:
        logger.info(f"Translating {algo.name} to English.")
        apply_translation(
            algo,
            db,
            "BULK_TRANSLATOR",
        )
        logger.info(f"Translated {algo.name} to English successfully.")


if __name__ == "__main__":
    logger.info("Starting translation of existing algorithms.")
    db = SessionLocal()
    algos = get_all_published_versions(db)
    logger.info(f"Found {len(algos)} Dutch algorithms to translate.")
    apply(db, algos)
    logger.info("Finished translation of existing algorithms.")
    db.close()
