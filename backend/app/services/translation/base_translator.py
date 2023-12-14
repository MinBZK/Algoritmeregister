from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from enum import Enum

from pydantic import BaseModel
from deepl import DeepLException

from app.services.translation import cloud_translators


class LanguageCode(str, Enum):
    DUTCH = "nl"
    ENGLISH = "en"
    FRYSIAN = "fy"


class TranslationResult(BaseModel):
    error: str | None
    fields: dict[str, int | str | list | bool | None | datetime] | None
    used_service: str


class Translator(ABC):
    """
    Abstract base class for translation services.

    Subclasses must implement the translate() method.
    """

    _SERVICE_RELATED_EXCEPTIONS = (DeepLException,)

    def __init__(
        self,
        field_dict: dict[str, Any],
        source_lang: LanguageCode = LanguageCode.DUTCH,
        target_lang: LanguageCode = LanguageCode.ENGLISH,
    ) -> None:
        self.field_dict = field_dict
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.client = None
        self.text_list = list(self.field_dict.values())
        self.text_list = [text if text else "" for text in self.text_list]

    @abstractmethod
    def translate(self, *args, **kwargs) -> TranslationResult:
        """
        Apply the translation service to the text list.
        """
        ...

    def _cloud_translate(self, original_values: str | list, html=False) -> str | list:
        """
        Fallback to cloud translation API if the original value is not found in the default_translations dict.
        """
        return cloud_translators.deepl_translate(
            original_values, self.source_lang.value, self.target_lang.value, html
        )

    @classmethod
    def _handle_exceptions(self, error: Exception) -> str:
        """
        Generate an informative error message.

        Distinct messages are returned for service related exceptions and unknown exceptions.
        """
        if isinstance(error, tuple(Translator._SERVICE_RELATED_EXCEPTIONS)):
            return (
                f"Bij het aanroepen van de {self.__class__.__name__} service is een fout opgetreden"
                f" van het type '{type(error).__name__}'."
            )

        return "Er is een onbekende fout opgetreden bij het vertalen van de tekst, zie logging voor details."

    def handle_response(self, response: list | dict[str, Any]) -> TranslationResult:
        """
        Decorator for the translate() method for automatic response and exception handling.

        Exception handling is applied on service related exceptions only.
        """
        class_name = self.__class__.__name__
        try:
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
        except Exception as error:
            error = self._handle_exceptions(error)
            return TranslationResult(error=error, fields=None, used_service=class_name)
