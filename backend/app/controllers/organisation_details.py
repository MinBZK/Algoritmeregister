from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.repositories import OrganisationDetailsRepository, AlgoritmeVersionRepository
from app.repositories.organisation import OrganisationRepository
from app.schemas.misc import Language
from app.services import translation
from app.services.translation import LanguageCode


def get_org_page_info(
    db: Session, org_id: str, lang: Language
) -> schemas.OrganisationDetailsPage:
    org_details_repo = OrganisationDetailsRepository(db)
    algoritme_version_repo = AlgoritmeVersionRepository(db)

    org_algorithms = algoritme_version_repo.get_published_by_org_by_lang(org_id, lang)
    algoritme_versions = [
        schemas.AlgoritmeVersionQuery(**algo.model_dump()) for algo in org_algorithms
    ]

    org_details = org_details_repo.get_shown_by_org_id_by_lang(org_id, lang)
    if org_details:
        return schemas.OrganisationDetailsPage(
            **dict(org_details), algoritme_versions=algoritme_versions
        )

    org_config = org_details_repo.get_org_configs_by_org_id_by_lang(org_id, lang)
    if not org_config:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "ORG_NOT_FOUND")

    return schemas.OrganisationDetailsPage(
        name=org_config.name,
        show_page=org_config.show_page,
        algoritme_versions=algoritme_versions,
    )


def get_org_detail(db: Session, as_org: str) -> schemas.OrganisationDetailsDB:
    org_detail_repo = OrganisationDetailsRepository(db)
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_org_id(as_org)
    if not org:
        raise HTTPException(404)
    org_detail = org_detail_repo.get_by_org_id_by_lang(org.id, Language.NLD)
    return schemas.OrganisationDetailsDB.model_validate(org_detail)


def update_org_details(
    background_tasks: BackgroundTasks,
    db: Session,
    as_org: str,
    organisation_detail: schemas.OrganisationDetailsUpdatable,
) -> schemas.OrganisationDetailsDB:
    org_detail_repo = OrganisationDetailsRepository(db)
    org_repo = OrganisationRepository(db)
    org = org_repo.get_by_org_id(as_org)
    if not org:
        raise HTTPException(404)
    org_detail = org_detail_repo.get_by_org_id_by_lang(org.id, Language.NLD)
    if not org_detail:
        raise HTTPException(404)

    org_detail_in = schemas.OrganisationDetailsIn.model_validate(org_detail)
    org_detail_in.about = organisation_detail.about
    org_detail_in.contact_info = organisation_detail.contact_info
    filtered_data = org_detail_in.model_dump(
        exclude={"show_page", "code", "type", "org_id"}
    )
    record = org_detail_repo.update_by_id(
        org_detail.id, schemas.OrganisationDetailsIn.model_validate(filtered_data)
    )

    # Translate about to english
    background_tasks.add_task(
        translate_org_details,
        db,
        org.id,
        organisation_detail,
        org_detail.name,
        LanguageCode.ENGLISH,
    )
    background_tasks.add_task(
        translate_org_details,
        db,
        org.id,
        organisation_detail,
        org_detail.name,
        LanguageCode.FRISIAN,
    )
    return schemas.OrganisationDetailsDB.model_validate(record)


def translate_org_details(
    db: Session,
    org_id: int,
    organisation_detail: schemas.OrganisationDetailsUpdatable,
    org_name: str,
    lang: LanguageCode = LanguageCode.ENGLISH,
) -> None:
    org_detail_repo = OrganisationDetailsRepository(db)

    lang_code_map = {
        LanguageCode.ENGLISH: Language.ENG,
        LanguageCode.FRISIAN: Language.FRY,
    }
    auto_translator = translation.AutoTranslator(
        field_dict={"about": organisation_detail.about},
        target_lang=lang,
        organisation_name=org_name,
    )
    translation_response = auto_translator.translate()
    if not translation_response.fields:
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY,
            detail="Translation for field 'about' failed.",
        )
    about_translated = translation_response.fields.get("about", "")
    if not isinstance(about_translated, str):
        raise HTTPException(
            status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"Translation to {lang_code_map[lang].value} failed for field {'about'}, "
            f" got: {translation_response.fields.get('about', '')}.",
        )

    org_detail_translated = org_detail_repo.get_by_org_id_by_lang(
        org_id, lang_code_map[lang]
    )
    if not org_detail_translated:
        raise HTTPException(
            409,
            "Application has conflicting DB state, please contact administrator",
        )

    org_detail_in_translated = schemas.OrganisationDetailsIn.model_validate(
        org_detail_translated
    )
    org_detail_in_translated.about = about_translated
    org_detail_in_translated.contact_info = organisation_detail.contact_info

    org_detail_repo.update_by_id(org_detail_translated.id, org_detail_in_translated)
