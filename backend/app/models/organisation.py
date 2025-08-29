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
    org_id: Mapped[str] = mapped_column(VARCHAR(1024), nullable=True, unique=True)

    official_name: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    alternative_name: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    abbreviation: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    roo_type: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    part_of: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    relation_with_ministry: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    tooi_uri: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    kvk_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    organisation_code: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    tooi_uri_regional_collaboration_body: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    label: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    official_name_with_type: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    official_name_without_type: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    official_name_for_sorting: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    preferred_name_without_type: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    preferred_name_including_type: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    preferred_name_for_sorting: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    tooi_alternative_name: Mapped[str | None] = mapped_column(
        VARCHAR(1024), nullable=True
    )
    last_updated_dt_tooi: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=None
    )
    parent_id: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    child_id: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)

    algoritmes: Mapped[list[Algoritme]] = relationship(
        "Algoritme", back_populates="organisation"
    )

    organisation_details: Mapped[list[OrganisationDetails]] = relationship(
        "OrganisationDetails", back_populates="organisation"
    )
