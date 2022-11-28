from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship


class Toezicht(Base):
    __tablename__ = "toezicht"

    id = Column(Integer, primary_key=True, index=True)
    monitoring = Column(VARCHAR(5000))
    human_intervention = Column(VARCHAR(5000))
    risks = Column(VARCHAR(5000))
    performance_standard = Column(VARCHAR(5000))
    algoritme_id = Column(Integer, ForeignKey("algoritme.id"))

    algoritme = relationship("Algoritme", back_populates="toezicht")
