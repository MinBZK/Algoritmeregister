import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.misc import Language


class BrokenLink(BaseModel):
    id: int
    name: str
    lars: str
    broken_links: list[tuple[str, Optional[int]]]
    language: Language
    create_dt: datetime.datetime
    organisation: str
    batch: int

    class Config:
        orm_mode = True


class BrokenLinkCount(BaseModel):
    count: int
    create_dt: datetime.datetime

    class Config:
        orm_mode = True
