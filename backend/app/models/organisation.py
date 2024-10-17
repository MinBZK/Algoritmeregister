import datetime
from sqlalchemy import Boolean, Integer, DateTime, VARCHAR, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base
from app.models.organisation_details import OrganisationDetails
from app.schemas import OrgType
from . import Algoritme
from app.middleware.authorisation.config._base import Flow


class Organisation(Base):
    __tablename__ = "organisation"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    type: Mapped[OrgType] = mapped_column(Enum(OrgType, name="type"), nullable=True)
    show_page: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="False"
    )
    flow: Mapped[Flow] = mapped_column(
        VARCHAR, nullable=False, server_default="ictu_last"
    )

    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    algoritmes: Mapped[list[Algoritme]] = relationship(
        "Algoritme", back_populates="organisation"
    )

    organisation_details: Mapped[list[OrganisationDetails]] = relationship(
        "OrganisationDetails", back_populates="organisation"
    )
