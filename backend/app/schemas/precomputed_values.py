import datetime
from pydantic import BaseModel
from app.schemas.misc import Language, PreComputedValues


class PrecomputedValue(BaseModel):
    id: int
    language: Language
    key: PreComputedValues
    value: list[dict[str, str]]
    create_dt: datetime.datetime

    class Config:
        orm_mode = True


class PrecomputedValueIn(BaseModel):
    language: Language
    key: PreComputedValues
    value: list[dict[str, str]]

    class Config:
        orm_mode = True


class PrecomputedValueResponse(BaseModel):
    id: int
    create_dt: datetime.datetime

    class Config:
        orm_mode = True
