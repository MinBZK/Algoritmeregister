from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, ColumnElement
from app.repositories.organisation import OrganisationRepository
from app.services.keycloak.repository import KeycloakRepository
from app.middleware import kc_settings
from app.schemas.algoritme_version import FilterData
from app.schemas.misc import Language, OrgType
from app.config.org_type_mapping import org_type_mapping


def build_org_filter_data_by_lang(
    organisations: list[schemas.OrganisationOverview], language: Language
) -> list[schemas.FilterData]:
    uniq_org_types = set([OrgType[r.type] for r in organisations])
    orgtype_dict: dict[OrgType, int] = {orgtype: 0 for orgtype in uniq_org_types}
    for org in organisations:
        orgtype_dict[org.type] += 1

    result = [
        FilterData(
            key=orgtype,
            label=org_type_mapping[language][orgtype],
            count=count,
        )
        for orgtype, count in orgtype_dict.items()
    ]
    result.sort(key=lambda x: x.count, reverse=True)
    return result


def get_basic_search_clause(searchtext: str, language: Language) -> ColumnElement[bool]:
    return models.OrganisationDetails.vector.op("@@")(
        func.websearch_to_tsquery(language.value, searchtext)
    )


def prep_search_for_query(search_query_value: str) -> str:
    adjusted_search_query = search_query_value.replace(" of ", " or ")
    return adjusted_search_query


def get_similarity_search_clause(
    db: Session, searchtext: str, language: Language
) -> ColumnElement[bool]:
    """
    Full text search query based on concatenation of a set of words from the 'words' table.
    The words are selected if their similarity is greater then the threshold when compared to the search value.
    """
    similarity_threshold = 0.4
    # similarity threshold is set to 0.4 because it returns good results

    subquery = (
        db.query(
            func.websearch_to_tsquery(
                language.value, func.string_agg(models.Words.word, " or ")
            )
        )
        .filter(func.similarity(models.Words.word, searchtext) > similarity_threshold)
        .as_scalar()
    )
    return models.OrganisationDetails.vector.op("@@")(subquery)


def get_orgs_count(db: Session, language: Language) -> int:
    org_repo = OrganisationRepository(db)
    data = org_repo.get_overview_by_lang(language)
    total_count = len(data)
    return total_count


def get_orgs_by_query(
    db: Session, query: schemas.OrganisationQuery, language: Language
) -> schemas.OrganisationQueryResponse:
    org_type = query.organisationtype
    page = query.page
    searchtext = query.searchtext
    if searchtext:
        searchtext = prep_search_for_query(searchtext)
    limit = min(query.limit, 20)
    offset = (page - 1) * limit

    filter_clauses = []
    selected_filters = []
    if org_type:
        selected_filters.append(
            schemas.SelectedFilters(
                key="organisationtype", value=org_type_mapping[language][org_type]
            )
        )
    if searchtext:
        selected_filters.append(
            schemas.SelectedFilters(key="searchtext", value=searchtext)
        )
        filter_clauses.append(get_basic_search_clause(searchtext, language))
    filter_clause = and_(*filter_clauses)

    org_repo = OrganisationRepository(db)
    data = org_repo.get_overview_by_type_by_lang(org_type, language, filter_clause)

    if len(data) == 0 and searchtext:
        # If a searchtext is given, we use similarity search in case of no results. Replace basic search on last entry:
        filter_clauses[-1] = get_similarity_search_clause(db, searchtext, language)
        filter_clause = and_(*filter_clauses)
        data = org_repo.get_overview_by_type_by_lang(org_type, language, filter_clause)

    total_count = len(data)
    data.sort(key=lambda x: x.count, reverse=True)
    results = data[offset : offset + limit]  # noqa
    organisationtype_filterdata = build_org_filter_data_by_lang(data, language)

    filter_data = schemas.OrganisationFilterData(
        organisationtype=organisationtype_filterdata
    )

    return schemas.OrganisationQueryResponse(
        results=results,
        total_count=total_count,
        filter_data=filter_data,
        selected_filters=selected_filters,
    )


def get_all_organisations_joined_date() -> list[schemas.OrganisationJoinedDate]:
    """
    Returns a list of all organisations and their 'aansluitdatum';
    This is the date that the oldest account associated with them was first created.
    """
    kc_repo = KeycloakRepository(kc_settings)
    all_users = kc_repo.get_all()

    organisation_oldest_date = {}
    for user in all_users:
        groups = user.groups
        created_at = user.created_at
        for group in groups:
            if group not in organisation_oldest_date:
                organisation_oldest_date[group] = created_at
            elif created_at < organisation_oldest_date[group]:
                organisation_oldest_date[group] = created_at

    formatted_organisation_dates = [
        schemas.OrganisationJoinedDate(code=code, create_dt=date)
        for code, date in organisation_oldest_date.items()
    ]

    return formatted_organisation_dates
