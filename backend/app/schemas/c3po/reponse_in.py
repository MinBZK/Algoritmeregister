from typing import Any, Optional, Union

from pydantic import BaseModel
from enum import Enum
import datetime


class TaskStatus(str, Enum):
    NEW = "new"
    PENDING = "pending"
    FINISHED = "finished"
    ERROR = "error"


class SeverityLevel(str, Enum):
    INFO = "info"
    WARNING = "waarschuwing"
    ERROR = "fout"


class Rule(BaseModel):
    id: int
    rule_code: str
    title: str
    rule_type: str
    description: str
    severity_level: SeverityLevel
    created_at: datetime.datetime


class Task(BaseModel):
    id: int
    processing_request_id: int
    feedback_message: str | None
    result: Optional[Union[str, list[Any], dict[str, Any]]]
    status: TaskStatus
    passed: bool | None
    created_at: datetime.datetime
    rule: Rule


class ProcessingRequest(BaseModel):
    id: int
    payload: str
    tasks: list[Task]
    created_at: datetime.datetime
    updated_at: datetime.datetime
