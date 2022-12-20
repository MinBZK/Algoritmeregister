from sqlalchemy import Column, Integer, VARCHAR, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Algoritme(Base):
    __tablename__ = "algoritme"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(1024))
    organization = Column(VARCHAR(1024))
    department = Column(VARCHAR(1024))
    description_short = Column(VARCHAR(1024))
    type = Column(VARCHAR(1024))
    category = Column(VARCHAR(1024))
    website = Column(VARCHAR(1024))
    status = Column(VARCHAR(1024))
    slug = Column(VARCHAR(128))

    toegevoegd_op = Column(DateTime(timezone=True), server_default=func.now())

    inzet = relationship("Inzet", back_populates="algoritme", uselist=False)
    juridisch = relationship("Juridisch", back_populates="algoritme", uselist=False)
    metadata_algorithm = relationship(
        "Metadata", back_populates="algoritme", uselist=False
    )
    toepassing = relationship("Toepassing", back_populates="algoritme", uselist=False)
    toezicht = relationship("Toezicht", back_populates="algoritme", uselist=False)
