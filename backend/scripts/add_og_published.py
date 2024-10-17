import pandas as pd
import json
from app.database.database import SessionLocal
from app import models
from sqlalchemy.orm import Session
from app.middleware.authorisation.schemas import State
from app.schemas import Language
from app.repositories import ActionHistoryRepository
from app.schemas import ActionHistoryIn, OperationEnum
from datetime import datetime


def add_113_first_published():
    db = SessionLocal()
    # The ones without a 'published' are the first 113
    versions_to_publish = (
        db.query(models.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.language == Language.NLD)
        .order_by(models.AlgoritmeVersion.create_dt)
        .limit(113)
        .all()
    )

    publication_date = datetime.strptime("2023-04-01", "%Y-%m-%d")

    # Check if this script has been run before
    duplicates = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.create_dt == publication_date)
        .first()
    )
    if duplicates:
        print("These records are already present, exiting. (1)")
        return

    print(f"Adding action history for {len(versions_to_publish)} descriptions.")
    action_repository = ActionHistoryRepository(db)
    for version in versions_to_publish:
        action = ActionHistoryIn(
            create_dt=publication_date,
            algoritme_version_id=version.id,
            operation=OperationEnum.published,
            user_id="RETRO-ACTIVE LOGGER",
        )
        action_repository.add(action)
    db.commit()


def add_any_other_without_action_history():
    db = SessionLocal()

    subquery = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.operation == OperationEnum.published)
        .subquery()
    )
    versions_to_publish = (
        db.query(models.AlgoritmeVersion)
        .join(
            subquery,
            isouter=True,
        )
        .filter(
            models.AlgoritmeVersion.state == State.PUBLISHED,
            models.AlgoritmeVersion.language == Language.NLD,
            subquery.columns.operation.is_(None),
        )
        .all()
    )

    if not versions_to_publish:
        print("No published versions without proper action history found, exiting. (2)")
        return

    print(f"Adding action history for {len(versions_to_publish)} descriptions.")
    action_repository = ActionHistoryRepository(db)
    for version in versions_to_publish:
        action = ActionHistoryIn(
            create_dt=version.create_dt,
            algoritme_version_id=version.id,
            operation=OperationEnum.published,
            user_id="RETRO-ACTIVE LOGGER",
        )
        action_repository.add(action)
    db.commit()


if __name__ == "__main__":
    add_113_first_published()
    add_any_other_without_action_history()
