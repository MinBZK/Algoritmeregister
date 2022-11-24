from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship


class Juridisch(Base):
    __tablename__ = "juridisch"

    id = Column(Integer, primary_key=True, index=True)
    competent_authority = Column(VARCHAR(1024))
    lawful_basis = Column(VARCHAR(5000))
    dpia = Column(Boolean)
    dpia_description = Column(VARCHAR(5000))
    objection_procedure = Column(VARCHAR(5000))
    algoritme_id = Column(Integer, ForeignKey("algemene_informatie.id"))

    algemene_informatie = relationship("AlgemeneInformatie", back_populates="juridisch")
