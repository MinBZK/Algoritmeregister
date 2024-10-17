import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas
from app.middleware.authorisation.schemas import State
from app.services.keycloak import KeycloakUser
from app.services import translation
from app.util import upc
from app.config.settings import Settings
from app.schemas import Language, OperationEnum
from .util import (
    find_version_changes,
)
from app.services.algoritme_version import db_list_to_python_list
from app.repositories import (
    AlgoritmeVersionRepository,
    OrganisationRepository,
    AlgoritmeRepository,
    ActionHistoryRepository,
)
from app.util.logger import get_logger
from app.services.translation import LanguageCode

logger = get_logger(__name__)
# Version agnostic database handling
env_settings = Settings()


def get_algorithm_summary(
    as_org: str,
    db: Session,
) -> list[schemas.AlgorithmSummary]:
    # Gets latest versions.
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    latest_versions = algoritme_version_repository.get_latest_by_org_by_lang(
        as_org, Language.NLD
    )
    published_versions = algoritme_version_repository.get_published_by_org_by_lang(
        as_org, Language.NLD
    )
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
            lars_code = published_algo.lars
            published_ids[lars_code] = published_algo.id

    # build an 'id' list
    ids = []
    for algo in latest_versions:
        ids.append(algo.id)

    # This is a list of all history associated with the algoritme_version entries.
    algos_history = (
        db.query(models.ActionHistory)
        .filter(
            models.ActionHistory.algoritme_version_id.in_(ids),
            or_(
                models.ActionHistory.operation == OperationEnum.created,
                models.ActionHistory.operation == OperationEnum.new_version,
                models.ActionHistory.operation == OperationEnum.released,
                models.ActionHistory.operation == OperationEnum.retracted,
            ),
        )
        .order_by(models.ActionHistory.create_dt.desc())
        .all()
    )

    # This dict describes who edited the algoritme_version last.
    # structure:
    #   algoritme_version_id : user_id
    # published_ids = {
    #   '12345678': 'example@ictu.nl',
    #   '11111111': 'example2@ictu.nl',
    # }
    last_edited = {}
    for history_point in algos_history:
        algoritme_version_id = history_point.algoritme_version_id
        if algoritme_version_id not in last_edited:
            last_edited[algoritme_version_id] = history_point.user_id

    summary_list = []
    for latest_algo in latest_versions:
        lars_code = latest_algo.lars

        summary_list.append(
            schemas.AlgorithmSummary(
                name=latest_algo.name,
                schema_version=latest_algo.standard_version,
                last_update_dt=latest_algo.create_dt,
                lars=latest_algo.lars,
                source_id=latest_algo.source_id,
                published=lars_code in published_ids,
                current_version_released=latest_algo.state == State.STATE_2,
                current_version_published=latest_algo.state == State.PUBLISHED,
                last_update_by=last_edited.get(latest_algo.id) or "Onbekend",
            )
        )
    summary_list.sort(key=lambda x: x.last_update_dt, reverse=True)
    return summary_list


def get_one_newest(
    lars: str,
    db: Session,
) -> schemas.AlgoritmeVersionDB:
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    newest_algo = algoritme_version_repository.get_latest_by_lars_by_lang(
        lars, Language.NLD
    )
    if not newest_algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme met LARS-code: {lars}.",
        )
    return newest_algo


def get_one_published(
    lars: str,
    db: Session,
) -> schemas.AlgoritmeVersionDB:
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    newest_algo = algoritme_version_repository.get_published_by_lars_by_lang(
        lars, Language.NLD
    )
    if not newest_algo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen gepubliceerd algoritme met LARS-code: {lars}.",
        )
    return newest_algo


def post_one(
    as_org: str,
    body: schemas.AlgoritmeVersionContent,
    db: Session,
    user: KeycloakUser,
) -> schemas.NewAlgorithmResponse:
    organisation_repo = OrganisationRepository(session=db)
    algoritme_version_repo = AlgoritmeVersionRepository(session=db)
    algoritme_repo = AlgoritmeRepository(session=db)
    action_history_repo = ActionHistoryRepository(session=db)

    org = organisation_repo.get_by_code(as_org)
    if not org:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="ORG_NOT_FOUND")

    # Generates a unique id for this algorithm.
    current_lars_codes = algoritme_repo.get_all_lars()
    new_lars = upc.find_new_upc(avoid_upc_list=current_lars_codes)

    algoritme = schemas.AlgoritmeIn(lars=new_lars, organisation_id=org.id)
    algoritme_db = algoritme_repo.add(algoritme)

    # Creates new entry in algoritme_version table.
    algoritme_version = schemas.AlgoritmeVersionIn(
        **body.dict(),
        algoritme_id=algoritme_db.id,
        language=Language.NLD,
        state=State.STATE_1,
    )
    algoritme_version_db = algoritme_version_repo.add(algoritme_version)

    # Logs action
    action = schemas.ActionHistoryIn(
        algoritme_version_id=algoritme_version_db.id,
        operation=OperationEnum.created,
        user_id=user.username,
    )
    action_history_repo.add(action)
    return schemas.NewAlgorithmResponse(lars_code=new_lars)


def apply_translation(
    algo: models.AlgoritmeVersion,
    db: Session,
    username: str,
    language: LanguageCode = LanguageCode.ENGLISH,
) -> schemas.AlgoritmeVersionIn:
    algo = db_list_to_python_list(algo)
    preprocessor = translation.Preprocessor(
        algo,
        attrs_to_delete=[
            "id",
            "create_dt",
            "algoritme",
            "lars",
            "owner",
            "published",
            "released",
            "preview_active",
            "state",
        ],
        target_lang=language.value,
    )
    # 1. Add the non-translatable fields as-is
    translated_dict = preprocessor.get_non_translatable_fields()

    # 2. Add translations for fields that have a list as value
    list_fields = preprocessor.get_list_fields()
    list_translator = translation.ListValuesTranslator(
        field_dict=list_fields,
        organisation_name=algo.organization,
        algorithm_name=algo.name,
    )
    translation_response = list_translator.translate(
        preprocessor.translation_spec["default_translations"]
    )
    translated_dict.update(translation_response.fields)

    # 3. Add translations for fields that need automatic translation
    auto_translate_fields = preprocessor.get_auto_translate_fields()
    auto_translator = translation.AutoTranslator(
        field_dict=auto_translate_fields,
        target_lang=language,
        organisation_name=algo.organization,
        algorithm_name=algo.name,
    )
    translation_response = auto_translator.translate()
    translated_dict.update(translation_response.fields)

    # 4. Translate the fields that have a default translation
    default_translator = translation.DefaultValuesTranslator(
        field_dict=preprocessor.get_default_translate_fields(),
        target_lang=language,
        organisation_name=algo.organization,
        algorithm_name=algo.name,
    )
    translation_response = default_translator.translate(
        preprocessor.translation_spec["default_translations"]
    )
    translated_dict.update(translation_response.fields)

    # 5. Truncate the fields that are too long
    preprocessor.truncate_fields(translated_dict)

    # 6. Save the translations
    algoritme_version = save_translation(algo, db, translated_dict, username, language)
    return algoritme_version


def save_translation(
    algo: models.AlgoritmeVersion,
    db: Session,
    translated_dict,
    username: str,
    language=LanguageCode.ENGLISH,
):
    """
    Saves the translation to the database.
    """
    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }
    algoritme_version = schemas.AlgoritmeVersionIn(
        **translated_dict, state=State.PUBLISHED
    )
    algoritme_version.language = lang_code_map[language]
    algoritme_version.create_dt = algo.create_dt  # Date should be the same

    algoritme_version_repository = AlgoritmeVersionRepository(db)
    algoritme_version_db = algoritme_version_repository.add(algoritme_version)

    action_history_repository = ActionHistoryRepository(db)
    action = schemas.ActionHistoryIn(
        algoritme_version_id=algoritme_version_db.id,
        operation=OperationEnum.created,
        user_id=username,
    )
    action_history_repository.add(action)
    action = schemas.ActionHistoryIn(
        algoritme_version_id=algoritme_version_db.id,
        operation=OperationEnum.published,
        user_id=username,
    )
    action_history_repository.add(action)

    return algoritme_version


def update_new_version(
    body: schemas.AlgoritmeVersionContent,
    lars: str,
    db: Session,
    user: KeycloakUser,
) -> schemas.AlgorithmActionResponse | None:
    algoritme_repo = AlgoritmeRepository(db)
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    action_history_repo = ActionHistoryRepository(db)

    algoritme = algoritme_repo.get_by_lars(lars)
    if not algoritme:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ALGORITHM_NOT_FOUND")

    latest_version = algoritme_version_repo.get_latest_by_lars_by_lang(
        lars, Language.NLD
    )
    if not latest_version:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ALGORITHM_NOT_FOUND")
    change_found = find_version_changes(
        schemas.AlgoritmeVersionContent(**latest_version.dict()), body
    )
    if not change_found:
        return schemas.AlgorithmActionResponse(message="NO_CHANGES")

    # Expire the previous version
    if latest_version.state != State.PUBLISHED:
        logger.warning("The state change to expired is not logged")
        algoritme_version_repo.update_state_by_id(latest_version.id, State.EXPIRED)
        # TODO: Add expired as option to operations.
        # action_history_repo.add(
        #     ActionHistoryIn(
        #         algoritme_version_id=latest_version.id,
        #         operation=OperationEnum.expired,
        #         user_id=user.username,
        #     )
        # )

    # Build new version
    new_version = schemas.AlgoritmeVersionIn(
        **body.dict(),
        algoritme_id=algoritme.id,
        language=Language.NLD,
        state=State.STATE_1,
    )
    new_version = algoritme_version_repo.add(new_version)
    action_history_repo.add(
        schemas.ActionHistoryIn(
            algoritme_version_id=new_version.id,
            operation=OperationEnum.new_version,
            user_id=user.username,
        )
    )


def get_preview_link(lars: str, db: Session, user: KeycloakUser) -> schemas.PreviewUrl:
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    action_history_repo = ActionHistoryRepository(db)
    previewed_algo = algoritme_version_repo.preview_latest_by_lars(lars)
    latest_by_lang = algoritme_version_repo.get_latest_by_lars_by_lang(
        lars, lang=Language.NLD
    )
    if latest_by_lang:
        name = latest_by_lang.name
        org = latest_by_lang.organization
        name = name if name is not None else ""
        org = org if org is not None else ""
        slug = name.lower() + " " + org.lower()
        slug = re.sub(r"[^a-zA-Z0-9 ]", "", slug)
        slug = re.sub(r" {2,}", "-", slug)
        slug = slug.replace(" ", "-")

    if previewed_algo:
        action_history_repo.add(
            schemas.ActionHistoryIn(
                algoritme_version_id=previewed_algo.id,
                operation=OperationEnum.preview_activated,
                user_id=user.username,
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme gevonden met LARS-code: ({lars})",
        )
    url = f"{env_settings.preview_url}/nl/algoritme/{slug}/C{lars}"
    return schemas.PreviewUrl(url=url)


def remove_one(lars: str, db: Session) -> None:
    algoritme_repository = AlgoritmeRepository(db)
    n_removed = algoritme_repository.delete_by_lars(lars)
    if n_removed == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritme gevonden met LARS-code: ({lars})",
        )
    db.commit()


def set_archive_status(
    version_id: int,
    db: Session,
    archived: bool,
    user_id: str,
) -> None:
    algo_version_repo = AlgoritmeVersionRepository(db)
    algo_version = algo_version_repo.get_by_id(version_id)
    if not algo_version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Er is geen algoritmeversie gevonden met ID: ({version_id})",
        )
    new_state = State.ARCHIVED if archived else State.STATE_1
    algo_version_repo.update_state_by_id(version_id, new_state)

    action_history_repo = ActionHistoryRepository(db)
    action_history_repo.add(
        schemas.ActionHistoryIn(
            algoritme_version_id=algo_version.id,
            operation=OperationEnum.archived if archived else OperationEnum.unarchived,
            user_id=user_id,
        )
    )
