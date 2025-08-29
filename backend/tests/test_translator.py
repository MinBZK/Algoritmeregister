import json
from app.util.logger import get_logger
from app import models, schemas
from app.middleware.middleware import get_db
from app.controllers.algoritme_version.endpoints import apply_translation
from app.services.translation import AutoTranslator
from app.services.translation.base_translator import TranslationResult, Translator
from app.repositories import AlgoritmeVersionRepository, ActionHistoryRepository

"""Test all controllers"""

logger = get_logger(__name__)


def add(self, item: schemas.AlgoritmeVersionIn) -> schemas.AlgoritmeVersionDB:
    fields_to_add = {
        "id": 0,
        "lars": "00000000",
        "owner": "",
        "code": "",
        "org_id": "",
    }
    schema = schemas.AlgoritmeVersionDB(**item.model_dump(), **fields_to_add)
    return schema


def _cloud_translate(self, original_values: str | list, html=False) -> None | list:
    if isinstance(original_values, list):
        return [None for _ in original_values]
    return None


translation_result = TranslationResult(
    error=None, fields={}, used_service="MockTranslator"
)


class TestTranslator:
    def setup_class(self):
        self.db = next(get_db())

    def teardown_class(self):
        self.db.close()

    def test_apply_translation_v010(self, mocker):
        filename = "tests/translation_files/v0_1.json"
        with open(filename, "r") as file:
            data = json.load(file)
        schema_in = schemas.AlgoritmeVersionIn(**data[0])
        reference = schemas.AlgoritmeVersionContent(**data[1])

        mocker.patch.object(
            AlgoritmeVersionRepository,
            "add",
            add,
        )

        mocker.patch.object(
            Translator,
            "_cloud_translate",
            _cloud_translate,
        )

        mocker.patch.object(
            AutoTranslator,
            "translate",
            return_value=translation_result,
        )

        mocker.patch.object(
            ActionHistoryRepository,
            "add",
            lambda x, y: None,
        )

        algo = models.AlgoritmeVersion(**schema_in.model_dump())
        result = apply_translation(algo, self.db, "translator")
        compare_result = schemas.AlgoritmeVersionContent(**result.model_dump())
        for key in dict(schema_in).keys():
            if key not in dict(reference).keys():
                continue
            in_value = getattr(schema_in, key)
            reference_value = getattr(reference, key)
            generated_value = getattr(compare_result, key)

            print(
                f"key: {key}, In: {in_value}, Out: {generated_value}, Expected: {reference_value}"
            )
            if key == "standard_version":
                assert generated_value == "0.1"
                continue
            if in_value == "NIET VERTAALT":
                assert generated_value == "NIET VERTAALT"
            elif in_value == "AUTOMATISCH VERTAALT":
                assert generated_value != "AUTOMATISCH VERTAALT"
            elif not in_value:
                assert not generated_value
            else:  # Expecting default translation
                assert generated_value == reference_value

    def test_apply_translation_v040(self, mocker):
        filename = "tests/translation_files/v0_4.json"
        with open(filename, "r") as file:
            data = json.load(file)
        schema_in = schemas.AlgoritmeVersionIn(**data[0])
        reference = schemas.AlgoritmeVersionContent(**data[1])

        mocker.patch.object(
            AlgoritmeVersionRepository,
            "add",
            add,
        )

        mocker.patch.object(
            Translator,
            "_cloud_translate",
            _cloud_translate,
        )

        mocker.patch.object(
            AutoTranslator,
            "translate",
            return_value=translation_result,
        )

        mocker.patch.object(
            ActionHistoryRepository,
            "add",
            lambda x, y: None,
        )

        algo = models.AlgoritmeVersion(**schema_in.model_dump())
        result = apply_translation(algo, self.db, "translator")
        compare_result = schemas.AlgoritmeVersionContent(**result.model_dump())

        for key in dict(schema_in).keys():
            in_value = getattr(schema_in, key)
            if key not in dict(reference).keys():
                continue
            reference_value = getattr(reference, key)
            generated_value = getattr(compare_result, key)

            print(
                f"key: {key}, In: {in_value}, Out: {generated_value}, Expected: {reference_value}"
            )
            if key == "standard_version":
                assert generated_value == "0.4"
                continue

            if in_value == "NIET VERTAALT":
                assert generated_value in ("NIET VERTAALT", "NIET...")
            elif in_value == "AUTOMATISCH VERTAALT":
                assert generated_value != "AUTOMATISCH VERTAALT"
            elif not in_value:
                assert not generated_value
            else:  # Expecting default translation
                assert generated_value == reference_value

    def test_apply_translation_v100(self, mocker):
        filename = "tests/translation_files/v1_0.json"
        with open(filename, "r") as file:
            data = json.load(file)
        schema_in = schemas.AlgoritmeVersionIn(**data[0])
        reference = schemas.AlgoritmeVersionContent(**data[1])

        mocker.patch.object(
            AlgoritmeVersionRepository,
            "add",
            add,
        )

        mocker.patch.object(
            Translator,
            "_cloud_translate",
            _cloud_translate,
        )

        mocker.patch.object(
            AutoTranslator,
            "translate",
            return_value=translation_result,
        )

        mocker.patch.object(
            ActionHistoryRepository,
            "add",
            lambda x, y: None,
        )

        algo = models.AlgoritmeVersion(**schema_in.model_dump())
        result = apply_translation(algo, self.db, "translator")
        compare_result = schemas.AlgoritmeVersionContent(**result.model_dump())

        for key in dict(schema_in).keys():
            in_value = getattr(schema_in, key)
            if key not in dict(reference).keys():
                continue
            reference_value = getattr(reference, key)
            generated_value = getattr(compare_result, key)

            print(
                f"key: {key}, In: {in_value}, Out: {generated_value}, Expected: {reference_value}"
            )
            if key == "standard_version":
                assert generated_value == "1.0"
                continue

            if in_value == "NIET VERTAALT":
                assert generated_value in ("NIET VERTAALT", "NIET...")
            elif in_value == "AUTOMATISCH VERTAALT":
                assert generated_value != "AUTOMATISCH VERTAALT"
            elif not in_value:
                assert not generated_value
            else:  # Expecting default translation
                assert generated_value == reference_value
