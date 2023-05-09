from pydantic import BaseModel


class Content(BaseModel):
    html: str
    lang: str
