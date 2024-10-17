from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy import ColumnElement, delete, desc, func, select, update, or_, and_
from app import models, schemas
from app.middleware.authorisation.schemas import State
from app.models.organisation import Organisation
from app.schemas.algoritme_version import FilterData
from app.schemas.misc import Language, OrgType, SortOption
from app.schemas.organization import OrganisationTop20
from .index import IRepository
from app.config.org_type_mapping import org_type_mapping


class OrganisationRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.OrganisationDB]:
        all_orgs = self.session.query(models.Organisation).all()
        return [schemas.OrganisationDB.from_orm(one_org) for one_org in all_orgs]

    def delete_by_code(self, org_code: str) -> None:
        stmt = delete(Organisation).where(Organisation.code == org_code)
        self.session.execute(stmt)

    def gen_published_nl_algos(self):
        # Generates algoritme_version, but only published versions (and only dutch).
        # Used to count the coupled published algorithms.
        return (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.state == State.PUBLISHED,
                models.AlgoritmeVersion.language == Language.NLD,
            )
            .subquery()
        )

    def gen_all_org_counts(self, published_nl_algos):
        # Generates an overview for number of published algorithms for all organisations.
        return (
            self.session.query(
                models.Organisation.code,
                func.count(published_nl_algos.c.algoritme_id).label("count"),
            )
            .select_from(models.Organisation)
            .join(models.Algoritme, isouter=True)
            .join(
                published_nl_algos,
                published_nl_algos.c.algoritme_id == models.Algoritme.id,
                isouter=True,
            )
            .group_by(models.Organisation.code)
            .subquery()
        )

    def gen_organisation_details_lang(
        self, lang: Language, filter_clause: ColumnElement[bool] | None = None
    ):
        # Used to get the name of the organisation, but only in the requested language.
        if filter_clause is not None:
            return (
                self.session.query(models.OrganisationDetails)
                .filter(models.OrganisationDetails.language == lang)
                .filter(filter_clause)
                .subquery()
            )
        return (
            self.session.query(models.OrganisationDetails)
            .filter(models.OrganisationDetails.language == lang)
            .subquery()
        )

    def gen_conditional_org_counts(self, all_org_counts, organisation_details_lang):
        # Gets only the organisations that have (published algorithms or have a page), and comply with the type filter.
        return (
            self.session.query(
                models.Organisation.code,
                all_org_counts.c.count,
                organisation_details_lang.c.name,
                models.Organisation.show_page,
                models.Organisation.type,
            )
            .select_from(all_org_counts)
            .join(
                models.Organisation, models.Organisation.code == all_org_counts.c.code
            )
            .join(
                organisation_details_lang,
                organisation_details_lang.c.organisation_id == models.Organisation.id,
                isouter=True,
            )
            .filter(
                or_(all_org_counts.c.count > 0, models.Organisation.show_page),
                and_(organisation_details_lang.c.name.isnot(None)),
            )
        )

    def get_overview_by_lang(
        self, lang: Language
    ) -> list[schemas.OrganisationOverview]:
        published_nl_algos = self.gen_published_nl_algos()

        all_org_counts = self.gen_all_org_counts(published_nl_algos)

        organisation_details_lang = self.gen_organisation_details_lang(lang)

        conditional_org_counts = self.gen_conditional_org_counts(
            all_org_counts, organisation_details_lang
        )

        query = conditional_org_counts.order_by(organisation_details_lang.c.name).all()

        return [schemas.OrganisationOverview.from_orm(o) for o in query]

    def get_overview_by_type_by_lang(
        self,
        type: OrgType | None,
        lang: Language,
        filter_clause: ColumnElement[bool] | None,
    ) -> list[schemas.OrganisationOverview]:
        published_nl_algos = self.gen_published_nl_algos()

        all_org_counts = self.gen_all_org_counts(published_nl_algos)

        organisation_details_lang = self.gen_organisation_details_lang(
            lang, filter_clause
        )

        conditional_org_counts = self.gen_conditional_org_counts(
            all_org_counts, organisation_details_lang
        )

        if type:
            conditional_org_counts = conditional_org_counts.filter(
                models.Organisation.type == type
            )
        query = conditional_org_counts.order_by(organisation_details_lang.c.name).all()

        return [schemas.OrganisationOverview.from_orm(o) for o in query]

    def get_aggregated_organisations_by_filter_by_lang(
        self,
        filter: ColumnElement[bool],
        lang: Language,
        sort_opt: SortOption,
    ) -> Tuple[list[schemas.FilterData], list[schemas.FilterData]]:
        subquery = (
            self.session.query(
                models.Algoritme.organisation_id,
                func.count(models.Algoritme.id).label("count"),
            )
            .join(models.Organisation)
            .join(
                models.AlgoritmeVersion,
                models.AlgoritmeVersion.algoritme_id == models.Algoritme.id,
            )
            .filter(filter)
            .group_by(models.Algoritme.organisation_id)
            .subquery()
        )

        org_rows_model = (
            self.session.query(
                models.Organisation.type,
                models.OrganisationDetails.name,
                models.Organisation.code,
                subquery.c.count,
            )
            .select_from(models.Organisation)
            .join(
                subquery,
                models.Organisation.id == subquery.c.organisation_id,
            )
            .join(
                models.OrganisationDetails,
                and_(
                    models.Organisation.id
                    == models.OrganisationDetails.organisation_id,
                    models.OrganisationDetails.language == lang,
                ),
            )
        )

        org_rows = [schemas.OrganisationGrouping.from_orm(o) for o in org_rows_model]
        types_present = set([r.type for r in org_rows])
        orgtype_counts = {k: 0 for k in types_present if k is not None}
        org_results: list[schemas.FilterData] = []
        for org_row in org_rows:
            # Handles counting by organisation type.
            if org_row.type is None:
                orgtype_counts[schemas.OrgType.overig]
            else:
                orgtype_counts[org_row.type] += org_row.count

            # Handles counting by organisations.
            org = FilterData(label=org_row.name, key=org_row.name, count=org_row.count)
            org_results.append(org)

        orgtype_results = [
            FilterData(label=org_type_mapping[lang][key], key=key, count=count)
            for key, count in orgtype_counts.items()
        ]
        orgtype_results.sort(key=lambda x: x.count, reverse=True)
        if sort_opt == SortOption.sort_name:
            org_results.sort(key=lambda x: x.label)
        if sort_opt == SortOption.sort_number:
            org_results.sort(key=lambda x: x.count, reverse=True)

        return org_results, orgtype_results

    def add(self, item: schemas.OrganisationIn) -> schemas.OrganisationDB:
        organization = models.Organisation(**item.dict())
        self.session.add(organization)
        self.session.flush()

        return schemas.OrganisationDB.from_orm(organization)

    def get_by_code(self, code: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.code == code)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.from_orm(organisation)

    def get_by_name(self, name: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.name == name)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.from_orm(organisation)

    def get_by_lars(self, lars: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .join(models.Algoritme)
            .filter(models.Algoritme.lars == lars)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.from_orm(organisation)

    def get_by_id(self, org_id: int) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.id == org_id)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.from_orm(organisation)

    def get_by_type(self, type: OrgType) -> list[schemas.OrganisationDB]:
        orgs = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.type == type)
            .all()
        )
        return [schemas.OrganisationDB.from_orm(o) for o in orgs]

    def update_by_code(self, code: str, item: schemas.OrganisationIn) -> None:
        stmt = (
            update(models.Organisation)
            .where(models.Organisation.code == code)
            .values(**dict(item))
        )
        self.session.execute(stmt)
        self.session.commit()

    def get_top_20(self, language: Language) -> list[OrganisationTop20]:
        stmt = (
            select(func.count(models.Organisation.id), models.OrganisationDetails.name)
            .select_from(models.Organisation)
            .join(models.Algoritme)
            .join(
                models.AlgoritmeVersion,
                and_(
                    models.AlgoritmeVersion.algoritme_id == models.Algoritme.id,
                    models.AlgoritmeVersion.language == language,
                    models.AlgoritmeVersion.state == State.PUBLISHED,
                ),
            )
            .join(
                models.OrganisationDetails,
                and_(
                    models.Organisation.id
                    == models.OrganisationDetails.organisation_id,
                    models.OrganisationDetails.language == language,
                ),
            )
            .group_by(models.OrganisationDetails.name)
            .order_by(desc(func.count(models.Organisation.id)))
            .limit(20)
        )
        org_counts = self.session.execute(stmt).all()
        return [OrganisationTop20(name=o[1], count=o[0]) for o in org_counts]
