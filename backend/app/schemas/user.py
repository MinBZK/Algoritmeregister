from pydantic import BaseModel

from app.middleware.authorisation.schemas import Role
from app.schemas.organization import OrganisationConfig


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    roles: list[Role]
    organisations: list[OrganisationConfig]
    id: str


class GetUsersResponse(BaseModel):
    users: list[User]
    count: int
