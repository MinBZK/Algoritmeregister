import datetime
from sqlalchemy import Boolean, Integer, DateTime, JSON, TEXT
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base


class HtmlFigures(Base):
    __tablename__ = "html_figures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    html: Mapped[str] = mapped_column(TEXT, nullable=False)
    most_recent: Mapped[bool] = mapped_column(Boolean, nullable=False)
    static_data: Mapped[dict] = mapped_column(JSON, nullable=True)
