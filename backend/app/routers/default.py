from fastapi import APIRouter
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import logging
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import datetime

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/algoritme/",
    response_model=list[schemas.algoritme.Algoritme],
)
async def get_all(db: Session = Depends(get_db)):
    return (
        db.query(models.algoritme.Algoritme)
        .order_by(models.algoritme.Algoritme.slug)
        .all()
    )


@router.get(
    "/algoritme/{slug}/",
    response_model=schemas.algoritme.Algoritme,
)
async def get_one(slug: str, db: Session = Depends(get_db)):
    x = (
        db.query(models.algoritme.Algoritme)
        .filter(models.algoritme.Algoritme.slug == slug)
        .first()
    )
    return x


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
    stream = io.StringIO()
    df[relevant_columns].to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    timestamp = datetime.datetime.now().strftime("%Y%M%d")
    filename = f"algoritmeregister_{timestamp}.csv"

    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    return response
