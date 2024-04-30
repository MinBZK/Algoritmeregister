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
    WARNING = "warning"
    ERROR = "error"


class Rule(BaseModel):
    rule_id: int
    rule_code: str
    rule_variant: str
    description: str
    python_reference: str
    severity_level: SeverityLevel
    created_at: datetime.datetime


class Task(BaseModel):
    task_id: int
    processing_request_id: int
    feedback_message: str | None
    result: bool | None
    status: TaskStatus | None
    created_at: datetime.datetime
    rule: Rule


class ProcessingRequest(BaseModel):
    processing_request_id: int
    payload: str
    tasks: list[Task]
    created_at: datetime.datetime
    updated_at: datetime.datetime
