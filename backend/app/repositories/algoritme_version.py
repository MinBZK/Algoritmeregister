from sqlalchemy.orm import Session
from sqlalchemy import (
    desc,
    exists,
    func,
    and_,
    or_,
    update,
    ColumnElement,
    select,
    not_,
    cast,
    Numeric,
)
from app import models, schemas
from app.middleware.authorisation.schemas import State
from app.models.algoritme_version import AlgoritmeVersion
from app.schemas.algoritme_version import FilterData
from app.schemas.misc import (
    ImpactAssessments,
    Language,
    ImpacttoetsenGrouping,
    OperationEnum,
)
from app.schemas.algoritme_version import AlgoritmeVersionEarliestPublish
from .index import IRepository
from app.services.algoritme_version import (
    db_list_to_python_list_schema,
)
from app.schemas.misc import standard_impact_assessment_titles
from app.config.publication_standard import publication_standard


def process_impact_assessment_filters(
    impact_assessments_by_algo: list[list[ImpacttoetsenGrouping] | None],
) -> list[FilterData]:
    """Processes the impact assessment filters to remove duplicates and return a list of strings."""
    ia_filter_data: list[FilterData] = []

    # Counts and removes the amount of entries without any impact assessments.
    algo_ia_data_not_none = [ia for ia in impact_assessments_by_algo if ia is not None]
    count_with_none = len(impact_assessments_by_algo) - len(algo_ia_data_not_none)
    if count_with_none > 0:
        ia_filter_data.append(
            FilterData(
                label=ImpactAssessments.NONE,
                key=ImpactAssessments.NONE,
                count=count_with_none,
            )
        )

    # Counts the standard Impact Assessments.
    standard_ia_counts = {sia: 0 for sia in standard_impact_assessment_titles}
    total_other_ias = 0
    for ia_data in algo_ia_data_not_none:
        # 'OTHER' can occur twice in one algorithm, but we only count it max once.
        other_ias_found = False
        for ia in ia_data:
            if ia["title"] in standard_impact_assessment_titles:
                standard_ia_counts[ImpactAssessments(ia["title"])] += 1
                continue
            elif not other_ias_found:
                total_other_ias += 1
                other_ias_found = True

    for standard_ia, count in standard_ia_counts.items():
        if count > 0:
            ia_filter_data.append(
                FilterData(label=standard_ia, key=standard_ia, count=count)
            )

    # 'Other' are the leftovers, the ones not caught by standard Impact Assessments.
    if total_other_ias > 0:
        ia_filter_data.append(
            FilterData(
                label=schemas.ImpactAssessments.OTHER,
                key=schemas.ImpactAssessments.OTHER,
                count=total_other_ias,
            )
        )

    ia_filter_data.sort(key=lambda x: x.count, reverse=True)
    return ia_filter_data


class AlgoritmeVersionRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> schemas.AlgoritmeVersionDB | None:
        algoritme_version = self.session.query(models.AlgoritmeVersion).get(id)
        if algoritme_version:
            return schemas.AlgoritmeVersionDB.from_orm(algoritme_version)

    def get_all(self) -> list[schemas.AlgoritmeVersionDB]:
        algoritme_versions = self.session.query(models.AlgoritmeVersion).all()
        return [schemas.AlgoritmeVersionDB.from_orm(a) for a in algoritme_versions]

    def get_all_published(self) -> list[schemas.AlgoritmeVersionDB]:
        algoritme_versions = (
            self.session.query(models.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.state == State.PUBLISHED)
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(a))
            for a in algoritme_versions
        ]

    def get_all_published_first_version(self) -> list[AlgoritmeVersionEarliestPublish]:
        """
        Returns the first publication date of each published algorithm.
        """
        all_published_algos = (
            select(models.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.state == State.PUBLISHED)
            .subquery()
        )

        # Subquery finds the first publication date of each published algorithm
        subquery = (
            select(
                func.min(models.ActionHistory.create_dt).label("create_dt"),
                models.AlgoritmeVersion.algoritme_id,
            )
            .join(
                models.ActionHistory,
                models.AlgoritmeVersion.id == models.ActionHistory.algoritme_version_id,
            )
            .where(
                models.ActionHistory.operation == OperationEnum.published,
                models.AlgoritmeVersion.language == Language.NLD,
                exists(
                    select(all_published_algos.c.algoritme_id).where(
                        all_published_algos.c.algoritme_id
                        == models.AlgoritmeVersion.algoritme_id
                    )
                ),
            )
            .group_by(models.AlgoritmeVersion.algoritme_id)
            .order_by(
                func.min(models.ActionHistory.create_dt),
                models.AlgoritmeVersion.algoritme_id,
            )
            .subquery()
        )

        # This query couples all the requested data with the first publication date.
        stmt = (
            select(
                subquery.c.create_dt,
                subquery.c.algoritme_id,
                models.AlgoritmeVersion.organization,
                models.Organisation.code,
            )
            .select_from(models.AlgoritmeVersion)
            .join(
                models.ActionHistory,
                models.AlgoritmeVersion.id == models.ActionHistory.algoritme_version_id,
            )
            .join(
                models.Algoritme,
                models.AlgoritmeVersion.algoritme_id == models.Algoritme.id,
            )
            .join(
                models.Organisation,
                models.Algoritme.organisation_id == models.Organisation.id,
            )
            .join(
                subquery,
                and_(
                    subquery.c.create_dt == models.ActionHistory.create_dt,
                    subquery.c.algoritme_id == models.AlgoritmeVersion.algoritme_id,
                ),
            )
        )
        results = self.session.execute(stmt)
        return [AlgoritmeVersionEarliestPublish.from_orm(a) for a in results]

    def get_published_by_filter(
        self,
        filter: ColumnElement[bool],
        offset: int = 0,
        limit: int = 10,
    ) -> list[schemas.AlgoritmeVersionQuery]:
        algoritme_versions = (
            self.session.query(models.AlgoritmeVersion)
            .select_from(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .join(models.Organisation)
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .filter(filter, models.AlgoritmeVersion.state == State.PUBLISHED)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionQuery.from_orm(a))
            for a in algoritme_versions
        ]

    def get_all_published_by_pubcat(
        self, lang: Language
    ) -> list[schemas.PublicationCategoryCount]:
        publication_categories = (
            self.session.query(
                func.count(models.AlgoritmeVersion.algoritme_id),
                models.AlgoritmeVersion.publication_category,
            )
            .filter(
                models.AlgoritmeVersion.state == State.PUBLISHED,
                cast(models.AlgoritmeVersion.standard_version, Numeric(10, 2))
                == publication_standard["preferredVersion"],
                models.AlgoritmeVersion.language == lang,
            )
            .group_by(models.AlgoritmeVersion.publication_category)
            .all()
        )
        return [
            schemas.PublicationCategoryCount(category=label, count=count)
            for count, label in publication_categories
        ]

    def get_pubcat_by_filter_by_lang(
        self, filter: ColumnElement[bool], lang: Language
    ) -> list[schemas.FilterData]:
        publication_categories = (
            self.session.query(
                func.count(models.AlgoritmeVersion.id),
                models.AlgoritmeVersion.publication_category,
            )
            .join(models.Algoritme)
            .join(models.Organisation)
            .filter(
                models.AlgoritmeVersion.language == lang,
                models.AlgoritmeVersion.publication_category.is_not(None),
                filter,
            )
            .group_by(models.AlgoritmeVersion.publication_category)
            .all()
        )
        publication_categories_results = [
            schemas.FilterData(label=cat[1], key=cat[1], count=cat[0])
            for cat in publication_categories
        ]
        publication_categories_results.sort(key=lambda x: x.count, reverse=True)
        return publication_categories_results

    def get_impact_assessments_by_filter_by_lang(
        self, filter: ColumnElement[bool], lang: Language
    ) -> list[schemas.FilterData]:
        impact_assessments = (
            self.session.query(models.AlgoritmeVersion.impacttoetsen_grouping)
            .join(models.Algoritme)
            .join(models.Organisation)
            .filter(
                models.AlgoritmeVersion.language == lang,
                filter,
            )
            .all()
        )
        # Validation happens in a nested list, unless there is no nested list.
        validated = [
            [ImpacttoetsenGrouping(**i) for i in ia[0]] if ia[0] else None
            for ia in impact_assessments
        ]
        return process_impact_assessment_filters(validated)

    def get_latest_by_lars_by_lang(
        self, lars: str, lang: Language
    ) -> schemas.AlgoritmeVersionDB | None:
        latest_algo = (
            self.session.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.language == lang,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
        ).first()
        if latest_algo:
            latest_algo = schemas.AlgoritmeVersionDB.from_orm(latest_algo)
            return db_list_to_python_list_schema(latest_algo)

    def get_published_by_lang(self, lang: Language) -> list[schemas.AlgoritmeVersionDB]:
        published_algoritmes = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.language == lang,
                models.AlgoritmeVersion.state == State.PUBLISHED,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_algoritmes
        ]

    def get_latest_by_lang(self, lang: Language) -> list[schemas.AlgoritmeVersionDB]:
        latest_all_algo_summary = (
            self.session.query(
                models.AlgoritmeVersion.algoritme_id,
                func.max(models.AlgoritmeVersion.create_dt).label("max_creation_dt"),
            )
            .group_by(models.AlgoritmeVersion.algoritme_id)
            .subquery()
        )
        latest_all_algoritmes = (
            self.session.query(models.AlgoritmeVersion)
            .join(
                latest_all_algo_summary,
                and_(
                    models.AlgoritmeVersion.algoritme_id
                    == latest_all_algo_summary.c.algoritme_id,
                    models.AlgoritmeVersion.create_dt
                    == latest_all_algo_summary.c.max_creation_dt,
                ),
            )
            .filter(
                models.AlgoritmeVersion.language == lang,
            )
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in latest_all_algoritmes
        ]

    def get_latest_by_org_by_lang(
        self, as_org: str, lang: Language
    ) -> list[schemas.AlgoritmeVersionDB]:
        """For an organisation, returns the latest versions of all algoritmebeschrijvingen under them."""
        latest_all_algoritmes = (
            self.session.query(
                models.AlgoritmeVersion.algoritme_id,
                func.max(models.AlgoritmeVersion.create_dt).label("max_creation_dt"),
            )
            .group_by(models.AlgoritmeVersion.algoritme_id)
            .subquery()
        )
        latest_org_algoritmes = (
            self.session.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .join(models.Organisation)
            .join(
                latest_all_algoritmes,
                and_(
                    models.AlgoritmeVersion.algoritme_id
                    == latest_all_algoritmes.c.algoritme_id,
                    models.AlgoritmeVersion.create_dt
                    == latest_all_algoritmes.c.max_creation_dt,
                ),
            )
            .filter(
                models.Organisation.code == as_org,
                models.AlgoritmeVersion.language == lang,
            )
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in latest_org_algoritmes
        ]

    def get_published_by_lars(self, lars: str) -> list[schemas.AlgoritmeVersionDB]:
        """For a lars-code, returns all published"""
        published_alg = (
            self.session.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.AlgoritmeVersion.state == State.PUBLISHED,
                models.Algoritme.lars == lars,
            )
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_alg
        ]

    def get_published_by_lars_by_lang(
        self, lars: str, lang: Language
    ) -> schemas.AlgoritmeVersionDB | None:
        """For a lars-code, return published by language"""
        published_alg = (
            self.session.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.AlgoritmeVersion.state == State.PUBLISHED,
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.language == lang,
            )
            .first()
        )
        if published_alg:
            return db_list_to_python_list_schema(
                schemas.AlgoritmeVersionDB.from_orm(published_alg)
            )

    def get_published_by_org_by_lang(
        self, as_org, lang: Language
    ) -> list[schemas.AlgoritmeVersionDB]:
        """For an organisation, returns all published versions by language"""
        published_algos = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.state == State.PUBLISHED,
                models.AlgoritmeVersion.owner == as_org,
                models.AlgoritmeVersion.language == lang,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_algos
        ]

    def get_all_versions_by_lars_by_lang(
        self, lars: str, lang: Language
    ) -> list[schemas.AlgoritmeVersionLastEdit]:
        """
        Returns all versions of an algorithm description.
        Does additional joins to determine by who and when it was last edited.
        """
        join_clause = and_(
            models.ActionHistory.algoritme_version_id == models.AlgoritmeVersion.id,
            not_(models.AlgoritmeVersion.state == State.PUBLISHED),
            or_(
                models.ActionHistory.operation == schemas.OperationEnum.created,
                models.ActionHistory.operation == schemas.OperationEnum.new_version,
            ),
        )
        stmt = (
            select(
                models.ActionHistory.user_id,
                models.ActionHistory.create_dt,
                models.Algoritme.lars,
                models.AlgoritmeVersion,
            )
            .select_from(models.AlgoritmeVersion)
            .join(models.ActionHistory, onclause=join_clause)
            .join(models.Algoritme)
            .where(
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.language == lang,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .offset(1)  # Current version is skipped
        )
        result = list(self.session.execute(stmt))
        return [
            db_list_to_python_list_schema(
                schemas.AlgoritmeVersionLastEdit(
                    **r[3].__dict__, user_id=r[0], archive_dt=r[1], lars=r[2]
                )
            )
            for r in result
        ]

    def get_archive(
        self, org: str, lang: Language
    ) -> list[schemas.AlgoritmeVersionLastEdit]:
        """
        Returns the most recent archived versions for all algorithm descriptions of a particular organisation.
        """
        subquery = (
            select(
                models.ActionHistory.algoritme_version_id,
                func.max(models.ActionHistory.create_dt).label("max_create_dt"),
            )
            .filter(models.ActionHistory.operation == schemas.OperationEnum.archived)
            .group_by(models.ActionHistory.algoritme_version_id)
            .subquery()
        )

        stmt = (
            select(
                models.ActionHistory.user_id,
                models.ActionHistory.create_dt,
                models.Algoritme.lars,
                models.AlgoritmeVersion,
            )
            .select_from(models.AlgoritmeVersion)
            .join(
                models.ActionHistory,
                and_(
                    models.ActionHistory.algoritme_version_id
                    == models.AlgoritmeVersion.id,
                    models.ActionHistory.operation == schemas.OperationEnum.archived,
                    models.AlgoritmeVersion.state == State.ARCHIVED,
                ),
            )
            .join(
                subquery,
                and_(
                    subquery.c.algoritme_version_id
                    == models.ActionHistory.algoritme_version_id,
                    subquery.c.max_create_dt == models.ActionHistory.create_dt,
                ),
            )
            .join(models.Algoritme)
            .join(models.Organisation)
            .where(
                models.Organisation.code == org,
                models.AlgoritmeVersion.language == lang,
            )
            .order_by(desc(models.ActionHistory.create_dt))
        )

        result = list(self.session.execute(stmt))
        return [
            db_list_to_python_list_schema(
                schemas.AlgoritmeVersionLastEdit(
                    **r[3].__dict__, user_id=r[0], archive_dt=r[1], lars=r[2]
                )
            )
            for r in result
        ]

    def add(self, item: schemas.AlgoritmeVersionIn) -> schemas.AlgoritmeVersionDB:
        algoritme_version = models.AlgoritmeVersion(**item.dict())
        self.session.add(algoritme_version)
        self.session.commit()

        return schemas.AlgoritmeVersionDB.from_orm(algoritme_version)

    def update_state_by_id(self, alg_id: int, target_state: State) -> None:
        stmt = (
            update(models.AlgoritmeVersion)
            .where(AlgoritmeVersion.id == alg_id)
            .values({"state": target_state})
        )
        self.session.execute(stmt)
        self.session.commit()

    def update_by_id(self, id: int, item: schemas.AlgoritmeVersionIn) -> None:
        stmt = (
            update(models.AlgoritmeVersion)
            .where(models.AlgoritmeVersion.id == id)
            .values(**item.dict(exclude={"create_dt"}))
        )
        self.session.execute(stmt)
        self.session.commit()

    def preview_latest_by_lars(self, lars: str) -> schemas.AlgoritmeVersionDB | None:
        # Always NLD
        latest_algo = self.get_latest_by_lars_by_lang(lars, Language.NLD)
        if not latest_algo:
            return None

        _ = (
            self.session.query(models.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.id == latest_algo.id)
            .update(
                {models.AlgoritmeVersion.preview_active: True},
                synchronize_session="fetch",
            )
        )
        latest_algo.preview_active = True
        return latest_algo

    def unpreview_by_lars(self, lars: str) -> schemas.AlgoritmeVersionDB | None:
        # Always NLD
        preview_algo = (
            self.session.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.preview_active,
                models.AlgoritmeVersion.language == Language.NLD,
            )
            .first()
        )
        if not preview_algo:
            return

        _ = (
            self.session.query(models.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.id == preview_algo.id)
            .update(
                {models.AlgoritmeVersion.preview_active: False},
                synchronize_session="fetch",
            )
        )
        preview_algo.preview_active = False
        return preview_algo
