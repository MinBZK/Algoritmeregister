from sqlalchemy import Column, Integer, DateTime, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Algoritme(Base):
    __tablename__ = "algoritme"

    id = Column(Integer, primary_key=True, index=True)
    lars = Column(VARCHAR(8), nullable=True, index=True)
    owner = Column(VARCHAR(1024), nullable=True)

    create_dt = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    versions = relationship("AlgoritmeVersion", back_populates="algoritme")
