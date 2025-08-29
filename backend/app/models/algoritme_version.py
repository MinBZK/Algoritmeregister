import datetime
from sqlalchemy import (
    JSON,
    Index,
    Integer,
    VARCHAR,
    DateTime,
    ForeignKey,
    Boolean,
    Enum,
)

from sqlalchemy.ext.associationproxy import association_proxy
from app.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TSVECTOR
from pgvector.sqlalchemy import Vector
from app.middleware.authorisation.schemas import State
from . import Algoritme
from app.schemas import (
    Language,
    ImpacttoetsenGrouping,
    SourceDataGrouping,
    LawfulBasisGrouping,
)


class AlgoritmeVersion(Base):
    __tablename__ = "algoritme_version"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    algoritme_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("algoritme.id", ondelete="cascade"), nullable=False
    )
    language: Mapped[Language] = mapped_column(Enum(Language), nullable=False)

    name: Mapped[str | None] = mapped_column(VARCHAR(1024))
    organization: Mapped[str | None] = mapped_column(VARCHAR(1024))
    department: Mapped[str | None] = mapped_column(VARCHAR(1024))
    description_short: Mapped[str | None] = mapped_column(VARCHAR(5000))
    type: Mapped[str | None] = mapped_column(VARCHAR(1024))
    category: Mapped[str | None] = mapped_column(VARCHAR(1024))
    website: Mapped[str | None] = mapped_column(VARCHAR(1024))
    status: Mapped[str | None] = mapped_column(VARCHAR(1024))

    # Inzet
    goal: Mapped[str | None] = mapped_column(VARCHAR(5000))
    impact: Mapped[str | None] = mapped_column(VARCHAR(5000))
    proportionality: Mapped[str | None] = mapped_column(VARCHAR(5000))
    decision_making_process: Mapped[str | None] = mapped_column(VARCHAR(5000))
    documentation: Mapped[str | None] = mapped_column(VARCHAR(1024))

    # Juridisch
    competent_authority: Mapped[str | None] = mapped_column(VARCHAR(1024))
    lawful_basis: Mapped[str | None] = mapped_column(VARCHAR(5000))
    iama: Mapped[str | None] = mapped_column(VARCHAR(128))
    iama_description: Mapped[str | None] = mapped_column(VARCHAR(5000))
    dpia: Mapped[str | None] = mapped_column(VARCHAR(128))
    dpia_description: Mapped[str | None] = mapped_column(VARCHAR(5000))
    objection_procedure: Mapped[str | None] = mapped_column(VARCHAR(5000))

    # Metadata
    standard_version: Mapped[str | None] = mapped_column(VARCHAR(1024))
    uuid: Mapped[str | None] = mapped_column(VARCHAR(1024))
    url: Mapped[str | None] = mapped_column(VARCHAR(1024))
    contact_email: Mapped[str | None] = mapped_column(VARCHAR(1024))
    area: Mapped[str | None] = mapped_column(VARCHAR(1024))
    lang: Mapped[str | None] = mapped_column(VARCHAR(1024))
    revision_date: Mapped[str | None] = mapped_column(VARCHAR(1024))

    # Toepassing
    description: Mapped[str | None] = mapped_column(VARCHAR(10000))
    application_url: Mapped[str | None] = mapped_column(VARCHAR(1024))
    publiccode: Mapped[str | None] = mapped_column(VARCHAR(1024))
    mprd: Mapped[str | None] = mapped_column(VARCHAR(500))
    source_data: Mapped[str | None] = mapped_column(VARCHAR(5000))
    methods_and_models: Mapped[str | None] = mapped_column(VARCHAR(10000))

    # Toezicht
    monitoring: Mapped[str | None] = mapped_column(VARCHAR(5000))
    human_intervention: Mapped[str | None] = mapped_column(VARCHAR(5000))
    risks: Mapped[str | None] = mapped_column(VARCHAR(5000))
    performance_standard: Mapped[str | None] = mapped_column(VARCHAR(5000))

    # Additions by 0.3.1
    provider: Mapped[str | None] = mapped_column(VARCHAR(5000))
    process_index_url: Mapped[str | None] = mapped_column(VARCHAR(500))
    tags: Mapped[str | None] = mapped_column(VARCHAR(2500))
    source_id: Mapped[str | None] = mapped_column(VARCHAR(100))

    # Additions by 0.4
    begin_date: Mapped[str | None] = mapped_column(VARCHAR(7))
    end_date: Mapped[str | None] = mapped_column(VARCHAR(7))
    lawful_basis_link: Mapped[str | None] = mapped_column(VARCHAR(5000))
    impacttoetsen: Mapped[str | None] = mapped_column(VARCHAR(5000))
    source_data_link: Mapped[str | None] = mapped_column(VARCHAR(500))

    # Additions by 1.0
    publication_category: Mapped[str | None] = mapped_column(VARCHAR(1000))
    lawful_basis_grouping: Mapped[list[LawfulBasisGrouping] | None] = mapped_column(
        JSON
    )
    impacttoetsen_grouping: Mapped[list[ImpacttoetsenGrouping] | None] = mapped_column(
        JSON
    )
    source_data_grouping: Mapped[list[SourceDataGrouping] | None] = mapped_column(JSON)

    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    released: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    preview_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    create_dt: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    vector: Mapped[str | None] = mapped_column(TSVECTOR)

    # Added with new publicationproces
    state: Mapped[State] = mapped_column(
        VARCHAR, nullable=False, server_default=State.STATE_1
    )

    algoritme: Mapped[Algoritme] = relationship("Algoritme", back_populates="versions")

    lars = association_proxy("algoritme", "lars")
    owner = association_proxy("algoritme", "owner")
    code = association_proxy("algoritme", "code")
    org_id = association_proxy("algoritme", "org_id")
    preferred_name = association_proxy("algoritme", "preferred_name")

    # Added embedding column
    embedding_nfi: Mapped[Vector | None] = mapped_column(Vector)


vector_index = Index("gin_idx", AlgoritmeVersion.vector, postgresql_using="gin")
