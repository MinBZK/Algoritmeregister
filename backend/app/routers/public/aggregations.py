from fastapi import APIRouter, Query
from fastapi import Depends
from pydantic import BaseModel
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.resource import Columns
from app import models
from app.config.settings import Settings
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
env_settings = Settings()


class Column(BaseModel):
    column_name: str
    is_nullable: str


@router.get("/columns/", response_model=list[Column])
async def get_columns(db: Session = Depends(get_db)):
    skip_columns = [
        "algoritme_id",
        "id",
        "create_dt",
        "published",
        "released",
        "preview_active",
        "language",
    ]
    skip_columns_statement = [
        f"AND column_name != '{column}' " for column in skip_columns
    ]
    stmt = text(
        f"""SELECT column_name, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'algoritme_version'
        {" ".join(skip_columns_statement)}
        ORDER BY ordinal_position
        """
    )
    results = db.execute(stmt).all()

    output = [{"column_name": r[0], "is_nullable": r[1]} for r in results]
    return output


@router.get("/db-count/{column}")
def get_count_per_type(column: Columns, db: Session = Depends(get_db)):
    stmt = text(
        f"""
            SELECT count(1), {column.value} as descriptor
            FROM algoritme_version
            WHERE state = 'PUBLISHED'
            AND language='NLD'
            GROUP BY {column.value}
            ORDER BY count(1) desc
            LIMIT 20
        """
    )
    results = db.execute(stmt).all()

    output = [{"count": r[0], "descriptor": r[1]} for r in results]

    return output


@router.get("/completeness/")
async def get_count_with_filled_columns(
    columns: list[Columns] = Query(default=None), db: Session = Depends(get_db)
):
    ignore_columns = ["end_dt", "published", "released", "language", "state"]
    columns_model_list = [
        col
        for col in models.AlgoritmeVersion.__table__.columns
        if col.key not in ignore_columns
    ]

    if "*" not in columns:
        columns_model_list = [col for col in columns_model_list if col.key in columns]

    table = (
        db.query(*columns_model_list)
        .filter(models.AlgoritmeVersion.state == State.PUBLISHED)
        .all()
    )

    def is_filled(cell) -> bool:
        # Handle scalar values directly
        if isinstance(cell, (str, int, float, type(None))):
            return cell != "" and cell is not None
        # Handle array-like objects
        elif hasattr(cell, "all") or hasattr(cell, "__iter__"):
            return all(c != "" and c is not None for c in cell)
        return False

    compliant_rows = []
    for row in table:
        compliant_row = all([is_filled(cell) for cell in row])
        if compliant_row:
            compliant_rows.append(row)
    return len(compliant_rows)
