from sqlalchemy.orm import Session
from app.repositories.precomputed_values import PreComputedValuesRepository
from app.schemas.misc import Language
from app import models, schemas
from sqlalchemy import and_, func, desc
from app.middleware.authorisation.schemas import State
from app.services.algoritme_version import db_list_to_python_list


def get_precomputed_values_by_lang(
    db: Session, lang: Language
) -> list[schemas.HighlightedAlgorithmResponse]:
    precomputed_values_repo = PreComputedValuesRepository(db)
    return precomputed_values_repo.get_highlighted_values(lang)


def calc_highlighted_algorithms(
    db: Session, language: Language
) -> list[schemas.HighlightedAlgorithmResponse]:
    latest_upload_owner = (
        db.query(
            models.Algoritme.organisation_id,
            func.max(models.AlgoritmeVersion.create_dt).label("max_creation_dt"),
        )
        .join(
            models.Algoritme,
            models.Algoritme.id == models.AlgoritmeVersion.algoritme_id,
        )
        .filter(
            models.AlgoritmeVersion.state == State.PUBLISHED,
            models.AlgoritmeVersion.language == language,
        )
        .group_by(models.Algoritme.organisation_id)
        .subquery()
    )

    latest_algo_owner = (
        db.query(models.AlgoritmeVersion)
        .join(
            latest_upload_owner,
            and_(
                latest_upload_owner.c.max_creation_dt
                == models.AlgoritmeVersion.create_dt
            ),
        )
        .filter(models.AlgoritmeVersion.language == language)
        .order_by(desc(models.AlgoritmeVersion.create_dt))
        .limit(3)
        .all()
    )
    for n, _ in enumerate(latest_algo_owner):
        latest_algo_owner[n] = db_list_to_python_list(latest_algo_owner[n])
    return [
        schemas.HighlightedAlgorithmResponse.model_validate(alg)
        for alg in latest_algo_owner
    ]
