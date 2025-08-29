import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.misc import Language, PreComputedValues
from app.schemas.algoritme_version import HighlightedAlgorithmResponse


class PrecomputedValue(BaseModel):
    id: int
    language: Language
    key: PreComputedValues
    value: list[HighlightedAlgorithmResponse]
    create_dt: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class PrecomputedValueIn(BaseModel):
    language: Language
    key: PreComputedValues
    value: list[HighlightedAlgorithmResponse]

    model_config = ConfigDict(from_attributes=True)


class PrecomputedValueResponse(BaseModel):
    id: int
    create_dt: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
