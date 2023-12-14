import time
import uuid

import requests
import deepl

from app.config import settings
from app.util.logger import get_logger

logger = get_logger(__name__)


def azure_translate(
    original_values: list | str, source_lang: str, target_lang: str, html=False
) -> str | list:
    azure_translate_settings = settings.AzureTranslation()
    api_key = azure_translate_settings.api_key
    endpoint = azure_translate_settings.endpoint
    region = azure_translate_settings.region

    params = {
        "api-version": "3.0",
        "from": source_lang,
        "to": [target_lang],
        "textType": "html" if html else "plain",
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # You can pass more than one object in body.
    if isinstance(original_values, list):
        if not original_values:
            return []
        body = [{"text": val} for val in original_values]
    else:
        body = [{"text": original_values}]

    response = requests.post(endpoint, params=params, headers=headers, json=body)
    if response.status_code == 429:
        # pause for a minute
        logger.info(
            "Azure Translator API rate limit reached. Pausing for 60 seconds..."
        )
        time.sleep(60)
        logger.info("Resuming translation.")
        response = requests.post(endpoint, params=params, headers=headers, json=body)

    response_obj = response.json()
    translations = [obj["translations"][0]["text"] for obj in response_obj]
    if isinstance(original_values, list):
        return translations
    return translations[0]


def deepl_translate(
    original_values: list | str, source_lang: str, target_lang: str, html=False
) -> str | list:
    if target_lang == "en":
        target_lang = "EN-GB"

    if isinstance(original_values, list):
        return _handle_list_translation(original_values, source_lang, target_lang, html)
    else:
        return _handle_string_translation(
            original_values, source_lang, target_lang, html
        )


def _handle_string_translation(
    original_values: str, source_lang: str, target_lang: str, html: bool
) -> str:
    if not original_values:
        return ""
    deepl_api_key = settings.DeepLSettings().api_key
    translator = deepl.Translator(deepl_api_key)
    response = translator.translate_text(
        original_values,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="html" if html else None,
    )
    return response.text


def _handle_list_translation(
    original_values: list, source_lang: str, target_lang: str, html: bool
) -> list:
    if not original_values:
        return []
    deepl_api_key = settings.DeepLSettings().api_key
    translator = deepl.Translator(deepl_api_key)
    response = translator.translate_text(
        original_values,
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling="html" if html else None,
    )
    return [translation.text for translation in response]
