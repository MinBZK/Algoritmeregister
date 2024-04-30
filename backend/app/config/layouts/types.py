from pydantic import BaseModel


class HeaderCardGrouping(BaseModel):
    mainElement: str
    subElements: list[str]


class TabGrouping(BaseModel):
    key: str
    label: str
    rows: list[str]


class LayoutJson(BaseModel):
    headerCardGrouping: HeaderCardGrouping
    tabsGrouping: list[TabGrouping]
