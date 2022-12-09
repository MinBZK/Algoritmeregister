from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Juridisch(Base):
    __tablename__ = "juridisch"

    id = Column(Integer, primary_key=True, index=True)
    competent_authority = Column(VARCHAR(1024))
    lawful_basis = Column(VARCHAR(5000))
    iama = Column(VARCHAR(128))
    iama_description = Column(VARCHAR(5000))
    dpia = Column(Boolean)
    dpia_description = Column(VARCHAR(5000))
    objection_procedure = Column(VARCHAR(5000))
    algoritme_id = Column(Integer, ForeignKey("algoritme.id"))
    toegevoegd_op = Column(DateTime(timezone=True), server_default=func.now())

    algoritme = relationship("Algoritme", back_populates="juridisch")
