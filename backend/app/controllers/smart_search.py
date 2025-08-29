from sqlalchemy.orm import Session
from sqlalchemy import and_, func, ColumnElement, cast, String, or_, not_
from sqlalchemy.dialects.postgresql import JSONB
from app import models, schemas, repositories
from app.middleware.authorisation.schemas import State
from app.schemas.misc import Language, standard_impact_assessment_titles_mapping
from app.config.org_type_mapping import org_type_mapping


def prep_search_for_query(search_query_value: str) -> str:
    adjusted_search_query = search_query_value.replace(" of ", " or ")
    return adjusted_search_query


def get_basic_search_clause(searchtext: str, language: Language) -> ColumnElement[bool]:
    return models.AlgoritmeVersion.vector.op("@@")(
        func.websearch_to_tsquery(language.value, searchtext)
    )


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
    return models.AlgoritmeVersion.vector.op("@@")(subquery)


def perform_smart_search(
    algoritme_query: schemas.algoritme_version.AlgoritmeQuery,
    db: Session,
    language: Language,
) -> schemas.AlgoritmeQueryResponse:
    algoritme_version_repo = repositories.AlgoritmeVersionRepository(db)
    org_repo = repositories.OrganisationRepository(db)

    searchtext = prep_search_for_query(algoritme_query.searchtext)
    organisation = algoritme_query.organisation
    publicationcategory = algoritme_query.publicationcategory
    organisationtype = algoritme_query.organisationtype
    impact_assessment = algoritme_query.impact_assessment
    sort_option = algoritme_query.sort_option

    limit = algoritme_query.limit
    page = algoritme_query.page
    offset = (page - 1) * limit

    selected_filters = []

    query_filters = []
    query_filters.append(models.AlgoritmeVersion.state == State.PUBLISHED)
    query_filters.append(models.AlgoritmeVersion.language == language)

    if organisationtype:
        selected_filters.append(
            schemas.SelectedFilters(
                key="organisationtype",
                value=org_type_mapping[language][organisationtype],
            )
        )
        query_filters.append(models.Organisation.type == organisationtype)

    if publicationcategory:
        selected_filters.append(
            schemas.SelectedFilters(
                key="publicationcategory", value=publicationcategory
            )
        )
        query_filters.append(
            models.AlgoritmeVersion.publication_category == publicationcategory
        )

    if organisation:
        selected_filters.append(
            schemas.SelectedFilters(key="organisation", value=organisation)
        )
        query_filters.append(models.AlgoritmeVersion.organization == organisation)

    if impact_assessment:
        impact_label = standard_impact_assessment_titles_mapping[language][
            impact_assessment
        ]
        selected_filters.append(
            schemas.SelectedFilters(
                key="impact_assessment",
                value=impact_label,
            )
        )
        ia_query_filters = get_impact_assessment_filters(
            impact_assessment, db, language
        )
        query_filters.extend(ia_query_filters)

    if searchtext:
        selected_filters.append(
            schemas.SelectedFilters(key="searchtext", value=algoritme_query.searchtext)
        )

        query_filters.append(get_basic_search_clause(searchtext, language))

    # Last entry is the search filter!!
    filter_clause = and_(*query_filters)

    # Perform query
    results = algoritme_version_repo.get_published_by_filter(
        filter_clause, offset, limit
    )
    if len(results) == 0 and searchtext:
        # If a searchtext is given, we use similarity search in case of no results. Replace basic search on last entry:
        query_filters[-1] = get_similarity_search_clause(db, searchtext, language)
        filter_clause = and_(*query_filters)
        results = algoritme_version_repo.get_published_by_filter(
            filter_clause, offset, limit
        )

    # Get all the records -> limit set to a random big number.
    total_count = len(
        algoritme_version_repo.get_published_by_filter(filter_clause, 0, 99999999)
    )
    (
        org_filterdata,
        orgtype_filterdata,
    ) = org_repo.get_aggregated_organisations_by_filter_by_lang(
        filter_clause,
        sort_opt=sort_option,
        lang=language,
    )
    publicationcategory_filterdata = (
        algoritme_version_repo.get_pubcat_by_filter_by_lang(
            filter_clause, lang=language
        )
    )
    impact_assessment_filterdata = (
        algoritme_version_repo.get_impact_assessments_by_filter_by_lang(
            filter_clause, lang=language
        )
    )

    filter_data = schemas.AlgoritmeFilterData(
        organisation=org_filterdata,
        publicationcategory=publicationcategory_filterdata,
        impact_assessment=impact_assessment_filterdata,
        organisationtype=orgtype_filterdata,
    )

    return schemas.AlgoritmeQueryResponse(
        results=results,
        total_count=total_count,
        filter_data=filter_data,
        selected_filters=selected_filters,
    )


def get_impact_assessment_filters(
    impact_assessment: schemas.ImpactAssessments,
    db: Session,
    language: Language,
) -> list[ColumnElement[bool]]:
    """
    Add filters for impact assessment to the query filters.

    Checks for the following pattern: ...{"<TITLE>": "<LINK>"}...
    """
    ia_query_filters = []
    grouping_pattern_subfilter = cast(
        models.AlgoritmeVersion.impacttoetsen_grouping, String
    ).like("%{%:%}%")
    if impact_assessment == schemas.ImpactAssessments.NONE:
        ia_query_filters.append(
            or_(
                models.AlgoritmeVersion.impacttoetsen_grouping.is_(None),
                not_(grouping_pattern_subfilter),
            )
        )
    else:
        ia_query_filters.append(grouping_pattern_subfilter)

    if impact_assessment in schemas.misc.standard_impact_assessment_titles:
        impact_label = standard_impact_assessment_titles_mapping[language][
            impact_assessment
        ]
        ia_query_filters.append(
            models.AlgoritmeVersion.impacttoetsen_grouping.cast(JSONB).contains(
                [{"title": impact_label}]
            )
        )

    if impact_assessment == schemas.ImpactAssessments.OTHER:
        reverse_mapping = schemas.misc.reverse_impact_assessment_titles_mapping[
            language
        ]
        overview_impacttoetsen = (
            db.query(
                models.AlgoritmeVersion.impacttoetsen_grouping,
                models.AlgoritmeVersion.algoritme_id,
            )
            .filter(
                models.AlgoritmeVersion.language == language,
                models.AlgoritmeVersion.state == State.PUBLISHED,
            )
            .all()
        )
        matching_ids = []

        for impacttoetsen_grouping, algoritme_id in overview_impacttoetsen:
            if impacttoetsen_grouping is not None:
                contains_standard = False
                contains_custom = False

                for assessment in impacttoetsen_grouping:
                    title = assessment.get("title")
                    enum_key = reverse_mapping.get(title)
                    if enum_key in schemas.misc.standard_impact_assessment_titles:
                        contains_standard = True
                    else:
                        contains_custom = True
                if contains_custom and (not contains_standard or contains_standard):
                    matching_ids.append(algoritme_id)

        if matching_ids:
            ia_query_filters.append(
                models.AlgoritmeVersion.algoritme_id.in_(matching_ids)
            )

    return ia_query_filters


def perform_suggestion_search(
    searchtext: str, db: Session, language: Language
) -> schemas.SearchSuggestionResponse:
    algoritme_version_repo = repositories.AlgoritmeVersionRepository(db)

    query_filters = []
    query_filters.append(models.AlgoritmeVersion.state == State.PUBLISHED)
    query_filters.append(models.AlgoritmeVersion.language == language)

    if searchtext:
        query_filters.append(get_basic_search_clause(searchtext, language))

    filter_clause = and_(*query_filters)

    results = algoritme_version_repo.get_published_by_filter(filter_clause)
    results = [schemas.SearchSuggestionAlgorithms(**dict(result)) for result in results]

    return schemas.SearchSuggestionResponse(algorithms=results)
