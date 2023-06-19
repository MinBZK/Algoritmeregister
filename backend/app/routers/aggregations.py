from fastapi import APIRouter, Query
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.resource import Columns
import logging
from app import models
from app.config.settings import Settings

router = APIRouter()
logger = logging.getLogger(__name__)
env_settings = Settings()


@router.get("/columns/")
async def get_columns(db: Session = Depends(get_db)):
    stmt = text(
        """SELECT column_name, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name = 'algoritme_version'
        AND column_name != 'algoritme_id'
        AND column_name != 'id'
        AND column_name != 'end_dt'
        AND column_name != 'create_dt'
        AND column_name != 'published'
        ORDER BY ordinal_position
        """
    )
    return db.execute(stmt).all()


@router.get("/db-count/")
async def get_total_count(db: Session = Depends(get_db)) -> int:
    if (env_settings.type == "API") or (env_settings.type == "DEV"):
        stmt = text("SELECT count(id) FROM algoritme_version WHERE released IS TRUE")
    else:
        stmt = text("SELECT count(id) FROM algoritme_version WHERE published IS TRUE")
    return int(db.execute(stmt).all()[0][0])


@router.get("/db-count/{column}")
async def get_count_per_type(column: Columns, db: Session = Depends(get_db)):
    if (env_settings.type == "API") or (env_settings.type == "DEV"):
        column_filter = "algoritme_version.released"
    else:
        column_filter = "algoritme_version.published"

    stmt = text(
        f"""
            SELECT count(1), {column.value} as descriptor
            FROM algoritme_version
            WHERE {column_filter} IS TRUE
            GROUP BY {column.value}
            ORDER BY count(1) desc
            LIMIT 10
        """
    )
    return db.execute(stmt).all()


@router.get("/completeness/")
async def get_count_with_filled_columns(
    columns: list[Columns] = Query(default=None), db: Session = Depends(get_db)
):
    column_list = [col[0] for col in columns]

    ignore_columns = ["end_dt", "published"]
    columns_model_list = [
        col
        for col in models.AlgoritmeVersion.__table__.columns
        if col.key not in ignore_columns
    ]

    if "*" not in column_list:
        columns_model_list = [
            col for col in columns_model_list if col.key in column_list
        ]

    table = (
        db.query(*columns_model_list).filter(models.AlgoritmeVersion.published).all()
    )

    def is_filled(cell) -> bool:
        checks = [cell != "", cell is not None]
        return all(checks)

    compliantRows = []
    for row in table:
        compliantRow = all([is_filled(cell) for cell in row])
        if compliantRow:
            compliantRows.append(row)
    return len(compliantRows)
