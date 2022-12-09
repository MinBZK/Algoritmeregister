from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Toepassing(Base):
    __tablename__ = "toepassing"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(VARCHAR(10000))
    application_url = Column(VARCHAR(1024))
    publiccode = Column(VARCHAR(1024))
    mprd = Column(Boolean)
    source_data = Column(VARCHAR(5000))
    methods_and_models = Column(VARCHAR(5000))
    algoritme_id = Column(Integer, ForeignKey("algoritme.id"))
    toegevoegd_op = Column(DateTime(timezone=True), server_default=func.now())

    algoritme = relationship("Algoritme", back_populates="toepassing")
