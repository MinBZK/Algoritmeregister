import datetime
from pydantic import BaseModel


class AlgoritmeIn(BaseModel):
    lars: str
    organisation_id: int


class AlgoritmeDB(AlgoritmeIn):
    id: int
    create_dt: datetime.datetime

    class Config:
        orm_mode = True
