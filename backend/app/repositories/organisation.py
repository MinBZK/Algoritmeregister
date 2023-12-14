from sqlalchemy.orm import Session
from sqlalchemy import ColumnElement, func
from app import models, schemas
from .index import IRepository


class OrganisationRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.OrganisationDB]:
        all_orgs: list[models.Organisation] = self.session.query(
            models.Organisation
        ).all()
        return [schemas.OrganisationDB.from_orm(one_org) for one_org in all_orgs]

    def get_aggregated_organisations_by_filter(
        self, filter: ColumnElement[bool]
    ) -> list[schemas.OrganisationFilterGroup]:
        subquery = (
            self.session.query(
                models.Algoritme.organisation_id,
                func.count(models.Algoritme.id).label("count"),
            )
            .join(
                models.AlgoritmeVersion,
                models.AlgoritmeVersion.algoritme_id == models.Algoritme.id,
            )
            .filter(filter)
            .group_by(models.Algoritme.organisation_id)
            .subquery()
        )

        org_rows_model = self.session.query(
            models.Organisation.type, models.Organisation.name, subquery.c.count
        ).join(
            subquery,
            models.Organisation.id == subquery.c.organisation_id,
        )

        org_rows = [schemas.OrganisationGrouping.from_orm(o) for o in org_rows_model]
        results: list[schemas.OrganisationFilterGroup] = []
        types_present = set([r.type for r in org_rows])
        for type in types_present:
            organisations: list[schemas.OrganisationPresenceCount] = []
            for org_row in org_rows:
                if org_row.type == type:
                    organisations.append(
                        schemas.OrganisationPresenceCount(
                            name=org_row.name, count=org_row.count
                        )
                    )

            if type is None:
                type = schemas.OrgType.overig

            results.append(
                schemas.OrganisationFilterGroup(type=type, organisations=organisations)
            )
        return results

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
