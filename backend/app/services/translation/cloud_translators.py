import time
import uuid
from fastapi import HTTPException, status

import requests

import deepl

from app.config import settings
from app.services.c3po import handle_c3po_exception
from app.util.logger import get_logger

logger = get_logger(__name__)
env_settings = settings.Settings()


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


def c3po_translate(
    original_values: list | str,
    source_lang: str,
    target_lang: str,
    organisation_name: str = "",
    algorithm_name: str = "",
) -> str | list:
    """
    Translates Dutch text to English or Frisian using the C3PO API.

    :return: The translated values. Depending on the input, it is either a string or a list.

    :raises ValueError: If the target language is not supported
    :raises httpx.ConnectError: If the connection with the C3PO API fails
    :raises httpx.HTTPStatusError: If the request to the C3PO API fails
    """
    if source_lang != "nl":
        raise ValueError(f"Unsupported source language: {source_lang}")

    if target_lang == "en":
        rule_code = "ENGLISH_TRANSLATION"
    elif target_lang == "fy":
        rule_code = "FRISIAN_TRANSLATION"
    else:
        raise ValueError(f"Unsupported target language: {target_lang}")

    request_body = {
        "payload": original_values,
        "rule_code": rule_code,
        "org_code": "ictu-devops",
        "project_code": "algreg",
    }

    try:
        response = requests.post(
            f"{env_settings.c3po_url}/processing-request/", json=request_body
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        handle_c3po_exception(e, rule_code, organisation_name, algorithm_name)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="EXPERT_SERVICE_CONN_ERROR",
        )
    return response.json()["result"]


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
