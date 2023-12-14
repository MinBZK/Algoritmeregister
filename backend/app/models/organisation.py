import datetime
from sqlalchemy import Integer, DateTime, VARCHAR, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base
from app.schemas import OrgType
from . import Algoritme


class Organisation(Base):
    __tablename__ = "organisation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    type: Mapped[OrgType] = mapped_column(Enum(OrgType, name="type"), nullable=True)

    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    algoritmes: Mapped[list[Algoritme]] = relationship(
        "Algoritme", back_populates="organisation"
    )
