from pydantic import BaseModel


class SchemaProperty(BaseModel):
    title: str
    type: str
    max_length: int | None
    max_items: int | None
    show_always: bool | None
    help_text: str | None
    instructions: str | None
    example: str | list[str] | None
    required: bool
    permitted_values: list[str] | None
    recommended_items: list[str] | None
    allowed_html_tags: list[str] | None
    items: dict[str, "SchemaProperty"] | None


class SchemaJson(BaseModel):
    properties: dict[str, SchemaProperty]
