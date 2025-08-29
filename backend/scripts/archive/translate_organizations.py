"""
This module translates all existing algorithms in the database.
It is meant to be run as a script once, and will not be used in the actual application.
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app import schemas
from app.models.organisation_details import OrganisationDetails
from app.controllers import translate_org_name
from app.schemas.misc import Language
from app.services.translation import LanguageCode
from app.util.logger import get_logger

# initialize new independent logger
logger = get_logger(__name__)


def get_all_published_versions(db: Session) -> list[schemas.OrganisationDetailsDB]:
    """
    Get all organisation_detailas from the database.
    """
    entries = (
        db.query(OrganisationDetails)
        .filter(OrganisationDetails.language == Language.NLD)
        .all()
    )
    return [schemas.OrganisationDetailsDB.model_validate(entry) for entry in entries]


def apply(
    db: Session,
    org_details: list[schemas.OrganisationDetailsDB],
    lang: LanguageCode = LanguageCode.ENGLISH,
):
    """
    Translate all algorithms to English.
    """
    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }
    existing_translations = (
        db.query(OrganisationDetails)
        .filter(OrganisationDetails.language == lang_code_map[lang])
        .all()
    )

    total_orgs = len(org_details)
    for org_count, org_detail in enumerate(org_details, 1):
        if any(
            existing_translation.organisation_id == org_detail.organisation_id
            for existing_translation in existing_translations
        ):
            logger.info(
                f"({org_count}/{total_orgs}) Skipping {org_detail.name} because it already has a translation in {lang_code_map[lang]}."
            )
            continue
        logger.info(f"Translating {org_detail.name} to {lang_code_map[lang]}.")
        translate_org_name(db, org_detail.name, org_detail.id, lang)
        logger.info(
            f"Translated {org_detail.name} to {lang_code_map[lang]} successfully."
        )
        if (org_count) % 100 == 0:
            db.commit()
            logger.info(f"Committed batch up to row {org_count}")


def main():
    logger.info("Starting translation of existing organisations.")
    db = SessionLocal()
    org_details = get_all_published_versions(db)
    logger.info(f"Found {len(org_details)} Dutch organisation details to translate.")
    apply(db, org_details, LanguageCode.ENGLISH)
    apply(db, org_details, LanguageCode.FRISIAN)
    logger.info("Finished translation of existing organisations.")
    db.close()


if __name__ == "__main__":
    main()
