from sqlalchemy.orm import Session
from sqlalchemy import and_, func, ColumnElement
from app import models, schemas, repositories


def prep_search_for_query(search_query_value: str) -> str:
    adjusted_search_query = search_query_value.replace(" of ", " or ")
    return adjusted_search_query


def get_basic_search_clause(searchtext: str) -> ColumnElement[bool]:
    return models.AlgoritmeVersion.vector.op("@@")(
        func.websearch_to_tsquery(schemas.Language.NLD.value, searchtext)
    )


def get_similarity_search_clause(db: Session, searchtext: str) -> ColumnElement[bool]:
    """
    Full text search query based on concatenation of a set of words from the 'words' table.
    The words are selected if their similarity is greater then the threshold when compared to the search value.
    """
    similarity_threshold = 0.4
    # similarity threshold is set to 0.4 because it returns good results

    subquery = (
        db.query(
            func.websearch_to_tsquery(
                schemas.Language.NLD.value, func.string_agg(models.Words.word, " or ")
            )
        )
        .filter(func.similarity(models.Words.word, searchtext) > similarity_threshold)
        .as_scalar()
    )
    return models.AlgoritmeVersion.vector.op("@@")(subquery)


def perform_smart_search(
    algoritme_query, db, language
) -> schemas.AlgoritmeQueryResponse:
    algoritme_version_repo = repositories.AlgoritmeVersionRepository(db)
    org_repo = repositories.OrganisationRepository(db)

    searchtext = prep_search_for_query(algoritme_query.searchtext)
    organisation = algoritme_query.organisation
    limit = algoritme_query.limit
    page = algoritme_query.page
    offset = (page - 1) * limit

    selected_filters = []

    filter = []
    filter.append(models.AlgoritmeVersion.published)
    filter.append(models.AlgoritmeVersion.language == language)

    if organisation:
        selected_filters.append(
            schemas.SelectedFilters(name="organisation", value=organisation)
        )
        filter.append(models.AlgoritmeVersion.organization == organisation)

    if searchtext:
        selected_filters.append(
            schemas.SelectedFilters(name="searchtext", value=algoritme_query.searchtext)
        )

        filter.append(get_basic_search_clause(searchtext))

    # Last entry is the search filter!!
    filter_clause = and_(*filter)

    # Perform query
    results = algoritme_version_repo.get_published_by_filter(
        filter_clause, offset, limit
    )
    if len(results) == 0 and searchtext:
        # If a searchtext is given, we use similarity search in case of no results. Replace basic search on last entry:
        filter[-1] = get_similarity_search_clause(db, searchtext)
        filter_clause = and_(*filter)
        results = algoritme_version_repo.get_published_by_filter(
            filter_clause, offset, limit
        )

    # Get all the records -> limit set to a random big number.
    total_count = len(
        algoritme_version_repo.get_published_by_filter(filter_clause, 0, 99999999)
    )
    organisations = org_repo.get_aggregated_organisations_by_filter(filter_clause)

    filter_data = schemas.FilterData(organisation=organisations)

    return schemas.AlgoritmeQueryResponse(
        results=results,
        total_count=total_count,
        filter_data=filter_data,
        selected_filters=selected_filters,
    )


def perform_suggestion_search(
    searchtext: str, db: Session, language: schemas.Language
) -> schemas.SearchSuggestionResponse:
    algoritme_version_repo = repositories.AlgoritmeVersionRepository(db)

    filter = []
    filter.append(models.AlgoritmeVersion.published)
    filter.append(models.AlgoritmeVersion.language == language)

    if searchtext:
        filter.append(get_basic_search_clause(searchtext))

    filter_clause = and_(*filter)

    results = algoritme_version_repo.get_published_by_filter(filter_clause)

    return schemas.SearchSuggestionResponse(algorithms=results)
