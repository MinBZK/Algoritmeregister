from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, update, ColumnElement
from app import models, schemas
from app.schemas.misc import Language
from .index import IRepository
from app.services.algoritme_version import (
    db_list_to_python_list_schema,
)


class AlgoritmeVersionRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    # def __del__(self):
    #     self.session.commit()

    def get_all(self) -> list[schemas.AlgoritmeVersionDB]:
        algoritme_versions = self.session.query(models.AlgoritmeVersion).all()
        return [schemas.AlgoritmeVersionDB.from_orm(a) for a in algoritme_versions]

    def get_published_by_filter(
        self,
        filter: ColumnElement[bool],
        offset: int = 0,
        limit: int = 10,
    ) -> list[schemas.AlgoritmeVersionQuery]:
        algoritme_versions = (
            self.session.query(models.AlgoritmeVersion)
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .filter(filter, models.AlgoritmeVersion.published)
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionQuery.from_orm(a))
            for a in algoritme_versions
        ]

    def get_latest_by_lars_by_lang(
        self, lars: str, lang: schemas.Language
    ) -> schemas.AlgoritmeVersionDB | None:
        latest_algo = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.lars == lars,
                models.AlgoritmeVersion.language == lang,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
        ).first()
        if latest_algo:
            latest_algo = schemas.AlgoritmeVersionDB.from_orm(latest_algo)
            return db_list_to_python_list_schema(latest_algo)

    def get_published_by_lang(
        self, lang: schemas.Language
    ) -> list[schemas.AlgoritmeVersionDB]:
        published_algoritmes = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.language == lang,
                models.AlgoritmeVersion.published,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_algoritmes
        ]

    def get_latest_by_lang(
        self, lang: schemas.Language
    ) -> list[schemas.AlgoritmeVersionDB]:
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
        self, as_org: str, lang: schemas.Language
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
                models.AlgoritmeVersion.owner == as_org,
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
            .filter(
                models.AlgoritmeVersion.published,
                models.AlgoritmeVersion.lars == lars,
            )
            .all()
        )
        return [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_alg
        ]

    def get_published_by_lars_by_lang(
        self, lars: str, lang: schemas.Language
    ) -> schemas.AlgoritmeVersionDB | None:
        """For a lars-code, return published by language"""
        published_alg = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.published,
                models.AlgoritmeVersion.lars == lars,
                models.AlgoritmeVersion.language == lang,
            )
            .first()
        )
        if published_alg:
            return db_list_to_python_list_schema(
                schemas.AlgoritmeVersionDB.from_orm(published_alg)
            )

    def get_published_by_org_by_lang(
        self, as_org, lang: schemas.Language
    ) -> list[schemas.AlgoritmeVersionDB]:
        """For an organisation, returns all published by language"""
        published_algos = (
            self.session.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.published,
                models.AlgoritmeVersion.owner == as_org,
                models.AlgoritmeVersion.language == lang,
            )
            .all()
        )

        result = [
            db_list_to_python_list_schema(schemas.AlgoritmeVersionDB.from_orm(alg))
            for alg in published_algos
        ]
        return result

    def add(self, item: schemas.AlgoritmeVersionIn) -> schemas.AlgoritmeVersionDB:
        algoritme_version = models.AlgoritmeVersion(**item.dict())
        self.session.add(algoritme_version)
        self.session.commit()

        return schemas.AlgoritmeVersionDB.from_orm(algoritme_version)

    def update_by_id(self, id: int, item: schemas.AlgoritmeVersionIn) -> None:
        stmt = (
            update(models.AlgoritmeVersion)
            .where(models.AlgoritmeVersion.id == id)
            .values(**item.dict(exclude={"create_dt"}))
        )
        self.session.execute(stmt)
        self.session.commit()

    def retract_by_lars(self, lars: str) -> list[schemas.AlgoritmeVersionDB] | None:
        query = self.session.query(models.AlgoritmeVersion).filter(
            models.AlgoritmeVersion.published,
            models.AlgoritmeVersion.lars == lars,
        )
        algoritme_versions = query.all()
        if len(algoritme_versions) == 0:
            return None

        update_is_succesful = query.update(
            {
                models.AlgoritmeVersion.published: False,
                models.AlgoritmeVersion.released: False,
            },
            synchronize_session=False,
        )
        self.session.commit()
        if update_is_succesful:
            return [
                schemas.AlgoritmeVersionDB.from_orm(alg) for alg in algoritme_versions
            ]

    def release_latest_by_lars(self, lars: str) -> int | None:
        # Always NLD
        latest_algo = self.get_latest_by_lars_by_lang(lars, schemas.Language.NLD)
        if not latest_algo:
            return None

        latest_algo.released = True
        self.update_by_id(
            latest_algo.id, schemas.AlgoritmeVersionIn(**latest_algo.dict())
        )
        self.session.commit()

    def unrelease_by_lars(self, lars: str) -> int:
        n_unreleased = (
            self.session.query(models.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.lars == lars)
            .update(
                {
                    models.AlgoritmeVersion.released: False,
                },
                synchronize_session="fetch",
            )
        )
        return n_unreleased

    def preview_latest_by_lars(self, lars: str) -> schemas.AlgoritmeVersionDB | None:
        # Always NLD
        latest_algo = self.get_latest_by_lars_by_lang(lars, schemas.Language.NLD)
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
            .filter(
                models.AlgoritmeVersion.lars == lars,
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
