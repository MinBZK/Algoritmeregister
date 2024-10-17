from pydantic import BaseModel

from app.middleware.authorisation.schemas import Role
from .user import User
from app.middleware.authorisation.config._base import Flow


class FlowStructureRole(BaseModel):
    key: Role
    alias: str
    min_required: int
    members: list[User]


class FlowStructure(BaseModel):
    key: Flow
    alias: str
    roles: list[FlowStructureRole]
