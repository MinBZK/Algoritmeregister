from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Inzet(Base):
    __tablename__ = "inzet"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(VARCHAR(5000))
    impact = Column(VARCHAR(5000))
    proportionality = Column(VARCHAR(5000))
    decision_making_process = Column(VARCHAR(5000))
    documentation = Column(VARCHAR(1024))

    algoritme_id = Column(Integer, ForeignKey("algoritme.id"))
    toegevoegd_op = Column(DateTime(timezone=True), server_default=func.now())

    algoritme = relationship("Algoritme", back_populates="inzet")
