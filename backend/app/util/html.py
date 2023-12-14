from lxml import etree
from lxml.html import document_fromstring
from lxml.html.clean import Cleaner


def strip_html(value: str) -> str:
    if not value:
        return value
    html = document_fromstring(value)
    plain_text = " ".join(etree.XPath("//text()")(html))
    return plain_text


def validate_html(cls, value, **kwargs):
    """Preprocess html fields by sanitization."""
    if not isinstance(value, str) or not value:
        return value

    field_name = kwargs["field"].name
    if field_name not in cls.__fields__:
        return value

    allowed_tags = cls.__fields__[field_name].field_info.extra.get("allowed_html_tags")
    if not allowed_tags:
        return strip_html(value)

    return sanitize_html(value, allowed_tags)


def sanitize_html(value: str, allowed_tags: list[str]):
    cleaner = Cleaner(
        allow_tags=allowed_tags,
        style=True,
        kill_tags=["script", "style"],
        safe_attrs_only=True,
        safe_attrs=[],
    )
    result = cleaner.clean_html(value)
    return result
