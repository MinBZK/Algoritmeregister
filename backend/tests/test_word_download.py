import pytest
import json
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException

from app.controllers import word_download
from app.middleware.middleware import get_db
from app import schemas

db = next(get_db())


def dummy_org_data() -> list[schemas.AlgoritmeVersionDB]:
    filename = "tests/files/db_output_1.json"
    with open(filename, "r") as file:
        content = json.load(file)

    return [schemas.AlgoritmeVersionDB(**c) for c in content]


def mocked_db_org_data() -> list[schemas.AlgoritmeVersionDB]:
    mock_db_response = dummy_org_data()
    return mock_db_response


def test_get_org_data(mocker):
    content = dummy_org_data()
    mock_db_response = mocked_db_org_data()
    mocker.patch(
        "app.controllers.word_download.AlgoritmeVersionRepository.get_latest_by_org_by_lang",
        return_value=mock_db_response,
    )
    org_name = "sandbox"
    response = word_download.get_org_data(db, org_name)
    for i, algorithm in enumerate(response):
        assert algorithm.name == content[i].name
        assert algorithm.standard_version == content[i].standard_version
        assert algorithm.lars == content[i].lars


def test_get_algo_data(mocker):
    content = dummy_org_data()[0]
    mock_db_response = mocked_db_org_data()[0]
    mocker.patch(
        "app.controllers.word_download.AlgoritmeVersionRepository.get_latest_by_lars_by_lang",
        return_value=mock_db_response,
    )
    response = word_download.get_algo_data(db, content.lars)

    if not response:
        raise ValueError
    assert response.name == content.name
    assert response.standard_version == content.standard_version
    assert response.lars == content.lars


def test_generate_word_download1(mocker):
    mock_db_response = mocked_db_org_data()
    mocker.patch(
        "app.controllers.word_download.AlgoritmeVersionRepository.get_latest_by_org_by_lang",
        return_value=mock_db_response,
    )

    org_name = "sandbox"
    response = word_download.generate_word_download(db, org_name=org_name)
    assert isinstance(response, StreamingResponse)


def test_generate_word_download2(mocker):
    mock_db_response = mocked_db_org_data()[0]
    mocker.patch(
        "app.controllers.word_download.AlgoritmeVersionRepository.get_latest_by_lars_by_lang",
        return_value=mock_db_response,
    )

    lars = "mock_lars"
    response = word_download.generate_word_download(db, lars=lars)
    assert isinstance(response, StreamingResponse)

    with pytest.raises(Exception):
        word_download.generate_word_download(db)

    mocker.patch(
        "app.controllers.word_download.get_one_algorithm_doc",
        return_value=(None, "mock_filename"),
    )
    with pytest.raises(HTTPException):
        word_download.generate_word_download(db, lars=lars)


def test_get_one_algorithm_doc(mocker):
    # Only empty data is tested
    mocker.patch("app.controllers.word_download.get_algo_data", return_value=None)
    lars = "mock_lars"
    response = word_download.get_one_algorithm_doc(db, lars)
    assert response == (None, None)


def test_get_all_algorithm_doc(mocker):
    mocker.patch("app.controllers.word_download.get_org_data", return_value=[])
    lars = "mock_lars"
    response = word_download.get_all_algorithm_doc(db, lars)
    assert response == (None, None)
