from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DateTime
from app.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    schema = Column(VARCHAR(1024))
    uuid = Column(VARCHAR(1024))
    url = Column(VARCHAR(1024))
    contact_email = Column(VARCHAR(1024))
    area = Column(VARCHAR(1024))
    lang = Column(VARCHAR(1024))
    revision_date = Column(VARCHAR(1024))
    algoritme_id = Column(Integer, ForeignKey("algoritme.id"))
    toegevoegd_op = Column(DateTime(timezone=True), server_default=func.now())

    algoritme = relationship("Algoritme", back_populates="metadata_algorithm")
