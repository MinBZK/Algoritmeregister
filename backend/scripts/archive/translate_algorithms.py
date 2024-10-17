"""
This module translates all existing algorithms in the database.
It is meant to be run as a script once, and will not be used in the actual application.
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.middleware.authorisation.schemas import State
from app.models import AlgoritmeVersion
from app.controllers.algoritme_version.endpoints import apply_translation
from app.schemas import Language
from app.services.algoritme_version import db_list_to_python_list
from app.services.translation.base_translator import LanguageCode
from app.util.logger import get_logger

# initialize new independent logger
logger = get_logger(__name__)


def get_all_published_versions(db):
    """
    Get all algorithm versions from the database.
    """
    model_list = (
        db.query(AlgoritmeVersion)
        .filter(AlgoritmeVersion.language == Language.NLD)
        .filter(AlgoritmeVersion.state == State.PUBLISHED)
        .all()
    )
    model_list = [db_list_to_python_list(model) for model in model_list]
    return model_list


def apply(
    db: Session,
    algos: list[AlgoritmeVersion],
    target_lang: LanguageCode = LanguageCode.ENGLISH,
):
    """
    Translate all algorithms to English.
    """
    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }
    existing_translations = (
        db.query(AlgoritmeVersion)
        .filter(AlgoritmeVersion.state == State.PUBLISHED)
        .filter(AlgoritmeVersion.language == lang_code_map[target_lang])
        .all()
    )

    total_algos = len(algos)
    for algo_count, algo in enumerate(algos, 1):
        if any(
            existing_translation.algoritme_id == algo.algoritme_id
            for existing_translation in existing_translations
        ):
            logger.info(
                f"({algo_count}/{total_algos}) Skipping {algo.name} because it already has a translation in {lang_code_map[target_lang]}."
            )
            continue
        logger.info(f"Translating {algo.name} to {lang_code_map[target_lang]}.")
        apply_translation(
            algo,
            db,
            "BULK_TRANSLATOR",
            language=target_lang,
        )
        logger.info(
            f"({algo_count}/{total_algos}) Translated {algo.name} to {lang_code_map[target_lang]} successfully."
        )


def main():
    logger.info("Retrieving all Dutch algorithms.")
    db = SessionLocal()
    algos = get_all_published_versions(db)
    logger.info(f"Found {len(algos)} Dutch algorithms to translate.")
    apply(db, algos, target_lang=LanguageCode.ENGLISH)
    logger.info("Finished translation of existing algorithms to English.")
    logger.info("Starting translation of existing algorithms to Frisian.\n")
    apply(db, algos, target_lang=LanguageCode.FRISIAN)
    logger.info("Finished translation of existing algorithms to Frisian.\n")
    db.close()


if __name__ == "__main__":
    main()
