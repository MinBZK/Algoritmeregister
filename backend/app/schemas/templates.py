from pydantic import BaseModel


class TemplateSummary(BaseModel):
    name: str
    id: str


class StandardSupplier(BaseModel):
    name: str
    algorithm_descriptions: list[TemplateSummary]
