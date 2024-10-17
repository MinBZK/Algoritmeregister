from app.database.database import SessionLocal
from sqlalchemy.orm import Session

from app.middleware.authorisation.schemas import State
from app.models.algoritme_version import AlgoritmeVersion
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.schemas.misc import Language
from app.util.logger import get_logger


# initialize new independent logger
logger = get_logger(__name__)


def migrate_state(db: Session):
    # Start with expiring all.
    algos = db.query(AlgoritmeVersion).all()
    for algo in algos:
        algo.state = State.EXPIRED

    # Need to put the latest versions on STATE_1.
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    latest_algos = algoritme_version_repo.get_latest_by_lang(Language.NLD)
    for algo in latest_algos:
        algoritme_version_repo.update_state_by_id(algo.id, State.STATE_1)

    # For published algorithms, set state to State.PUBLISHED.
    published_algos = db.query(AlgoritmeVersion).where(AlgoritmeVersion.published).all()
    for algo in published_algos:
        algo.state = State.PUBLISHED

    # For released algorithms, set state to State.STATE_2.
    released_algos = db.query(AlgoritmeVersion).where(AlgoritmeVersion.released).all()
    latest_ids = [a.id for a in latest_algos]
    for algo in released_algos:
        # Can only be done if it is also the latest version
        if algo.id in latest_ids:
            algo.state = State.STATE_2

    db.commit()


if __name__ == "__main__":
    logger.info("Starting updating state based on released and published columns.")
    db = SessionLocal()
    migrate_state(db)
    logger.info("Finished updating state based on released and published columns.")
    db.close()
