from .base_translator import Translator


class DefaultValuesTranslator(Translator):
    def translate(self, translation_spec: dict[str, dict]):
        raw_result = self.apply_default_translations(translation_spec)
        return self.handle_response(raw_result)

    def apply_default_translations(
        self, default_translations: dict[str, dict]
    ) -> dict[str, str]:
        new_field_dict = self.field_dict.copy()
        for field_key, original_value in new_field_dict.items():
            original_value = original_value.strip()
            if original_value in default_translations[field_key].keys():
                new_value = default_translations[field_key][original_value]
                new_field_dict[field_key] = new_value
            else:
                fallback_translation = self._cloud_translate(original_value)
                new_field_dict[field_key] = fallback_translation

        return new_field_dict
