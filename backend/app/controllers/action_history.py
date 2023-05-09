from app import models, schemas
from sqlalchemy.orm import Session


def post_action(
    action: models.OperationEnum,
    algoritme_version_id: str,
    db: Session,
    user: schemas.User | str,
) -> None:
    action_history = {
        "algoritme_version_id": algoritme_version_id,
        "operation": action,
        "user_id": getattr(user, "name", user),
    }
    new_action = models.ActionHistory(**action_history)

    db.add(new_action)
