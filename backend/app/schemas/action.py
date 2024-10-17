from enum import Enum
from pydantic import BaseModel

from app.middleware.authorisation.schemas import State


class EmailType(Enum):
    RELEASE_ICTU_LAST = "release_ictu_last"
    RELEASE_SELF_PUBLISH_TWO = "release_self_publish_two"
    RETRACT = "retract"


class StateChangeActionOut(BaseModel):
    label: str
    key: str
    enabled: bool = True
    origin_state: State
    target_state: State


class StateChangeAction(StateChangeActionOut):
    send_email_type: EmailType | None = None


class StateChangeRequest(BaseModel):
    origin_state: State
    target_state: State
