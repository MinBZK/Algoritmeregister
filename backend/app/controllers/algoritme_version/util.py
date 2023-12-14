from sqlalchemy.orm import Session
from threading import Timer
from app.config.settings import Settings
from app import schemas
from app.repositories import ActionHistoryRepository, AlgoritmeVersionRepository

env_settings = Settings()


def wait_then_disable_preview(lars: str, db: Session) -> None:
    S = Timer(
        env_settings.retract_preview_time,
        disable_preview,
        kwargs={
            "lars": lars,
            "db": db,
            "user": "system",
            "reason": schemas.OperationEnum.preview_timeout,
        },
    )
    S.start()


def disable_preview(
    lars: str, db: Session, user: str, reason: schemas.OperationEnum
) -> bool:
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    action_history_repo = ActionHistoryRepository(db)

    preview_algo = algoritme_version_repo.unpreview_by_lars(lars)
    if not preview_algo:
        return False
    action_history_repo.add(
        schemas.ActionHistoryIn(
            algoritme_version_id=preview_algo.id, user_id=user, operation=reason
        )
    )
    return True


def find_version_changes(
    v1: schemas.AlgoritmeVersionContent, v2: schemas.AlgoritmeVersionContent
) -> bool:
    """
    Compares two algoritme_versions.
    Return true if at least one difference is found.
    """
    for key in dict(v1).keys():
        if getattr(v1, key) != getattr(v2, key):
            return True
    return False
