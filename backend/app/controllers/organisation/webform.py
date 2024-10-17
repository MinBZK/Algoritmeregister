from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.middleware.authorisation.schemas import Role
from app.repositories.organisation import OrganisationRepository
from app.repositories.organisation_details import OrganisationDetailsRepository
from app.schemas.misc import Language
from app.schemas.organization import (
    GetOrganisationsResponse,
    OrganisationConfig,
    OrganisationConfigIn,
)
from app.services.keycloak import KeycloakUser
from app.services import translation
from app.services.keycloak.repository import KeycloakRepository
from app.services.keycloak.schemas import KeycloakUserUpdate
from app.services.translation import LanguageCode
from app.middleware import kc_settings


def get_orgs(
    db: Session,
    user: KeycloakUser,
    limit: int | None = None,
    skip: int | None = None,
    q: str | None = None,
) -> GetOrganisationsResponse:
    org_details_repo = OrganisationDetailsRepository(db)
    # Gets orgs based on requested parameters. The limit is manual, to avoid doing 2 calls to DB.
    if Role.AllGroups in user.roles or Role.Administrator in user.roles:
        orgs = org_details_repo.get_org_configs_by_lang(Language.NLD, skip=skip, q=q)
    else:
        orgs = org_details_repo.get_org_configs_by_org_list_by_lang(
            user.groups, Language.NLD, skip=skip, q=q
        )
    return GetOrganisationsResponse(
        organisations=orgs[0:limit], count=len(orgs) + (skip or 0)
    )


def is_unique_code(db: Session, organisation: OrganisationConfigIn) -> bool:
    """Test for presence of the organisation code in the DB. If found, throws an HTTPException"""
    organisation_repo = OrganisationRepository(db)
    duplicate_code = organisation_repo.get_by_code(organisation.code)
    if duplicate_code is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CODE_TAKEN")
    return True


def is_unique_name(db: Session, config: OrganisationConfigIn) -> bool:
    """Test for presence of the organisation name in the DB. If found, throws an HTTPExcetion"""
    org_detail_repo = OrganisationDetailsRepository(db)
    duplicate_name = org_detail_repo.get_by_name(config.name)
    if duplicate_name is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NAME_TAKEN")
    return True


def create_org(
    background_tasks: BackgroundTasks, db: Session, config: OrganisationConfigIn
) -> OrganisationConfig:
    is_unique_name(db, config)
    is_unique_code(db, config)

    org_model = models.Organisation(
        type=config.type, code=config.code, flow=config.flow
    )
    db.add(org_model)
    db.flush()

    org_detail_model = models.OrganisationDetails(
        name=config.name, language=Language.NLD, organisation_id=org_model.id
    )
    db.add(org_detail_model)
    db.commit()

    org_detail_repo = OrganisationDetailsRepository(db)
    org_config = org_detail_repo.get_org_configs_by_code_by_lang(
        config.code, Language.NLD
    )
    if not org_config:
        raise HTTPException(status.HTTP_409_CONFLICT, "RECORD_NOT_FOUND")

    background_tasks.add_task(
        translate_org_name, db, org_config.name, org_config.id, LanguageCode.ENGLISH
    )
    background_tasks.add_task(
        translate_org_name, db, org_config.name, org_config.id, LanguageCode.FRISIAN
    )
    return org_config


def update_org(
    background_tasks: BackgroundTasks,
    db: Session,
    org_code: str,
    config: OrganisationConfigIn,
) -> OrganisationConfig:
    current_org_query = (
        db.query(
            models.Organisation.id,
            models.Organisation.code,
            models.Organisation.type,
            models.OrganisationDetails.name,
        )
        .join(
            models.Organisation,
            models.Organisation.id == models.OrganisationDetails.organisation_id,
        )
        .filter(
            models.OrganisationDetails.language == Language.NLD,
            models.Organisation.code == org_code,
        )
    )
    current_org = current_org_query.first()
    if not current_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ORG_NOT_FOUND"
        )

    if org_code != config.code:
        # On code change, test for uniqueness.
        is_unique_code(db, config)

    if current_org.name != config.name:
        # On name change, test for uniqueness.
        is_unique_name(db, config)

    db.query(models.Organisation).filter(models.Organisation.code == org_code).update(
        {
            models.Organisation.code: config.code,
            models.Organisation.type: config.type,
            models.Organisation.flow: config.flow,
        },
        synchronize_session=False,
    )
    db.query(models.OrganisationDetails).filter(
        models.OrganisationDetails.organisation_id == current_org.id,
        models.OrganisationDetails.language == Language.NLD,
    ).update({models.OrganisationDetails.name: config.name}, synchronize_session=False)
    # If update is succesful, and code changed, also update the rights of the users.
    if org_code != config.code:
        kc_repo = KeycloakRepository(kc_settings)
        users = kc_repo.get_all(group=org_code)
        for user in users:
            new_groups = [config.code] + [g for g in user.groups if g != org_code]
            updated_user = {**user.dict(), "groups": new_groups}
            kc_repo.update_user(user.id, KeycloakUserUpdate(**updated_user))

    db.commit()

    background_tasks.add_task(
        translate_org_name, db, config.name, current_org.id, LanguageCode.ENGLISH
    )
    background_tasks.add_task(
        translate_org_name, db, config.name, current_org.id, LanguageCode.FRISIAN
    )

    org_details_repo = OrganisationDetailsRepository(db)
    org_config = org_details_repo.get_org_configs_by_code_by_lang(
        config.code, Language.NLD
    )
    if not org_config:
        raise HTTPException(status.HTTP_409_CONFLICT, "RECORD_NOT_FOUND")
    return org_config


def remove_org(
    db: Session,
    org_code: str,
) -> None:
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_code(org_code)
    if not org:
        raise HTTPException(404)
    org_repo.delete_by_code(org_code)


def update_org_show_page(
    db: Session, org_code: str, show_page: bool
) -> OrganisationConfig:
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_code(org_code)
    if not org:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    org.show_page = show_page
    item = schemas.OrganisationIn.from_orm(org)
    org_repo.update_by_code(org.code, item)

    org_detail_repo = OrganisationDetailsRepository(db)
    org_config = org_detail_repo.get_org_configs_by_code_by_lang(org_code, Language.NLD)
    if not org_config:
        raise HTTPException(status.HTTP_409_CONFLICT, "RECORD_NOT_FOUND")
    return org_config


def translate_org_name(
    db: Session,
    org_name: str,
    org_id: int,
    target_lang: LanguageCode = LanguageCode.ENGLISH,
) -> None:
    org_details_repo = OrganisationDetailsRepository(db)

    # Load preprocessor class, because it has the default translations
    preprocessor = translation.Preprocessor(
        models.AlgoritmeVersion(), target_lang=target_lang.value
    )
    # key is organization, because the file is also written for algoritme_version, where the column has that name.
    field_dict = {"organization": org_name}
    default_translator = translation.DefaultValuesTranslator(
        field_dict=field_dict,
        target_lang=target_lang,
        organisation_name=org_name,
    )
    translation_response = default_translator.translate(
        preprocessor.translation_spec["default_translations"]
    )
    if not translation_response.fields:
        raise HTTPException(status.HTTP_424_FAILED_DEPENDENCY, "Translation failed")

    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }
    org_detail = org_details_repo.get_by_org_id_by_lang(
        org_id, lang_code_map[target_lang]
    )
    if not org_detail:
        org_details_in = schemas.OrganisationDetailsIn(
            about=None,
            contact_info=None,
            name=str(translation_response.fields["organization"]),
            organisation_id=org_id,
            language=lang_code_map[target_lang],
        )
        org_details_repo.add(org_details_in)
    else:
        org_details_in = schemas.OrganisationDetailsIn(**dict(org_detail))
        org_details_in.name = str(translation_response.fields["organization"])
        org_details_repo.update_by_id(org_detail.id, org_details_in)
