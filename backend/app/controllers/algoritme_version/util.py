from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from threading import Timer
from app.config.settings import Settings
from app import models, controllers

env_settings = Settings()


def get_published_version_algo(id: str, db: Session) -> models.AlgoritmeVersion | None:
    published_algo = (
        db.query(models.AlgoritmeVersion)
        .filter(
            models.AlgoritmeVersion.published,
            models.AlgoritmeVersion.lars == id,
        )
        .first()
    )
    return published_algo


def get_published_versions_algo(
    as_org: str, db: Session
) -> list[models.AlgoritmeVersion] | None:
    published_algo = (
        db.query(models.AlgoritmeVersion)
        .filter(
            models.AlgoritmeVersion.published,
            models.AlgoritmeVersion.owner == as_org,
        )
        .all()
    )
    return published_algo


def get_latest_version_algo(id: str, db: Session) -> models.AlgoritmeVersion | None:
    query = (
        db.query(models.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.lars == id)
        .order_by(desc(models.AlgoritmeVersion.create_dt))
    )
    latest_algo = query.first()
    return latest_algo


def get_latest_versions_algo(as_org: str, db: Session) -> list[models.AlgoritmeVersion]:
    subquery = (
        db.query(
            models.AlgoritmeVersion.algoritme_id,
            func.max(models.AlgoritmeVersion.create_dt).label("max_creation_dt"),
        )
        .group_by(models.AlgoritmeVersion.algoritme_id)
        .subquery()
    )
    query = (
        db.query(models.AlgoritmeVersion)
        .join(
            subquery,
            and_(
                models.AlgoritmeVersion.algoritme_id == subquery.c.algoritme_id,
                models.AlgoritmeVersion.create_dt == subquery.c.max_creation_dt,
            ),
        )
        .filter(
            models.AlgoritmeVersion.owner == as_org,
        )
    )
    query_result = query.all()
    return query_result


def retract_published_algo(id: str, db: Session) -> str | None:
    query = db.query(models.AlgoritmeVersion).filter(
        models.AlgoritmeVersion.published,
        models.AlgoritmeVersion.lars == id,
    )
    row = query.first()
    if row:
        update_is_succesful = query.update(
            {
                models.AlgoritmeVersion.published: False,
                models.AlgoritmeVersion.released: False,
            },
            synchronize_session=False,
        )
        if update_is_succesful:
            return row.id


def release_latest_version_algo(id: str, db: Session) -> str | None:
    latest_version = get_latest_version_algo(id, db)
    if latest_version:
        setattr(latest_version, "released", True)
        return str(latest_version.id)


def publish_latest_version_algo(id: str, db: Session) -> str | None:
    latest_version = get_latest_version_algo(id, db)
    if latest_version:
        setattr(latest_version, "published", True)
        return str(latest_version.id)


def set_preview_active(lars: str, db: Session) -> str | None:
    latest_algo = (
        db.query(models.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.lars == lars)
        .order_by(desc(models.AlgoritmeVersion.create_dt))
    ).first()
    if not latest_algo:
        return
    setattr(latest_algo, "preview_active", True)
    db.commit()
    return latest_algo.id


def wait_then_disable_preview(lars: str, db: Session) -> None:
    S = Timer(
        env_settings.retract_preview_time,
        disable_preview,
        kwargs={
            "lars": lars,
            "db": db,
            "user": "system",
            "reason": models.OperationEnum.preview_timeout,
        },
    )
    S.start()


def get_preview_algo(lars: str, db: Session):
    preview_algo = (
        db.query(models.AlgoritmeVersion)
        .filter(
            models.AlgoritmeVersion.lars == lars, models.AlgoritmeVersion.preview_active
        )
        .first()
    )
    return preview_algo


def disable_preview(
    lars: str, db: Session, user: str, reason: models.OperationEnum
) -> bool:
    preview_algo = get_preview_algo(lars, db)
    if not preview_algo:
        return False
    setattr(preview_algo, "preview_active", False)
    controllers.action_history.post_action(
        action=reason,
        algoritme_version_id=preview_algo.id,
        db=db,
        user=user,
    )
    db.commit()
    return True


def find_version_changes(v1, v2) -> bool:
    ignore_attributes = ["id", "published", "released", "preview_active", "create_dt"]
    for each in v1.__table__.columns:
        attribute = str(each).split(".")[-1]
        old_attribute = getattr(v1, attribute)
        new_attribute = getattr(v2, attribute)
        if (old_attribute != new_attribute) and attribute not in ignore_attributes:
            return True
    return False


def remove_all_versions_algo(lars: str, db: Session) -> int:
    n_removed = (
        db.query(models.Algoritme).filter(models.Algoritme.lars == lars).delete()
    )
    return n_removed
