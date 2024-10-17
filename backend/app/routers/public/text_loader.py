import logging
from fastapi import APIRouter, Body
import json
import os
from app.config.settings import Settings

env_settings = Settings()

GET_URL = "/api/supporting-text"
JSON_PATH = "app/data/text_loader/supporting_text.json"
JSON_DEFAULT_PATH = "app/data/static_content_default.json"

include_in_schema = False

logger = logging.getLogger(__name__)
router = APIRouter()


def get_content_json() -> dict[str, dict[str, dict[str, str]]]:
    path = JSON_PATH if os.path.exists(JSON_PATH) else JSON_DEFAULT_PATH
    with open(path) as f:
        content: dict[str, dict[str, dict[str, str]]] = json.load(f)
    return content


@router.get(GET_URL)
async def get_all_content():
    """
    Fetch all content.

    :return: Content in dictionary format: lang { group { field { key, label } }}
    """
    content = get_content_json()
    return content
