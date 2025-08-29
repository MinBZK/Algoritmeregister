import datetime
from sqlalchemy import Integer, DateTime, VARCHAR, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.database.database import Base
from app.schemas import Language


class OrganisationDetails(Base):
    __tablename__ = "organisation_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organisation_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("organisation.id", ondelete="cascade"), nullable=False
    )
    language: Mapped[Language] = mapped_column(Enum(Language), nullable=False)

    name: Mapped[str] = mapped_column(VARCHAR(1024), nullable=False)
    contact_info: Mapped[str | None] = mapped_column(VARCHAR(1024), nullable=True)
    about: Mapped[str | None] = mapped_column(VARCHAR(10000), nullable=True)
    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    vector: Mapped[str | None] = mapped_column(TSVECTOR)
    __table_args__ = (
        UniqueConstraint(
            "language", "organisation_id", name="language_organisation_id_uc"
        ),
    )

    organisation = relationship("Organisation", back_populates="organisation_details")

    show_page = association_proxy("organisation", "show_page")
    code = association_proxy("organisation", "code")
    org_id = association_proxy("organisation", "org_id")
    type = association_proxy("organisation", "type")
