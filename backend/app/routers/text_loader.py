import logging
from fastapi import APIRouter
import json
from app.config.settings import Settings

env_settings = Settings()

# Application specific code
if (env_settings.type == "PUB") or (env_settings.type == "DEV"):
    fe_api_url = "/api"
else:
    fe_api_url = "/conceptapi"

GET_URL = f"{fe_api_url}/supporting-text"
JSON_PATH = "app/data/text_loader/supporting_text.json"

# Boilerplate
if env_settings.type == "DEV":
    include_in_schema = True
else:
    include_in_schema = False

logger = logging.getLogger(__name__)
router = APIRouter()


def get_content_json() -> dict[str, dict[str, dict[str, str]]]:
    path = JSON_PATH
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
