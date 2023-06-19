from sqlalchemy import Column, Integer, VARCHAR, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class AlgoritmeVersion(Base):
    __tablename__ = "algoritme_version"

    id = Column(Integer, primary_key=True, index=True)
    algoritme_id = Column(Integer, ForeignKey("algoritme.id"), nullable=False)
    name = Column(VARCHAR(1024))
    organization = Column(VARCHAR(1024))
    department = Column(VARCHAR(1024))
    description_short = Column(VARCHAR(5000))
    type = Column(VARCHAR(1024))
    category = Column(VARCHAR(1024))
    website = Column(VARCHAR(1024))
    status = Column(VARCHAR(1024))

    # Inzet
    goal = Column(VARCHAR(5000))
    impact = Column(VARCHAR(5000))
    proportionality = Column(VARCHAR(5000))
    decision_making_process = Column(VARCHAR(5000))
    documentation = Column(VARCHAR(1024))

    # Juridisch
    competent_authority = Column(VARCHAR(1024))
    lawful_basis = Column(VARCHAR(5000))
    iama = Column(VARCHAR(128))
    iama_description = Column(VARCHAR(5000))
    dpia = Column(VARCHAR(128))
    dpia_description = Column(VARCHAR(5000))
    objection_procedure = Column(VARCHAR(5000))

    # Metadata
    standard_version = Column(VARCHAR(1024))
    uuid = Column(VARCHAR(1024))
    url = Column(VARCHAR(1024))
    contact_email = Column(VARCHAR(1024))
    area = Column(VARCHAR(1024))
    lang = Column(VARCHAR(1024))
    revision_date = Column(VARCHAR(1024))

    # Toepassing
    description = Column(VARCHAR(10000))
    application_url = Column(VARCHAR(1024))
    publiccode = Column(VARCHAR(1024))
    mprd = Column(VARCHAR(500))
    source_data = Column(VARCHAR(5000))
    methods_and_models = Column(VARCHAR(5000))

    # Toezicht
    monitoring = Column(VARCHAR(5000))
    human_intervention = Column(VARCHAR(5000))
    risks = Column(VARCHAR(5000))
    performance_standard = Column(VARCHAR(5000))

    # Additions by 0.3.1
    provider = Column(VARCHAR(200))
    process_index_url = Column(VARCHAR(500))
    tags = Column(VARCHAR(2500))
    source_id = Column(VARCHAR(100))

    # Additions by 0.4.0
    begin_date = Column(VARCHAR(7))
    end_date = Column(VARCHAR(7))
    lawful_basis_link = Column(VARCHAR(200))
    impacttoetsen = Column(VARCHAR(1024))
    source_data_link = Column(VARCHAR(500))

    published = Column(Boolean, nullable=False, default=False)
    released = Column(Boolean, nullable=False, default=False)
    preview_active = Column(Boolean, nullable=False, default=False)
    create_dt = Column(DateTime(timezone=True), server_default=func.now())

    algoritme = relationship("Algoritme", back_populates="versions")

    lars = association_proxy("algoritme", "lars")
    owner = association_proxy("algoritme", "owner")
