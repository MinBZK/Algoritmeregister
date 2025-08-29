from pydantic import BaseModel


class SchemaProperty(BaseModel):
    title: str
    type: str
    max_length: int | None = None
    max_items: int | None = None
    show_always: bool | None = None
    help_text: str | None = None
    instructions: str | None = None
    example: str | list[str] | None = None
    required: bool
    permitted_values: list[str] | None = None
    recommended_items: list[str] | None = None
    allowed_html_tags: list[str] | None = None
    items: dict[str, "SchemaProperty"] | None = None


class SchemaJson(BaseModel):
    properties: dict[str, SchemaProperty]
