from sqlalchemy import Column, Integer, DateTime, VARCHAR, Enum
import enum
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base


class OperationEnum(str, enum.Enum):
    created = "created"
    new_version = "new version"
    released = "released"
    published = "published"
    retracted = "retracted"
    preview_activated = "preview activated"
    preview_used = "preview used"
    preview_timeout = "preview timeout"
    removed = "removed"


class ActionHistory(Base):
    __tablename__ = "action_history"

    id = Column(Integer, primary_key=True, index=True)
    algoritme_version_id = Column(
        Integer, ForeignKey("algoritme_version.id"), nullable=False
    )
    operation = Column(Enum(OperationEnum), nullable=False)
    user_id = Column(VARCHAR(1024), nullable=False)

    create_dt = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
