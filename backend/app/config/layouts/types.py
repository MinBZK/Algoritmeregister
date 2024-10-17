from pydantic import BaseModel


class GenericCardGrouping(BaseModel):
    mainElement: str
    subElements: list[str]


class TabGrouping(BaseModel):
    key: str
    label: str
    rows: list[str]


class LayoutJson(BaseModel):
    genericCardGrouping: GenericCardGrouping
    tabsGrouping: list[TabGrouping]
