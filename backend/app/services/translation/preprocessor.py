import json
from typing import Any

from sqlalchemy import inspect, VARCHAR
from app.database.database import Base as SQLAlchemyModel


class Preprocessor:
    """
    A class for preprocessing a model instance before translation.

    Assumed order of translation:
        1. Non-translatable fields
        4. List fields
        2. Default translate fields
        3. Auto translate fields
    """

    TRANSLATION_SPEC_FILE = "app/services/translation/translation_spec.json"

    def __init__(
        self, model_instance: SQLAlchemyModel, attrs_to_delete: list[str] = None
    ):
        self.model_instance = model_instance
        self.attrs_to_delete = set(attrs_to_delete) if attrs_to_delete else set()
        self.model_attrs = (
            set(inspect(self.model_instance).attrs.keys()) - self.attrs_to_delete
        )
        self.translation_spec = self._load_translation_spec()
        self.passed = set()

    @classmethod
    def _load_translation_spec(cls) -> dict:
        """
        Load the translation specifications from a file.

        Defines the way fields should be translated (automatically or with default values)
        """
        with open(cls.TRANSLATION_SPEC_FILE, "r") as file:
            return json.load(file)

    def _get_none_fields(self) -> set[str]:
        """
        Get the fields that have None as value and keep them.
        """
        none_fields = {
            field
            for field in self.model_attrs
            if getattr(self.model_instance, field) is None
        }
        return none_fields

    def get_non_translatable_fields(self) -> dict[str, Any]:
        """
        Get fields that don't need translation.
        """
        excluded_field_keys = set.union(
            set(self.translation_spec["auto_translate_fields"]),
            self.translation_spec["default_translations"].keys(),
            self._get_list_field_keys(),
        )
        non_translatable_field_keys = (
            self.model_attrs - excluded_field_keys
        ) | self._get_none_fields()
        return self.filter_fields(non_translatable_field_keys)

    def _get_list_field_keys(self) -> set[str]:
        return {
            field
            for field in self.model_attrs
            if isinstance(getattr(self.model_instance, field), list)
        }

    def get_list_fields(self) -> dict[str, list[str]]:
        """
        Get fields that have a list as values.

        List fields are computed by inspecting model attrs that are of type list.
        """
        list_fields = self._get_list_field_keys()
        return self.filter_fields(list_fields)

    def get_default_translate_fields(self) -> dict[str, Any]:
        """
        Get the fields that need default translation.

        Avoid translating fields that have None or a list as value.
        These are already handled by other translation methods.
        """
        default_translations = self.translation_spec["default_translations"]
        default_translate_fields = set(default_translations.keys())
        return self.filter_fields(default_translate_fields)

    def get_auto_translate_fields(self) -> dict[str, str]:
        """
        Get the fields that need translation.
        """
        auto_translate_fields = set(self.translation_spec["auto_translate_fields"])
        return self.filter_fields(auto_translate_fields)

    def filter_fields(self, field_set: set) -> dict[str, str | list]:
        """
        Utility function for returning filtered fields.
        """
        field_set = field_set - self.passed
        self.passed.update(field_set)
        fields_dict = {}
        valid_fields = self.model_attrs & field_set
        for field in valid_fields:
            value = getattr(self.model_instance, field)
            fields_dict[field] = value

        return fields_dict

    def __get_max_lengths(self) -> dict[str, int | None]:
        """
        Get the maximum lengths of the fields.
        """
        column_max_lengths = {}
        columns = self.model_instance.__table__.columns
        for column in columns:
            if isinstance(column.type, VARCHAR):
                column_max_lengths[column.name] = column.type.length
            else:
                column_max_lengths[column.name] = None

        return column_max_lengths

    def truncate_fields(self, translated_dict: dict[str, Any]):
        for field_key, value in translated_dict.items():
            max_length = self.__get_max_lengths().get(field_key)
            exceeds_max_length = (
                isinstance(value, str) and max_length and len(value) > max_length
            )
            if exceeds_max_length:
                translated_dict[field_key] = value[: max_length - 3] + "..."
