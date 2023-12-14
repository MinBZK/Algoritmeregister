from .base_translator import Translator


class ListValuesTranslator(Translator):
    def translate(self, translation_spec: dict[str, dict]):
        new_field_dict = self.field_dict.copy()
        for field_key, original_list in new_field_dict.items():
            translated_list = self.translate_list(
                field_key, original_list, translation_spec
            )
            new_field_dict[field_key] = translated_list

        return self.handle_response(new_field_dict)

    def translate_list(
        self, field_key: str, original_list: list, default_translations: dict[str, dict]
    ) -> list[str]:
        """
        Translate a list of strings.

        If a string is not found in the default_translations dict, the original string is kept.
        """

        new_list = []
        for original_value in original_list:
            if type(original_value) is not str:
                new_list.append(original_value)
                continue
            original_value = original_value.strip()
            if original_value in default_translations[field_key].keys():
                new_value = default_translations[field_key][original_value]
                new_list.append(new_value)
            else:
                fallback_translation = self._cloud_translate(original_value)
                new_list.append(fallback_translation)
        return new_list
