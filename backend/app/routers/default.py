from fastapi import APIRouter
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import logging
from sqlalchemy import or_, and_, func, sql
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import datetime
import csv

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/algoritme/",
    # response_model=schemas.algoritme.AlgoritmeQueryResponse,
)
async def get_all(
    algoritme_query: schemas.algoritme.AlgoritmeQuery, db: Session = Depends(get_db)
):
    model = models.algoritme.Algoritme

    or_clauses_search = []
    if len(algoritme_query.search) > 0:
        columns_to_search_in = [model.name, model.organization, model.description_short]
        for c in columns_to_search_in:
            or_clauses_search.append(
                or_(
                    func.lower(c)
                    .like(f"%{algoritme_query.search.lower()}%")
                    .self_group()
                )
            )

    and_clauses_filters = []
    if len(algoritme_query.filters) > 0:
        for a in algoritme_query.filters:
            column = getattr(model, a.attribute)
            if type(a.value) is list:
                and_clauses_filters.append(and_(column.in_(a.value)).self_group())
            else:
                and_clauses_filters.append(and_(column == a.value).self_group())

    search_clause = and_(or_(*or_clauses_search))
    where_clause = and_(search_clause, and_(*and_clauses_filters))

    query_filtered = (
        db.query(model)
        .order_by(model.slug)
        .filter(where_clause)
        .limit(algoritme_query.limit)
        .offset((algoritme_query.page - 1) * algoritme_query.limit)
    )

    aggregation_columns = [model.organization]

    aggregation_queries = [
        db.query(
            sql.expression.literal(c.name).label("aggregation_column"),
            c.label("aggregation_value"),
            func.count(c).label("count"),
        )
        .filter(where_clause)
        .group_by(c)
        for c in aggregation_columns
    ]

    aggregation_union = aggregation_queries[0].union(*aggregation_queries[1:]).all()

    return {
        "results": query_filtered.all(),
        "total_count": db.query(func.count(model.id)).filter(where_clause).scalar(),
        "aggregations": [
            {
                "values": [a for a in aggregation_union if a[0] == c.name],
                "aggregation_attribute": c.name,
            }
            for c in aggregation_columns
        ],
    }


@router.get(
    "/algoritme/{slug}/",
    response_model=schemas.algoritme.Algoritme,
)
async def get_one(slug: str, db: Session = Depends(get_db)):
    return (
        db.query(models.algoritme.Algoritme)
        .filter(models.algoritme.Algoritme.slug == slug)
        .first()
    )


@router.get("/algoritme-simple-list/")
async def get_simple_list(db: Session = Depends(get_db)):
    return db.query(
        models.algoritme.Algoritme.slug,
        models.algoritme.Algoritme.name,
        models.algoritme.Algoritme.organization,
    ).all()


@router.get("/file/algoritme")
async def download_algoritme(db: Session = Depends(get_db)):
    result = (
        db.query(models.algoritme.Algoritme)
        .order_by(models.algoritme.Algoritme.slug)
        .all()
    )

    data = [schemas.algoritme.Algoritme.from_orm(r).dict() for r in result]
    df = pd.json_normalize(data)
    relevant_columns = [
        c
        for c in df.columns
        if c not in ["id", "slug"]
        and all(
            [excluded_string not in c for excluded_string in ["algoritme_id", ".id"]]
        )
    ]
    stream = io.BytesIO()
    df = df[relevant_columns].replace(r"\n", "", regex=True)
    df.to_csv(stream, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")
    df.to_csv("test.csv", index=False, quoting=csv.QUOTE_ALL, encoding="utf-8-sig")

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"algoritmeregister_{timestamp}.csv"

    response.headers["Content-Encoding"] = "UTF-8"
    response.headers["Content-type"] = "text/csv; charset=UTF-8"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
