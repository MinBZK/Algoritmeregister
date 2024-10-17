import datetime
from pydantic import BaseModel


class HtmlFigures(BaseModel):
    date: datetime.datetime
    html: str
    static_data: dict
    most_recent: bool

    class Config:
        orm_mode = True


class HtmlFiguresOut(BaseModel):
    date: datetime.datetime
    html: str
    static_data: dict
    static: dict
