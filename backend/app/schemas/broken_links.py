import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)


class BrokenLinkCount(BaseModel):
    count: int
    create_dt: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
