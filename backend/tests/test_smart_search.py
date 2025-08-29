import json
import os
import re
from contextlib import contextmanager
from pathlib import Path
from typing import Any, List, Optional, cast

import delayed_assert
import pytest
import yaml
from fastapi.testclient import TestClient
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models, repositories, schemas
from app.main import app
from app.middleware.authorisation.schemas import State
from app.middleware.middleware import get_db
from app.schemas.misc import Language
from app.middleware.authorisation.config._base import Flow

TESTDATA_DIR = Path("tests/smart_search/data")
QUERIES_YAML = Path("tests/smart_search/queries.yaml")
QUERY_LIMIT = 100


class Query(BaseModel):
    woord: str
    id: int
    expected: List[int]
    lang: Language


class Queries(BaseModel):
    spelfouten: Optional[List[Query]]
    synoniemen: Optional[List[Query]]
    combinaties: Optional[List[Query]]
    suggesties: Optional[List[Query]]


class NoDataError(Exception):
    pass


class IDAlreadyExists(Exception):
    pass


@contextmanager
def cd(dest: Path):
    curr_dir = Path().absolute()
    try:
        os.chdir(dest)
        yield
    finally:
        os.chdir(curr_dir)


class GenTestData:
    @classmethod
    def queries_yaml_to_dict(cls, filename: Path) -> Queries:
        with open(filename, "rb") as filehandler:
            return Queries.parse_obj(yaml.safe_load(filehandler))

    @classmethod
    def _dict_to_json(cls, payload: dict, filename: str, directory: Path) -> bool:
        with cd(directory):
            try:
                with open(filename, "w") as filehandler:
                    json.dump(payload, filehandler)
                    return True
            except Exception:
                pass

            return False

    @classmethod
    def _check_file_exist(cls, filename: str, directory: Path) -> bool:
        with cd(directory):
            return True if filename in os.listdir() else False

    @classmethod
    def find_file_by_id(cls, id: int, data_dir: Path) -> str | None:
        with cd(data_dir):
            files = os.listdir()
            regex = re.compile(r"\d+")

            matching_files = [
                file
                for file in files
                if file.endswith(".json") and id == int(regex.findall(file)[0])
            ]

            return next(iter(matching_files), None)

    @classmethod
    def calling_smart_search_endpoint(
        cls, client: TestClient, query: Query
    ) -> schemas.AlgoritmeQueryResponse | None:
        endpoint = f"api/algoritme/{query.lang.value}"
        body = schemas.AlgoritmeQuery(limit=QUERY_LIMIT, searchtext=query.woord).model_dump()

        try:
            response = client.post(endpoint, json=body)
        except Exception as exc:
            print(f"Calling post endpoint failed: {query}; msg: {exc}")
            return

        if response.status_code != 200:
            raise RuntimeError("Request returned HTTP code {response.status_code}")

        return schemas.AlgoritmeQueryResponse(**response.json())

    @classmethod
    def calling_suggestion_endpoint(
        cls, client: TestClient, query: Query
    ) -> schemas.SearchSuggestionResponse | None:
        endpoint = f"api/suggestion/{query.lang.value}/{query.woord}"

        try:
            response = client.get(endpoint)
        except Exception as exc:
            print(f"Calling get endpoint failed: {query}; msg: {exc}")
            return

        if response.status_code != 200:
            raise RuntimeError("Request returned HTTP code {response.status_code}")

        return schemas.SearchSuggestionResponse(**response.json())


class ConfigMockDB:
    @classmethod
    def _clear_db_tables(cls, table_model: Any, session: Session) -> None:
        session.query(table_model).delete()
        session.commit()

    @classmethod
    def json_to_schema(
        cls, filename: Path
    ) -> list[schemas.AlgoritmeVersionContent] | None:
        try:
            with open(filename, "rb") as filehandler:
                json_obj = json.load(filehandler)
                if json_obj:
                    return [
                        schemas.AlgoritmeVersionContent(**item) for item in json_obj
                    ]
        except Exception as exc:
            print(f"Failed to load json to schema: {exc}")

    @classmethod
    def algoritme_version_json_to_db(cls, filepath: Path, session: Session) -> None:
        cls._clear_db_tables(models.Organisation, session)

        algoritme_version_repo = repositories.AlgoritmeVersionRepository(session)
        algoritme_repo = repositories.AlgoritmeRepository(session)
        organisation_repo = repositories.OrganisationRepository(session)

        if (algo_data_set := cls.json_to_schema(filepath)) is None:
            print(f"Json file: {filepath} is empty")
            raise NoDataError(
                f"Failed to load JSON. Check if file exists {filepath} or file is empty"
            )

        # Creates new entry in organization table.
        org = organisation_repo.add(
            schemas.OrganisationIn(
                code="x",
                org_id="x",
                type=schemas.OrgType.overig,
                show_page=False,
                flow=Flow.ICTU_LAST,
            )
        )
        for unique_id, algo_data in enumerate(algo_data_set):
            algoritme = schemas.AlgoritmeIn(lars=str(unique_id), organisation_id=org.id)
            algoritme_db = algoritme_repo.add(algoritme)

            # lars-code is used for assert later, and must match the algoritme_id.
            # assert unique_id == algoritme_db.id, "lars-code must equal algoritme.id"

            # Creates new entry in algoritme_version table.
            algoritme_version = schemas.AlgoritmeVersionIn(
                **algo_data.model_dump(),
                algoritme_id=algoritme_db.id,
                language=Language.NLD,
                state=State.PUBLISHED,
            )
            algoritme_version_repo.add(algoritme_version)


class TestSmartSearch:
    @classmethod
    def setup_class(cls) -> None:
        cls.client = TestClient(app)
        cls.session = next(get_db())
        cls.queries = GenTestData.queries_yaml_to_dict(QUERIES_YAML)

    @classmethod
    def teardown_class(cls) -> None:
        cls.session.query(models.Organisation).delete()
        cls.session.commit()
        cls.session.close()

    @classmethod
    def run_test_smart_search_endpoint(
        cls, query: Query
    ) -> schemas.AlgoritmeQueryResponse | None:
        json_file = GenTestData.find_file_by_id(id=query.id, data_dir=TESTDATA_DIR)
        if not json_file:
            raise RuntimeError(f"Failed to find json_file with id: {query.id}")

        ConfigMockDB.algoritme_version_json_to_db(
            filepath=TESTDATA_DIR / json_file, session=cls.session
        )

        return GenTestData.calling_smart_search_endpoint(cls.client, query)

    @classmethod
    def run_test_suggestion_endpoint(
        cls, query: Query
    ) -> schemas.SearchSuggestionResponse | None:
        json_file = GenTestData.find_file_by_id(id=query.id, data_dir=TESTDATA_DIR)
        if not json_file:
            raise RuntimeError(f"Failed to find json_file with id: {query.id}")

        ConfigMockDB.algoritme_version_json_to_db(
            filepath=TESTDATA_DIR / json_file, session=cls.session
        )

        return GenTestData.calling_suggestion_endpoint(cls.client, query)

    @classmethod
    def assert_response_smart_search(
        cls, query: Query, response: schemas.AlgoritmeQueryResponse
    ) -> None:
        delayed_assert.expect(
            response.total_count == len(query.expected),
            f"Assertion fails for query: {query.woord}, { response.total_count } != {len(query.expected)},\
            because amount expected does not match results amount",
        )
        delayed_assert.expect(
            (cast(int, item.lars) in query.expected for item in response.results),
            f"Assertion fails for query: {query.woord}",
        )

    @classmethod
    def assert_response_suggestion(
        cls, query: Query, response: schemas.SearchSuggestionResponse
    ) -> None:
        delayed_assert.expect(
            (cast(int, item.lars) in query.expected for item in response.algorithms),
            f"Assertion fails for query: {query.woord}",
        )

    def test_synonyms(self):
        if not self.queries.synoniemen:
            pytest.skip("No synoniemen given")

        for query in self.queries.synoniemen:
            response = self.run_test_smart_search_endpoint(query)
            if not response:
                raise NoDataError(
                    f"No data retrieved for query {query.woord}; Check database"
                )
            self.assert_response_smart_search(query, response)
        delayed_assert.assert_expectations()

    def test_combinations(self) -> None:
        if not self.queries.combinaties:
            pytest.skip("No combinaties given")

        for query in self.queries.combinaties:
            response = self.run_test_smart_search_endpoint(query)
            if not response:
                raise NoDataError(
                    f"No data retrieved for query {query.woord}; Check database"
                )
            self.assert_response_smart_search(query, response)
        delayed_assert.assert_expectations()

    def test_spelling_mistakes(self):
        if not self.queries.spelfouten:
            pytest.skip("No spelfouten given")

        for query in self.queries.spelfouten:
            response = self.run_test_smart_search_endpoint(query)
            if not response:
                raise NoDataError(
                    f"No data retrieved for query {query.woord}; Check database"
                )
            self.assert_response_smart_search(query, response)
        delayed_assert.assert_expectations()

    def test_search_suggestion(self):
        if not self.queries.suggesties:
            pytest.skip("No suggesties given")

        for query in self.queries.suggesties:
            response = self.run_test_suggestion_endpoint(query)
            if not response:
                raise NoDataError(
                    f"No data retrieved for query {query.woord}; Check database"
                )
            self.assert_response_suggestion(query, response)
        delayed_assert.assert_expectations()
