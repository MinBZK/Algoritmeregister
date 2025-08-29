from sqlalchemy import func, update
from sqlalchemy.orm import Session
from app import models, schemas
from app.schemas.organization import OrganisationConfig
from .index import IRepository
from app.schemas import Language


class OrganisationDetailsRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.OrganisationDetailsDB]:
        organisation_details = self.session.query(models.OrganisationDetails).all()
        return [
            schemas.OrganisationDetailsDB.model_validate(org_detail)
            for org_detail in organisation_details
        ]

    def add(self, item: schemas.OrganisationDetailsIn) -> schemas.OrganisationDetailsDB:
        organization_detail = models.OrganisationDetails(**dict(item))
        self.session.add(organization_detail)
        self.session.flush()

        return schemas.OrganisationDetailsDB.model_validate(organization_detail)

    def update_by_id(
        self, id: int, item: schemas.OrganisationDetailsIn
    ) -> schemas.OrganisationDetailsDB | None:
        stmt = (
            update(models.OrganisationDetails)
            .where(models.OrganisationDetails.id == id)
            .values(**dict(item))
        )
        self.session.execute(stmt)
        self.session.flush()

        updated_object = (
            self.session.query(models.OrganisationDetails)
            .filter(models.OrganisationDetails.id == id)
            .first()
        )
        if updated_object:
            return schemas.OrganisationDetailsDB.model_validate(updated_object)

    def get_shown_by_org_id_by_lang(
        self, org_id: str, lang: Language
    ) -> schemas.OrganisationDetailsDB | None:
        organisation_detail = (
            self.session.query(models.OrganisationDetails)
            .join(
                models.Organisation,
                models.Organisation.id == models.OrganisationDetails.organisation_id,
            )
            .filter(
                models.Organisation.org_id == org_id,
                models.OrganisationDetails.language == lang,
                models.Organisation.show_page,
            )
            .first()
        )
        if organisation_detail:
            return schemas.OrganisationDetailsDB.model_validate(organisation_detail)

    def get_by_org_id_by_lang(
        self, org_id: int, lang: Language
    ) -> schemas.OrganisationDetailsDB | None:
        organisation_detail = (
            self.session.query(models.OrganisationDetails)
            .filter(
                models.OrganisationDetails.organisation_id == org_id,
                models.OrganisationDetails.language == lang,
            )
            .first()
        )

        if organisation_detail:
            return schemas.OrganisationDetailsDB.model_validate(organisation_detail)

    def get_by_name(self, name: str) -> schemas.OrganisationDetailsDB | None:
        organisation_detail = (
            self.session.query(models.OrganisationDetails)
            .filter(models.OrganisationDetails.name == name)
            .first()
        )
        if organisation_detail:
            return schemas.OrganisationDetailsDB.model_validate(organisation_detail)

    def __build_org_config_query(
        self,
        lang: Language,
        q: str | None = None,
    ):
        search = f"%{q.lower()}%" if q is not None else "%%"
        return (
            self.session.query(
                models.Organisation.id,
                models.Organisation.code,
                models.Organisation.org_id,
                models.Organisation.type,
                models.Organisation.flow,
                models.Organisation.show_page,
                models.OrganisationDetails.name,
            )
            .join(
                models.Organisation,
                models.Organisation.id == models.OrganisationDetails.organisation_id,
            )
            .filter(models.OrganisationDetails.language == lang)
            .filter(func.lower(models.OrganisationDetails.name).like(search))
            .order_by(models.OrganisationDetails.name)
        )

    def get_org_configs_by_lang(
        self,
        lang: Language,
        limit: int | None = None,
        skip: int | None = None,
        q: str | None = None,
    ) -> list[OrganisationConfig]:
        query = self.__build_org_config_query(lang, q)
        org_configs = query.limit(limit).offset(skip).all()
        return [OrganisationConfig.model_validate(org) for org in org_configs]

    def get_org_configs_by_org_list_by_lang(
        self,
        org_list: list[str],
        lang: Language,
        limit: int | None = None,
        skip: int | None = None,
        q: str | None = None,
    ) -> list[OrganisationConfig]:
        query = self.__build_org_config_query(lang, q)
        org_configs = (
            query.filter(
                models.Organisation.code.in_(org_list),
            )
            .limit(limit)
            .offset(skip)
            .all()
        )
        return [OrganisationConfig.model_validate(org) for org in org_configs]

    def get_org_configs_by_org_id_list_by_lang(
        self,
        org_list: list[str],
        lang: Language,
        limit: int | None = None,
        skip: int | None = None,
        q: str | None = None,
    ) -> list[OrganisationConfig]:
        query = self.__build_org_config_query(lang, q)
        org_configs = (
            query.filter(
                models.Organisation.org_id.in_(org_list),
            )
            .limit(limit)
            .offset(skip)
            .all()
        )
        return [OrganisationConfig.model_validate(org) for org in org_configs]

    def get_org_configs_by_org_id_by_lang(
        self, org_id: str, lang: Language
    ) -> OrganisationConfig | None:
        query = self.__build_org_config_query(lang)
        org_config = query.filter(
            models.Organisation.org_id == org_id,
        ).first()
        if org_config:
            return OrganisationConfig.model_validate(org_config)
