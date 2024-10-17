import datetime
from app.database.database import Base
from sqlalchemy import JSON, VARCHAR, Enum, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.schemas.misc import Language


class BrokenLinks(Base):
    __tablename__ = "broken_links"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lars: Mapped[str] = mapped_column(VARCHAR(8), nullable=True, index=True)
    name: Mapped[str | None] = mapped_column(VARCHAR(1024))
    organisation: Mapped[str | None] = mapped_column(VARCHAR(1024))
    language: Mapped[Language] = mapped_column(Enum(Language), nullable=False)
    batch: Mapped[int] = mapped_column(Integer, nullable=False)
    broken_links: Mapped[list[str] | None] = mapped_column(JSON)
    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
