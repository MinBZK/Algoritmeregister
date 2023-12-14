from enum import Enum
from typing import TypedDict, Literal, Tuple, Union
from reportlab.lib.colors import Color


class TextStyle(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    SUBTITLE = "subtitle"
    P = "p"
    DEFAULT = "default"


class TextEntry(TypedDict):
    type: Literal["text"]
    text: str
    style: TextStyle


class TextFieldEntry(TypedDict):
    type: Literal["textfield"]
    text: str
    key: str
    max_length: int


TextBlockConfig = list[Union[TextEntry, TextFieldEntry]]


class StyleDict(TypedDict):
    font: Tuple[str, int]
    height: int
    color: Color
