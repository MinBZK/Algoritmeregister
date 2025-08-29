from fastapi import BackgroundTasks, HTTPException
from app import models, schemas
from app.config.settings import Settings
from app.controllers.algoritme_version.endpoints import (
    apply_translation,
    set_highlighted_algorithms,
)
from app.controllers.mailing import send_email
from app.controllers.user import get_from_keycloak_user
from app.middleware.authorisation.schemas import State
from app.middleware.authorisation.user_configuration import UserConfiguration
from app.middleware.authorisation.config._base import (
    load_flow_configurations,
)
from app.repositories.action_history import ActionHistoryRepository
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.repositories.organisation import OrganisationRepository
from app.schemas.action import StateChangeAction
from sqlalchemy.orm import Session

from app.schemas.action_history import ActionHistoryIn
from app.schemas.misc import Language, OperationEnum
from app.services.keycloak.schemas import KeycloakUser
from app.services.translation.base_translator import LanguageCode
from app.util.logger import get_logger

logger = get_logger(__name__)
env_settings = Settings()


def get_state_change_action(
    db: Session, as_org: str, action_key: str
) -> StateChangeAction:
    """
    Provides an action based on the organisation (e.g. their flow)
    and the requested action_key.
    """
    all_flows = load_flow_configurations()

    org_repository = OrganisationRepository(db)
    org = org_repository.get_by_org_id(as_org)
    if not org:
        raise HTTPException(404)
    flow = all_flows[org.flow]
    return flow["state_change_actions"][action_key]


def get_available_actions_by_lars(
    db: Session, keycloak_user: KeycloakUser, lars: str
) -> list[StateChangeAction]:
    """
    Provides the actions available based on the user and
    the state of the requested algorithm description, and
    the flow in which the organisation operates.
    """
    # Collect algorithm description to get the state and flow.
    algo_repository = AlgoritmeVersionRepository(db)
    algo = algo_repository.get_latest_by_lars_by_lang(lars, Language.NLD)
    if not algo:
        raise HTTPException(404)
    organisation = algo.owner

    user = get_from_keycloak_user(db, keycloak_user)
    user_config = UserConfiguration(user)
    all_permissions = user_config._state_change_permissions(organisation)
    for a in all_permissions:
        if a.origin_state != algo.state:
            a.enabled = False
    return all_permissions


def update_state_by_lars(
    db: Session,
    user: KeycloakUser,
    lars: str,
    as_org: str,
    action_key: str,
    background_tasks: BackgroundTasks,
) -> None:
    """
    Updates the state of the algorithm version, if the origin state matches the current state.
    The variants in other languages are also handled, if it concerns publishing/retraction.
    """
    algo_repository = AlgoritmeVersionRepository(db)
    action_history_repo = ActionHistoryRepository(db)

    action = get_state_change_action(db, as_org, action_key)
    origin_state = action.origin_state
    target_state = action.target_state

    latest_nld = algo_repository.get_latest_by_lars_by_lang(lars, Language.NLD)
    if not latest_nld:
        raise HTTPException(404)
    # Latest record has to mach origin state, except during retraction
    if latest_nld.state != origin_state and origin_state != State.PUBLISHED:
        raise HTTPException(
            400, f"INVALID ORIGIN_STATE, CURRENT STATE: {latest_nld.state}"
        )

    if origin_state == State.PUBLISHED or target_state == State.PUBLISHED:
        # Retraction or publication, expire all.
        algos_all_lang = algo_repository.get_published_by_lars(lars)
        for algo in algos_all_lang:
            algo_repository.update_state_by_id(algo.id, State.EXPIRED)
            action_history_repo.add(
                ActionHistoryIn(
                    algoritme_version_id=algo.id,
                    user_id=user.username,
                    operation=OperationEnum.retracted,
                )
            )

    if target_state == State.PUBLISHED:
        # Publication -> do translations.
        for lang in [LanguageCode.ENGLISH, LanguageCode.FRISIAN]:
            new_algo = schemas.AlgoritmeVersionIn(**latest_nld.model_dump())
            new_algo_model = models.AlgoritmeVersion(**new_algo.model_dump())
            background_tasks.add_task(
                apply_translation, new_algo_model, db, user.username, lang
            )

    # Update state of NLD record (can be because of published, retracted or anything else.)
    algo_repository.update_state_by_id(latest_nld.id, target_state)
    if action.key == "publish":
        operation = OperationEnum.published
    elif action.key == "release":
        operation = OperationEnum.released
    elif action.key == "retract":
        operation = OperationEnum.retracted
    elif action.key == "release_to_2":
        operation = OperationEnum.released
    else:
        # TODO: actions should have predefined operation attached to them
        # missing operation: reject_to_1.
        logger.error("This action is not implemented")
        raise HTTPException(500)

    action_history_repo.add(
        ActionHistoryIn(
            algoritme_version_id=latest_nld.id,
            operation=operation,
            user_id=user.username,
        )
    )

    if action.send_email_type is not None:
        background_tasks.add_task(
            send_email, db=db, email_type=action.send_email_type, lars=lars
        )
    if origin_state == State.PUBLISHED or target_state == State.PUBLISHED:
        # Retracting or publishing -> set highlighted algorithms
        background_tasks.add_task(set_highlighted_algorithms, db)

    db.commit()
