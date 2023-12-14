from .base_translator import Translator


class AutoTranslator(Translator):
    _PUNCTUATION_MARKS = ".,;:!?"

    def translate(self):
        translated_texts = self._cloud_translate(self.text_list, html=True)
        translated_texts = self.__fix_anchor_punctuation(translated_texts)
        translated_fields = self.handle_response(translated_texts)
        return translated_fields

    def __fix_anchor_punctuation(self, translations: list[str]) -> list[str]:
        """
        Removes spaces between anchor tags and punctuation marks.
        """
        for mark in self._PUNCTUATION_MARKS:
            for i, sentence in enumerate(translations):
                translations[i] = sentence.replace(f"</a> {mark}", f"</a>{mark}")
        return translations
