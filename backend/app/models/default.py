from sqlalchemy import Column, Integer
from app.database.database import Base


class AlgemeneInformatie(Base):
    __tablename__ = "algemene_informatie"

    id = Column(Integer, primary_key=True, index=True)
