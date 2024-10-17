from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from enum import Enum

import httpx
from pydantic import BaseModel

from app.config.settings import Settings
from app.services.translation import cloud_translators
from app.util.logger import get_logger

logger = get_logger(__name__)
settings = Settings()


class LanguageCode(str, Enum):
    DUTCH = "nl"
    ENGLISH = "en"
    FRISIAN = "fy"


class TranslationResult(BaseModel):
    error: str | None
    fields: dict[str, int | str | list | bool | None | datetime] | None
    used_service: str


class Translator(ABC):
    """
    Abstract base class for translation services.

    Subclasses must implement the translate() method.
    """

    _SERVICE_RELATED_EXCEPTIONS = [
        httpx.ConnectError,
        httpx.HTTPStatusError,
    ]

    def __init__(
        self,
        field_dict: dict[str, Any],
        source_lang: LanguageCode = LanguageCode.DUTCH,
        target_lang: LanguageCode = LanguageCode.ENGLISH,
        organisation_name: str = "",
        algorithm_name: str = "",
    ) -> None:
        self.field_dict = field_dict
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.client = None
        self.text_list = list(self.field_dict.values())
        self.text_list = [text if text else "" for text in self.text_list]
        self.organisation_name = organisation_name
        self.algorithm_name = algorithm_name

    @abstractmethod
    def translate(self, *args, **kwargs) -> TranslationResult:
        """
        Apply the translation service to the text list.
        """
        ...

    def _cloud_translate(
        self,
        original_values: str | list,
    ) -> str | list:
        """
        Fallback to cloud translation API if the original value is not found in the default_translations dict.
        """
        translation = cloud_translators.c3po_translate(
            original_values,
            self.source_lang.value,
            self.target_lang.value,
            organisation_name=self.organisation_name,
            algorithm_name=self.algorithm_name,
        )
        return translation

    def handle_response(self, response: list | dict[str, Any]) -> TranslationResult:
        """
        Decorator for the translate() method for automatic response and exception handling.

        Exception handling is applied on service related exceptions only.
        """
        class_name = self.__class__.__name__
        if isinstance(response, dict):
            result = TranslationResult(
                error=None, fields=response, used_service=class_name
            )
        elif isinstance(response, list):
            fields = dict(zip(list(self.field_dict.keys()), response))
            result = TranslationResult(
                error=None, fields=fields, used_service=class_name
            )
        else:
            raise TypeError(
                f"Expected response to be a dict or list, got {type(response)} instead."
            )
        return result
