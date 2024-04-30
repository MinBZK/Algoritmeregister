from app.database.database import Base
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class Words(Base):
    __tablename__ = "words"

    word: Mapped[str | None] = mapped_column(Text, primary_key=True)
