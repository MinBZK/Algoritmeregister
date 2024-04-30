import datetime
from sqlalchemy import Integer, DateTime, VARCHAR, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base
from app import schemas


class ActionHistory(Base):
    __tablename__ = "action_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    algoritme_version_id = mapped_column(
        Integer, ForeignKey("algoritme_version.id", ondelete="cascade"), nullable=False
    )
    operation = mapped_column(
        Enum(schemas.OperationEnum, name="operation"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)

    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
