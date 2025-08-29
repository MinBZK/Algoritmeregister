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
        self,
        field_key: str,
        original_list: list,
        default_translations: dict[str, dict],
        translate_key: str = "title",
    ) -> list[str]:
        """
        Translate a list of strings OR dicts with a translate_key field.

        If a string is not found in the default_translations dict, the original string is kept.
        """
        new_list = []
        translations = default_translations.get(field_key, {})
        for original_value in original_list:
            if isinstance(original_value, dict) and translate_key in original_value:
                translate_value = original_value.get(translate_key)
                if isinstance(translate_value, str):
                    translate_value = translate_value.strip()
                    translated = translations.get(
                        translate_value
                    ) or self._cloud_translate(translate_value)
                    original_value[translate_key] = translated
                new_list.append(original_value)

            elif isinstance(original_value, str):
                original_value = original_value.strip()
                translated = translations.get(original_value) or self._cloud_translate(
                    original_value
                )
                new_list.append(translated)
            else:
                new_list.append(original_value)

        return new_list
