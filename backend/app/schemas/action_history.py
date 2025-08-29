from .misc import OperationEnum
from pydantic import BaseModel, ConfigDict
import datetime


class ActionHistoryIn(BaseModel):
    algoritme_version_id: int
    operation: OperationEnum
    user_id: str
    create_dt: datetime.datetime | None = None


class ActionHistoryDB(ActionHistoryIn):
    id: int
    create_dt: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
