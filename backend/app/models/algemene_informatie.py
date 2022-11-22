from sqlalchemy import Column, Integer, VARCHAR
from app.database.database import Base
from sqlalchemy.orm import relationship


class AlgemeneInformatie(Base):
    __tablename__ = "algemene_informatie"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(1024))
    organization = Column(VARCHAR(1024))
    department = Column(VARCHAR(1024))
    description_short = Column(VARCHAR(1024))
    type = Column(VARCHAR(1024))
    category = Column(VARCHAR(1024))
    website = Column(VARCHAR(1024))
    status = Column(VARCHAR(1024))

    inzet_entity = relationship(
        "Inzet", back_populates="algemene_informatie_entity", uselist=False
    )
    juridisch_entity = relationship(
        "Juridisch", back_populates="algemene_informatie_entity", uselist=False
    )
    metadata_entity = relationship(
        "Metadata", back_populates="algemene_informatie_entity", uselist=False
    )
    toepassing_entity = relationship(
        "Toepassing", back_populates="algemene_informatie_entity", uselist=False
    )
    toezicht_entity = relationship(
        "Toezicht", back_populates="algemene_informatie_entity", uselist=False
    )
