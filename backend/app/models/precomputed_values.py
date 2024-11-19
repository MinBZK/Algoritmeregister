import datetime
from sqlalchemy import VARCHAR, Enum, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.schemas.misc import Language
from app.database.database import Base


class PrecomputedValues(Base):
    __tablename__ = "precomputed_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    language: Mapped[Language] = mapped_column(Enum(Language), nullable=False)
    key: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    value: Mapped[dict] = mapped_column(JSON, nullable=True)
    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
