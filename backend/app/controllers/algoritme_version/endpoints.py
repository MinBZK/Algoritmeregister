from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, controllers
from app.util import upc
from app.config.settings import Settings
from .util import (
    retract_published_algo,
    get_latest_version_algo,
    get_latest_versions_algo,
    publish_latest_version_algo,
    release_latest_version_algo,
    get_published_version_algo,
    get_published_versions_algo,
    set_preview_active,
    find_version_changes,
    remove_all_versions_algo,
    unrelease_all_versions_algo,
)
from app.services.algoritme_version import db_list_to_python_list

# Version agnostic database handling
env_settings = Settings()


def get_all_newest(
    as_org: str,
    db: Session,
    user: schemas.User,
) -> list[schemas.AlgorithmSummary]:
    # Gets latest versions.
    latest_versions = get_latest_versions_algo(as_org=as_org, db=db)
    published_versions = get_published_versions_algo(as_org=as_org, db=db)

    # This dict described which algoritme_version row is published for each algorithm.
    # structure:
    #   lars_code : id_in_db
    # published_ids = {
    #   '12345678': '234',
    #   '11111111': '111',
    # }
    published_ids = {}
    if published_versions:
        for published_algo in published_versions:
            lars_code = getattr(published_algo, "lars")
            published_ids[lars_code] = getattr(published_algo, "id")

    summary_list = []
    for latest_algo in latest_versions:
        lars_code = getattr(latest_algo, "lars")

        summary_list.append(
            schemas.AlgorithmSummary(
                name=getattr(latest_algo, "name"),
                schema_version=getattr(latest_algo, "standard_version"),
                last_update_dt=getattr(latest_algo, "create_dt"),
                lars=getattr(latest_algo, "lars"),
                source_id=getattr(latest_algo, "source_id"),
                published=lars_code in published_ids,
                current_version_released=getattr(latest_algo, "released"),
                current_version_published=getattr(latest_algo, "published"),
                last_update_by="Temporarily unavailable",
            )
        )
    return summary_list


def get_one_newest(
    lars: str,
    db: Session,
    user: schemas.User,
) -> models.AlgoritmeVersion:
    newest_algo = get_latest_version_algo(lars, db)
    if not newest_algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme met LARS-code: {lars}.",
        )
    newest_algo = db_list_to_python_list(newest_algo)
    return newest_algo


def get_one_published(
    lars: str,
    db: Session,
    user: schemas.User,
) -> models.AlgoritmeVersion:
    newest_algo = get_published_version_algo(lars, db)
    if not newest_algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen gepubliceerd algoritme met LARS-code: {lars}.",
        )
    newest_algo = db_list_to_python_list(newest_algo)
    return newest_algo


def post_one(
    as_org: str,
    body,
    db: Session,
    user: schemas.User,
) -> schemas.NewAlgorithmResponse:
    # Generate a unique id for this algorithm.
    current_lars_list = [lars[0] for lars in db.query(models.Algoritme.lars).all()]
    new_lars = upc.find_new_upc(avoid_upc_list=current_lars_list)

    # Creates new entry in algoritme_version table.
    algoritme_version_dict = body.dict()
    new_algoritme_version = models.AlgoritmeVersion(**algoritme_version_dict)

    # Creates new entry in algoritme table.
    algoritme_dict = {
        "lars": new_lars,
        "owner": as_org,
        "versions": [new_algoritme_version],
    }
    new_algoritme = models.Algoritme(**algoritme_dict)

    db.add(new_algoritme)
    db.add(new_algoritme_version)
    db.flush()
    controllers.action_history.post_action(
        models.OperationEnum.created,
        str(new_algoritme_version.id),
        db,
        user,
    )
    db.commit()

    return schemas.NewAlgorithmResponse(lars_code=new_lars)


def retract_one(
    lars: str,
    db: Session,
    user: schemas.User,
) -> None:
    archived_id = retract_published_algo(lars, db)
    if archived_id:
        controllers.action_history.post_action(
            models.OperationEnum.retracted, archived_id, db, user
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen gepubliceerd algoritme gevonden met LARS-code: ({lars})",
        )

    db.commit()


def release_one(
    lars: str,
    db: Session,
    user: schemas.User,
) -> schemas.AlgorithmActionResponse | None:
    latest_version = get_latest_version_algo(lars, db)
    if getattr(latest_version, "released"):
        return schemas.AlgorithmActionResponse(
            message="De laatste versie is al vrijgegeven."
        )
    elif getattr(latest_version, "published"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="De laatste versie is al gepubliceerd. Deze kan niet worden vrijgegeven.",
        )

    unrelease_all_versions_algo(lars, db)
    released_id = release_latest_version_algo(lars, db)
    if released_id:
        controllers.action_history.post_action(
            models.OperationEnum.released, released_id, db, user
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er kan geen algoritme met LARS-code: ({lars}) worden vrijgegeven.",
        )

    db.commit()


def publish_one(
    lars: str,
    db: Session,
    user: schemas.User,
) -> schemas.AlgorithmActionResponse | None:
    latest_version = get_latest_version_algo(lars, db)
    if getattr(latest_version, "published"):
        return schemas.AlgorithmActionResponse(
            message="The latest version is already published."
        )
    elif not getattr(latest_version, "released"):
        return schemas.AlgorithmActionResponse(
            message="The latest version is not released."
        )

    retracted_id = retract_published_algo(lars, db)
    if retracted_id:
        controllers.action_history.post_action(
            models.OperationEnum.retracted, retracted_id, db, user
        )

    unrelease_all_versions_algo(lars, db)
    published_id = publish_latest_version_algo(lars, db)
    if published_id:
        controllers.action_history.post_action(
            models.OperationEnum.published, published_id, db, user
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er kan geen algoritme met LARS-code: ({lars}) worden gepubliceerd.",
        )

    db.commit()


def update_new_version(
    body,
    lars: str,
    db: Session,
    user: schemas.User,
) -> schemas.AlgorithmActionResponse | None:
    algoritme = db.query(models.Algoritme).filter(models.Algoritme.lars == lars).first()
    if not algoritme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme gevonden met LARS-code: ({lars})",
        )

    # Store new entry
    new_algoritme_version = body.dict()
    new_algoritme_version["algoritme_id"] = algoritme.id
    new_version_model = models.AlgoritmeVersion(**new_algoritme_version)

    # Compare with current entry
    latest_version = get_latest_version_algo(lars, db)
    change_found = find_version_changes(latest_version, new_version_model)
    if not change_found:
        return schemas.AlgorithmActionResponse(message="Version has no changes.")

    db.add(new_version_model)
    db.flush()
    controllers.action_history.post_action(
        models.OperationEnum.new_version, str(new_version_model.id), db, user
    )
    db.commit()


def get_preview_link(lars: str, db: Session, user: schemas.User) -> schemas.PreviewUrl:
    preview_id = set_preview_active(lars=lars, db=db)
    if preview_id:
        controllers.action_history.post_action(
            action=models.OperationEnum.preview_activated,
            algoritme_version_id=str(preview_id),
            db=db,
            user=user,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme gevonden met LARS-code: ({lars})",
        )

    db.commit()
    url = f"{env_settings.preview_url}/algoritme/C{lars}"
    return schemas.PreviewUrl(url=url)


def remove_one(lars: str, db: Session, user: schemas.User) -> None:
    n_removed = remove_all_versions_algo(lars=lars, db=db)
    if n_removed == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme gevonden met LARS-code: ({lars})",
        )
    db.commit()
