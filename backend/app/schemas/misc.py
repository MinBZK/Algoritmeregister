from pydantic import BaseModel


class User(BaseModel):
    name: str | None
    organizations: list[str]
    role: str | None


class Message(BaseModel):
    detail: str


class PreviewUrl(BaseModel):
    url: str
