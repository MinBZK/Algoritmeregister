from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session
from app import schemas, controllers, repositories
from app.middleware.middleware import get_db
from app.schemas.misc import Language
from app.config.org_name_mapping import org_name_mapping


router = APIRouter()


@router.post("/organisation/{language}")
async def get_some_orgs_overview(
    query: schemas.OrganisationQuery,
    language: Language = Path(alias="language"),
    db: Session = Depends(get_db),
) -> schemas.OrganisationQueryResponse:
    return controllers.get_orgs_by_query(db, query, language)


@router.get("/organisation-count/{language}")
async def get_orgs_count(
    db: Session = Depends(get_db),
    language: Language = Path(alias="language"),
) -> int:
    return controllers.get_orgs_count(db, language)


@router.get("/organisation/{org_code}")
async def get_org_id_by_org_code(
    db: Session = Depends(get_db),
    org_code: str = Path(alias="org_code"),
) -> schemas.OrganisationCodeResponse:
    return controllers.get_org_id_by_org_code(db, org_code)


@router.get("/organisation-relation/{org_id}")
async def get_org_relation_based_on_org_id(
    db: Session = Depends(get_db),
    org_id: str = Path(alias="org_id"),
) -> schemas.OrganisationRelationResponse:
    return controllers.get_org_relation_based_on_org_id(db, org_id)


@router.get("/organisation/{language}/{search}")
async def get_elaborate_organisation(
    search: str = "",
    language: Language = Path(alias="language"),
    db: Session = Depends(get_db),
) -> schemas.OrganisationSearchSuggestionResponse | None:
    org_repo = repositories.OrganisationRepository(db)
    results = org_repo.get_overview_by_lang(language)
    organisation_details = [
        schemas.OrganisationMappingResult(
            code=result.code,
            name=result.name,
            org_id=result.org_id,
            show_page=result.show_page,
            count=result.count,
        )
        for result in results
        if search.lower() in result.name.lower()
    ]
    results_from_mapping = org_name_mapping.get(language, {}).get(search.lower(), {})

    if results_from_mapping:
        mapped_org = schemas.OrganisationMappingResult(
            name=results_from_mapping["name"], code=results_from_mapping["code"]
        )
        return schemas.OrganisationSearchSuggestionResponse(organisations=[mapped_org])
    elif organisation_details:
        return schemas.OrganisationSearchSuggestionResponse(
            organisations=organisation_details
        )
