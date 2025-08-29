import datetime
from pydantic import BaseModel, ConfigDict


class HtmlFigures(BaseModel):
    date: datetime.datetime
    html: str
    static_data: dict
    most_recent: bool

    model_config = ConfigDict(from_attributes=True)


class HtmlFiguresOut(BaseModel):
    date: datetime.datetime
    html: str
    static_data: dict
    static: dict
