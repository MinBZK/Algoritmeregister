from app import schemas, models
from app.middleware.authorisation.schemas import State


def search_similar(
    lars, db, language, model, min_score: int
) -> schemas.AlgoritmeSimilarQueryResponse:
    if lars[0] == "C":
        current = (
            db.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars[1:],
                models.AlgoritmeVersion.preview_active,
                models.AlgoritmeVersion.language == language,
            )
            .first()
        )
    else:
        current = (
            db.query(models.AlgoritmeVersion)
            .join(models.Algoritme)
            .filter(
                models.Algoritme.lars == lars,
                models.AlgoritmeVersion.language == language,
                models.AlgoritmeVersion.state == State.PUBLISHED,
            )
            .first()
        )

    # distance_func = model.l2_distance
    # distance_func = model.l1_distance
    # distance_func = model.max_inner_product
    distance_func = model.cosine_distance

    _results = (
        db.query(models.AlgoritmeVersion, distance_func(getattr(current, model.key)))
        .order_by(distance_func(getattr(current, model.key)))
        .filter(
            models.AlgoritmeVersion.language == language,
            models.AlgoritmeVersion.id != current.id,
            models.AlgoritmeVersion.state == State.PUBLISHED,
        )
        .limit(5)
    ).all()

    _results = [item for item in _results if (1 - item[1]) * 100 > min_score]
    results = [item[0] for item in _results]
    scores = [(1 - item[1]) * 100 for item in _results]

    filter_data = schemas.AlgoritmeFilterData(
        organisation=None,
        publicationcategory=None,
        impact_assessment=None,
        organisationtype=None,
    )

    return schemas.AlgoritmeSimilarQueryResponse(
        scores=scores,
        results=results,
        total_count=10,
        filter_data=filter_data,
        selected_filters=[],
    )
