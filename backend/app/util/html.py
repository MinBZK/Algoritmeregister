from lxml import etree
from lxml.html import document_fromstring
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from typing import Dict
import re
from pydantic import ValidationInfo


def strip_html(value: str) -> str:
    if not value.strip():
        return value
    html = document_fromstring(value)
    plain_text = " ".join(etree.XPath("//text()")(html))
    return plain_text


def sanitize_string_fields(cls, value, info: ValidationInfo):
    """Preprocess html fields by sanitization."""
    if not isinstance(value, str) or not value:
        return value

    field_name = info.field_name
    if field_name not in cls.model_fields:
        return value

    allowed_tags = cls.model_fields[field_name].json_schema_extra.get(
        "allowed_html_tags"
    )
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


def get_static_html(input: str) -> Dict:
    static_content = {}
    soup = BeautifulSoup(input, "lxml")
    for div in soup.findAll("div", attrs={"class": re.compile("scrape-element")}):
        static_content[div.get("id")] = str(div)
    for div in soup.findAll("div", attrs={"id": re.compile("^table-types-*")}):
        static_content[div.get("id")] = str(div)
    for div in soup.findAll(
        "div", attrs={"id": re.compile("^table-kwaliteitsregimes-*")}
    ):
        static_content[div.get("id")] = str(div)
    return static_content
