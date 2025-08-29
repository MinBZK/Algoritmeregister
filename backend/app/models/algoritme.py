import datetime
from sqlalchemy import Integer, DateTime, VARCHAR, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.database import Base


class Algoritme(Base):
    __tablename__ = "algoritme"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lars: Mapped[str] = mapped_column(VARCHAR(8), nullable=True, index=True)
    organisation_id: Mapped[str] = mapped_column(
        Integer, ForeignKey("organisation.id", ondelete="cascade"), nullable=True
    )

    create_dt: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    versions = relationship("AlgoritmeVersion", back_populates="algoritme")

    organisation = relationship("Organisation", back_populates="algoritmes")

    owner = association_proxy("organisation", "org_id")
    code = association_proxy("organisation", "code")
    org_id = association_proxy("organisation", "org_id")
    preferred_name = association_proxy("organisation", "preferred_name")
