from pydantic import BaseModel
from datetime import datetime
from typing import TypedDict
from .util import get_all_output_schemas_union


# api
class AlgorithmSummary(BaseModel):
    name: str | None
    schema_version: str | None
    last_update_dt: datetime
    lars: str
    source_id: str | None
    published: bool
    current_version_released: bool
    current_version_published: bool
    last_update_by: str | None

    class Config:
        orm_mode = True


class NewAlgorithmResponse(BaseModel):
    lars_code: str


class AlgorithmActionResponse(BaseModel):
    message: str | None


# burgerwebsite
output_schemas = get_all_output_schemas_union()


class AlgoritmeFilters(BaseModel):
    attribute: str
    value: str | list[str]


class AlgoritmeQuery(BaseModel):
    filters: list[AlgoritmeFilters] = []
    page: int = 1
    limit: int = 10
    search: str = ""


class AlgoritmeAggregation(BaseModel):
    aggregation_value: str | None
    count: int | None

    class Config:
        orm_mode = True


class AggregatedAttribute(TypedDict):
    values: list[AlgoritmeAggregation]
    aggregation_attribute: str


class AlgoritmeQueryResponse(BaseModel):
    results: list[output_schemas]  # type: ignore
    total_count: int
    aggregations: list[AggregatedAttribute]
