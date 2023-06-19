from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import logging
from sqlalchemy import or_, and_, func, sql, desc
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import datetime
import csv
import json
from app.config.settings import Settings
from app.middleware.middleware import get_db
from app.services.algoritme_version import db_list_to_python_list
from app import models, schemas, controllers

router = APIRouter()
logger = logging.getLogger(__name__)

env_settings = Settings()


@router.post(
    "/algoritme/",
    response_model=schemas.AlgoritmeQueryResponse,
)
async def get_all(
    algoritme_query: schemas.algoritme_version.AlgoritmeQuery,
    db: Session = Depends(get_db),
):
    model = models.AlgoritmeVersion

    or_clauses_search = []

    exclude_columns = [
        "id",
        "algoritme_id",
        "create_dt",
        "end_dt",
        "dpia",
        "mprd",
        "published",
        "preview_active",
        "released",
        "source_id",
    ]
    if len(algoritme_query.search) > 0:
        # Select columns to search in from the table
        columns = model.__table__.columns
        search_columns = [col for col in columns if col.key not in exclude_columns]

        # Add searching in every column to the or clauses
        for col in search_columns:
            or_clauses_search.append(col.ilike(f"%{algoritme_query.search.lower()}%"))

    and_clauses_filters = []
    if len(algoritme_query.filters) > 0:
        for a_filter in algoritme_query.filters:
            column = getattr(model, a_filter.attribute)
            # a_filter.value is a list when multiple filters of the same column (e.g. organization) are applied.
            if type(a_filter.value) is list:
                and_clauses_filters.append(column.in_(a_filter.value))
            else:
                and_clauses_filters.append(column == a_filter.value)

    search_clause = or_(*or_clauses_search)

    # Public website sees only published, Concept website sees only released.
    if (env_settings.type == "API") or (env_settings.type == "DEV"):
        show_clause = model.released
    else:  # env_settings.type == "PUB"
        show_clause = model.published

    where_clause = and_(search_clause, *and_clauses_filters, show_clause)

    query = (
        db.query(model)
        .order_by(model.algoritme_id)
        .filter(where_clause)
        .limit(algoritme_query.limit)
        .offset((algoritme_query.page - 1) * algoritme_query.limit)
    )

    # Constructs returning aggregation dictionary.
    aggregation_columns = [model.organization]
    aggregation_queries = []
    for c in aggregation_columns:
        query_agg = db.query(
            sql.expression.literal(c.name).label("aggregation_column"),
            c.label("aggregation_value"),
            func.count(c).label("count"),
        )

        query_agg = query_agg.filter(where_clause).group_by(c)
        aggregation_queries.append(query_agg)

    aggregation_union = aggregation_queries[0].union(*aggregation_queries[1:]).all()

    # Constructs returning total count.
    total_count = db.query(func.count(model.id)).filter(where_clause).scalar()

    results = []
    for q in query.all():
        parsed_algo = db_list_to_python_list(q)
        algo_dict = parsed_algo.__dict__.copy()
        algo_dict["lars"] = q.lars
        results.append(algo_dict)

    return {
        "results": results,
        "total_count": total_count,
        "aggregations": [
            {
                "values": [a for a in aggregation_union if a[0] == c.name],
                "aggregation_attribute": c.name,
            }
            for c in aggregation_columns
        ],
    }


output_schemas = schemas.util.get_all_output_schemas_union()


@router.get(
    "/algoritme/{lars}/",
    response_model=output_schemas | None,
)
async def get_one(lars: str, db: Session = Depends(get_db)):
    if lars[0] == "C":
        result = (
            db.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.lars == lars[1:],
                models.AlgoritmeVersion.preview_active,
            )
            .first()
        )
        controllers.disable_preview(
            lars=lars[1:],
            db=db,
            user="anonymous website visitor",
            reason=models.OperationEnum.preview_used,
        )
    else:
        # Public website sees only published, Concept website sees only released.
        if (env_settings.type == "API") or (env_settings.type == "DEV"):
            show_clause = models.AlgoritmeVersion.released
        else:  # env_settings.type == "PUB"
            show_clause = models.AlgoritmeVersion.published

        result = (
            db.query(models.AlgoritmeVersion)
            .filter(
                models.AlgoritmeVersion.lars == lars,
                show_clause,
            )
            .order_by(desc(models.AlgoritmeVersion.create_dt))
            .first()
        )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kan algoritme niet vinden.",
        )

    result = db_list_to_python_list(result)
    return result


excel_schema = schemas.get_algorithm_export_schema(truncated=True)


@router.get("/file/algoritme")
async def download_algoritme(db: Session = Depends(get_db)):
    result = (
        db.query(models.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.published)
        .order_by(models.AlgoritmeVersion.algoritme_id)
        .all()
    )

    # Use schema to filter output of query
    data = [excel_schema.from_orm(r).dict() for r in result]
    df = pd.DataFrame(data)

    stream = io.BytesIO()
    df = df.replace(r"\n", "", regex=True)
    df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"algoritmeregister_{timestamp}.csv"

    response.headers["Content-Encoding"] = "UTF-8"
    response.headers["Content-type"] = "text/csv; charset=UTF-8"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response


json_schema = schemas.get_algorithm_export_schema(truncated=False)
if (env_settings.type == "API") or (env_settings.type == "DEV"):

    @router.get(
        "/json/algoritme",
        response_model=list[json_schema],
    )
    async def export_algoritme_json(db: Session = Depends(get_db)):
        result = (
            db.query(models.algoritme_version.AlgoritmeVersion)
            .filter(models.AlgoritmeVersion.published)
            .order_by(models.AlgoritmeVersion.algoritme_id)
            .all()
        )

        data = [json_schema.from_orm(r).dict() for r in result]
        df = pd.DataFrame(data)
        df["create_dt"] = df["create_dt"].astype(str)

        df = df[(df["owner"] != "sandbox")]
        data_out = df.to_dict(orient="records")

        stream = io.BytesIO()
        stream.write(json.dumps(data_out).encode())
        response = StreamingResponse(iter([stream.getvalue()]), media_type="json")

        # response.headers["Content-Encoding"] = "UTF-8"
        # response.headers["Content-type"] = "json; charset=UTF-8"
        response.headers["Content-Disposition"] = "attachment; filename=pub_data.json"

        return response
