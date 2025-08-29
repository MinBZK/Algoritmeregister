from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy import (
    ColumnElement,
    delete,
    desc,
    func,
    select,
    update,
    or_,
    and_,
)
from app import models, schemas
from app.middleware.authorisation.schemas import State
from app.models.organisation import Organisation
from app.schemas.algoritme_version import FilterData
from app.schemas.misc import (
    Language,
    OrgType,
    OrganisationCluster,
    RelationWithMinistry,
    SortOption,
)
from app.schemas.organization import (
    OrganisationRelationHierarchy,
    OrganisationRelationResponse,
    OrganisationTop20,
    NationalOrganisationsCount,
    NationalOrganisationsCountDashboard,
)
from .index import IRepository
from app.config.org_type_mapping import org_type_mapping


class OrganisationRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.OrganisationDB]:
        all_orgs = self.session.query(models.Organisation).all()
        return [schemas.OrganisationDB.model_validate(one_org) for one_org in all_orgs]

    def delete_by_code(self, org_code: str) -> None:
        stmt = delete(Organisation).where(Organisation.code == org_code)
        self.session.execute(stmt)

    def delete_by_org_id(self, org_id: str) -> None:
        stmt = delete(Organisation).where(Organisation.org_id == org_id)
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
                models.Organisation.org_id,
                func.count(published_nl_algos.c.algoritme_id).label("count"),
            )
            .select_from(models.Organisation)
            .join(models.Algoritme, isouter=True)
            .join(
                published_nl_algos,
                published_nl_algos.c.algoritme_id == models.Algoritme.id,
                isouter=True,
            )
            .group_by(models.Organisation.code, models.Organisation.org_id)
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

    def gen_conditional_org_counts(
        self, all_org_counts, organisation_details_lang, published=False
    ):
        # Gets only the organisations that have (algorithms or have a page), and comply with the type filter.
        query = (
            self.session.query(
                models.Organisation.code,
                all_org_counts.c.count,
                organisation_details_lang.c.name,
                models.Organisation.show_page,
                models.Organisation.type,
                models.Organisation.org_id,
                models.Organisation.part_of,
                models.Organisation.relation_with_ministry,
            )
            .select_from(all_org_counts)
            .join(
                models.Organisation,
                models.Organisation.org_id == all_org_counts.c.org_id,
            )
            .join(
                organisation_details_lang,
                organisation_details_lang.c.organisation_id == models.Organisation.id,
                isouter=True,
            )
        )
        if published:
            query = query.filter(
                or_(all_org_counts.c.count > 0, models.Organisation.show_page),
                and_(organisation_details_lang.c.name.isnot(None)),
            )
        else:
            query = query.order_by(
                desc(all_org_counts.c.count), organisation_details_lang.c.name
            )
        return query

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

        return [schemas.OrganisationOverview.model_validate(o) for o in query]

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
            all_org_counts, organisation_details_lang, published=True
        )

        if type:
            conditional_org_counts = conditional_org_counts.filter(
                models.Organisation.type == type
            )
        query = conditional_org_counts.order_by(organisation_details_lang.c.name).all()

        return [schemas.OrganisationOverview.model_validate(o) for o in query]

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
                models.Organisation.org_id,
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

        org_rows = [
            schemas.OrganisationGrouping.model_validate(o) for o in org_rows_model
        ]
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
        organization = models.Organisation(**item.model_dump())
        self.session.add(organization)
        self.session.flush()

        return schemas.OrganisationDB.model_validate(organization)

    def get_by_code(self, code: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.code == code)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.model_validate(organisation)

    def get_by_org_id(self, org_id: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.org_id == org_id)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.model_validate(organisation)

    def get_by_name(self, name: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.name == name)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.model_validate(organisation)

    def get_by_lars(self, lars: str) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .join(models.Algoritme)
            .filter(models.Algoritme.lars == lars)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.model_validate(organisation)

    def get_by_id(self, org_id: int) -> schemas.OrganisationDB | None:
        organisation = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.id == org_id)
            .first()
        )
        if organisation:
            return schemas.OrganisationDB.model_validate(organisation)

    def get_by_type(self, type: OrgType) -> list[schemas.OrganisationDB]:
        orgs = (
            self.session.query(models.Organisation)
            .filter(models.Organisation.type == type)
            .all()
        )
        return [schemas.OrganisationDB.model_validate(o) for o in orgs]

    def update_by_code(self, code: str, item: schemas.OrganisationIn) -> None:
        stmt = (
            update(models.Organisation)
            .where(models.Organisation.code == code)
            .values(**dict(item))
        )
        self.session.execute(stmt)
        self.session.commit()

    def update_by_org_id(self, org_id: str, item: schemas.OrganisationIn) -> None:
        stmt = (
            update(models.Organisation)
            .where(models.Organisation.org_id == org_id)
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

    def get_org_code_to_org_id_mapping(self) -> dict[str, str]:
        """
        Returns a mapping of org_code to org_id.
        """
        result = self.session.query(
            models.Organisation.code, models.Organisation.org_id
        ).all()
        return {org.code: org.org_id for org in result}

    def get_ministeries_KD(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type == OrgType.ministerie
        )

    def get_agentschappen(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type == OrgType.agentschap
        )

    def get_UTO(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type.in_(
                [
                    OrgType.agentschap,
                    OrgType.politie,
                    # OrgType.inspectie,
                    OrgType.zelfstandig_bestuursorgaan,
                    OrgType.rechtspraak,
                    OrgType.openbaar_lichaam_voor_beroep_en_bedrijf,
                ]
            )
        )

    def get_BOO(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type.in_(
                [
                    OrgType.adviescollege,
                    OrgType.interdepartementale_commissie,
                    OrgType.koepelorganisatie,
                    OrgType.regionaal_samenwerkingsorgaan,
                ]
            )
        )

    def get_Overig(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type.in_(
                [
                    OrgType.organisatie_met_overheidsbemoeienis,
                    OrgType.organisatieonderdeel,
                ]
            )
        )

    def get_OverigPublic(self, conditional_org_counts):
        return self.session.query(conditional_org_counts).filter(
            conditional_org_counts.c.type.in_(
                [
                    OrgType.organisatieonderdeel,
                    OrgType.politie,
                ]
            )
        )

    def get_overview_published_nat_org(
        self, language: Language
    ) -> list[NationalOrganisationsCount]:
        published_nl_algos = self.gen_published_nl_algos()
        all_org_counts = self.gen_all_org_counts(published_nl_algos)
        organisation_details_lang = self.gen_organisation_details_lang(language)
        conditional_org_counts = self.gen_conditional_org_counts(
            all_org_counts, organisation_details_lang, published=True
        ).subquery()

        ministeries = self.get_ministeries_KD(conditional_org_counts)
        UTOs = self.get_UTO(conditional_org_counts)
        BOOs = self.get_BOO(conditional_org_counts)
        overige = self.get_Overig(conditional_org_counts)

        results_ministeries = self.session.execute(ministeries).all()
        results_UTO = self.session.execute(UTOs).all()
        results_BOO = self.session.execute(BOOs).all()
        results_Overig = self.session.execute(overige).all()
        overview_nat_orgs = []
        for ministry in RelationWithMinistry:
            overview_nat_org = {
                OrganisationCluster.Name: ministry.value,
                OrganisationCluster.Total: 0,
                OrganisationCluster.KD: 0,
                OrganisationCluster.UTO: 0,
                OrganisationCluster.BOO: 0,
                OrganisationCluster.Overig: 0,
            }
            overview_nat_orgs.append(overview_nat_org)

        self.update_overview(
            overview_nat_orgs, results_ministeries, OrganisationCluster.KD, 2
        )
        self.update_overview(overview_nat_orgs, results_UTO, OrganisationCluster.UTO, 7)
        self.update_overview(overview_nat_orgs, results_BOO, OrganisationCluster.BOO, 7)
        self.update_overview(
            overview_nat_orgs, results_Overig, OrganisationCluster.Overig, 7
        )
        return overview_nat_orgs

    def update_overview(self, overview_nat_orgs, results, org_cluster, index):
        for dict_nat_org in overview_nat_orgs:
            for row in results:
                relation_with_ministery = (
                    row[index].replace("Ministerie van", "").strip()
                    if org_cluster == OrganisationCluster.KD and row[index]
                    else row[index]
                )
                part_of = row[6]

                if relation_with_ministery is None and part_of is None:
                    continue

                if (
                    relation_with_ministery is not None
                    and relation_with_ministery
                    in dict_nat_org[OrganisationCluster.Name]
                ):
                    key = relation_with_ministery

                elif (
                    part_of is not None
                    and part_of in dict_nat_org[OrganisationCluster.Name]
                ):
                    key = part_of
                else:
                    continue

                if key is not None and key in dict_nat_org[OrganisationCluster.Name]:
                    dict_nat_org[org_cluster] += row[1]
                    dict_nat_org[OrganisationCluster.Total] += row[1]

    def get_overview_published_nat_org_public(
        self, language: Language
    ) -> list[NationalOrganisationsCountDashboard]:
        published_nl_algos = self.gen_published_nl_algos()
        all_org_counts = self.gen_all_org_counts(published_nl_algos)
        organisation_details_lang = self.gen_organisation_details_lang(language)
        conditional_org_counts = self.gen_conditional_org_counts(
            all_org_counts, organisation_details_lang, published=True
        ).subquery()

        ministeries = self.get_ministeries_KD(conditional_org_counts)
        agentschappen = self.get_agentschappen(conditional_org_counts)
        overige = self.get_OverigPublic(conditional_org_counts)

        results_ministeries = self.session.execute(ministeries).all()
        results_agentschappen = self.session.execute(agentschappen).all()
        results_Overig = self.session.execute(overige).all()
        overview_nat_orgs = []
        for ministry in RelationWithMinistry:
            overview_nat_org = {
                OrganisationCluster.Name: ministry.value,
                OrganisationCluster.Total: 0,
                OrganisationCluster.KD: 0,
                OrganisationCluster.Agency: 0,
                OrganisationCluster.Overig: 0,
            }
            overview_nat_orgs.append(overview_nat_org)

        self.update_overview(
            overview_nat_orgs, results_ministeries, OrganisationCluster.KD, 2
        )
        self.update_overview(
            overview_nat_orgs, results_agentschappen, OrganisationCluster.Agency, 7
        )
        self.update_overview(
            overview_nat_orgs, results_Overig, OrganisationCluster.Overig, 7
        )
        return overview_nat_orgs

    def get_org_relation_based_on_org_id(
        self, org_id: str
    ) -> schemas.OrganisationRelationResponse:
        """
        Recursively get the hierarchy for the given organisation org_id.
        """

        def get_org_relation(org_id: str):
            stmt = (
                select(
                    models.Organisation.org_id,
                    models.Organisation.parent_id,
                    models.Organisation.child_id,
                    models.Organisation.official_name,
                )
                .select_from(models.Organisation)
                .where(models.Organisation.org_id == org_id)
            )
            results = self.session.execute(stmt).first()
            return results

        hierarchy = []
        org_ids_in_path = []
        current_org = get_org_relation(org_id)

        if not current_org:
            return OrganisationRelationResponse(
                org_id=org_id, hierarchy=[], hierarchy_path=""
            )

        while current_org:
            current_org_id, parent_id, child_id, name = current_org
            hierarchy.append(
                {
                    "org_id": current_org_id,
                    "name": name,
                }
            )
            if current_org_id != org_id:
                org_ids_in_path.append(current_org_id)
            if parent_id:
                current_org = get_org_relation(parent_id)
            else:
                break

        hierarchy.reverse()
        org_ids_in_path.reverse()
        hierarchy_path = "/".join(org_ids_in_path)

        return OrganisationRelationResponse(
            org_id=org_id,
            hierarchy_path=hierarchy_path,
            hierarchy=[OrganisationRelationHierarchy(**entry) for entry in hierarchy],
        )
