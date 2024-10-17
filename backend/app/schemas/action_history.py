from .misc import OperationEnum
from pydantic import BaseModel
import datetime


class ActionHistoryIn(BaseModel):
    algoritme_version_id: int
    operation: OperationEnum
    user_id: str
    create_dt: datetime.datetime | None = None


class ActionHistoryDB(ActionHistoryIn):
    id: int
    create_dt: datetime.datetime

    class Config:
        orm_mode = True
