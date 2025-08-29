"""
This module translates the column impacttoetsen_grouping column in the database.
"""

from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.middleware.authorisation.schemas import State
from app.models import AlgoritmeVersion
from app.services.translation.base_translator import LanguageCode
from etl.logger import get_logger
from sqlalchemy import select
from app.schemas.misc import Language, standard_impact_assessment_titles_mapping
import copy

# python -m scripts.archive.translate_impacttoetsen_grouping_column

logger = get_logger(__name__)


def translate_impacttoetsen_grouping_column(
    db: Session,
    target_lang: LanguageCode,
):
    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }

    # Get all Dutch published algorithm versions from the database
    stmt = select(AlgoritmeVersion).where(
        AlgoritmeVersion.state == State.PUBLISHED,
        AlgoritmeVersion.language == Language.NLD,
    )
    dutch_algos = db.execute(stmt).scalars().all()

    for algo in dutch_algos:
        # Retrieve the published algo_version of the target language
        stmt = select(AlgoritmeVersion).where(
            AlgoritmeVersion.algoritme_id == algo.algoritme_id,
            AlgoritmeVersion.language == lang_code_map[target_lang],
            AlgoritmeVersion.state == State.PUBLISHED,
        )
        translated_algo = db.execute(stmt).scalars().first()

        if not translated_algo:
            logger.info(
                f"No {lang_code_map[target_lang]} translation found for algo_id {algo.algoritme_id}, skipping."
            )
            continue

        # if there is data in the algo.impacttoetsen_grouping
        # replace only the title with the translated version
        if algo.impacttoetsen_grouping:
            logger.info(f"Translating impacttoetsen for algo_id {algo.algoritme_id}")
            translated_grouping = []
            for ia in algo.impacttoetsen_grouping:
                ia_copy = copy.deepcopy(ia)
                ia_title = ia_copy.get("title")
                for enum_key, label in standard_impact_assessment_titles_mapping[
                    Language.NLD
                ].items():
                    if ia_title == label:
                        ia_copy["title"] = standard_impact_assessment_titles_mapping[
                            lang_code_map[target_lang]
                        ][enum_key]
                        break
                translated_grouping.append(ia_copy)
            logger.info(f"Old impacttoetsen for algo_id {algo.algoritme_id}: {algo.impacttoetsen_grouping}")
            translated_algo.impacttoetsen_grouping = translated_grouping
            logger.info(
                f"New impacttoetsen for algo_id {algo.algoritme_id}: {translated_algo.impacttoetsen_grouping}"
            )
        db.commit()


def main():
    logger.info("Starting script for translating column impacttoetsen grouping.")
    db = SessionLocal()
    logger.info("Starting translation of column into English.")
    translate_impacttoetsen_grouping_column(db, target_lang=LanguageCode.ENGLISH)
    logger.info("Completed translation of column into English.")
    logger.info("Starting translation of column into Frisian.")
    translate_impacttoetsen_grouping_column(db, target_lang=LanguageCode.FRISIAN)
    logger.info("Completed translation of column into Frisian.")
    db.close()


if __name__ == "__main__":
    main()
