from fastapi import APIRouter, Query
from fastapi import Depends
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config.resource import Columns
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/columns/")
async def get_columns(db: Session = Depends(get_db)):
    stmt = text(
        """SELECT table_name, column_name, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND column_name != 'algoritme_id'
        AND column_name != 'id'
        AND table_name != 'alembic_version'
        ORDER BY table_name, ordinal_position
        """
    )
    return db.execute(stmt).all()


@router.get("/db-count/")
async def get_total_count(db: Session = Depends(get_db)) -> int:
    stmt = text("SELECT count(id) FROM algoritme")
    return int(db.execute(stmt).all()[0][0])


@router.get("/db-count/{column}")
async def get_count_per_type(column: Columns, db: Session = Depends(get_db)):
    stmt = text(
        f"""
            SELECT count(1), {column.value} as descriptor
            FROM algoritme
            LEFT JOIN inzet ON algoritme.id=inzet.algoritme_id
            LEFT JOIN juridisch ON algoritme.id=juridisch.algoritme_id
            LEFT JOIN metadata ON algoritme.id=metadata.algoritme_id
            LEFT JOIN toepassing ON algoritme.id=toepassing.algoritme_id
            LEFT JOIN toezicht ON algoritme.id=toezicht.algoritme_id
            GROUP BY {column.value}
            ORDER BY count(1) desc
            LIMIT 10
        """
    )
    return db.execute(stmt).all()


@router.get("/completeness/")
async def get_count_with_filled_columns(
    columns: list[Columns] | None = Query(default=None), db: Session = Depends(get_db)
):
    selection_string = ", ".join(columns)
    stmt = text(
        f"""SELECT {selection_string}
        FROM algoritme
        LEFT JOIN inzet ON algoritme.id=inzet.algoritme_id
        LEFT JOIN juridisch ON algoritme.id=juridisch.algoritme_id
        LEFT JOIN metadata ON algoritme.id=metadata.algoritme_id
        LEFT JOIN toepassing ON algoritme.id=toepassing.algoritme_id
        LEFT JOIN toezicht ON algoritme.id=toezicht.algoritme_id
        """
    )

    table = db.execute(stmt).all()

    def is_filled(cell: any) -> bool:
        return [""].count(cell) == 0

    compliantRows = []
    for row in table:
        compliantRow = all([is_filled(cell) for cell in row])
        if compliantRow:
            compliantRows.append(row)
    return len(compliantRows)
