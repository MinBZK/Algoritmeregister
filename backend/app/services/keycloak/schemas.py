from pydantic import BaseModel
from datetime import datetime


class KeycloakUser(BaseModel):
    groups: list[str]
    roles: list[str]
    first_name: str
    last_name: str
    username: str
    id: str


class KeycloakUserFromRepo(KeycloakUser):
    created_at: datetime


class KeycloakUserUpdate(BaseModel):
    groups: list[str] | None = None
    roles: list[str] | None = None
    first_name: str | None = None
    last_name: str | None = None


class KeycloakUserNew(KeycloakUserUpdate):
    username: str


class KeycloakGroup(BaseModel):
    name: str
    id: str
