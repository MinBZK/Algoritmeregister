from app.services.algoritme_version.algoritme_version_service import (
    db_list_to_python_list,
    field_db_list_to_python_list,
)
from app import models


def test_db_list_to_python_list():
    body: dict[str, str] = {"impacttoetsen": "{a,b}", "standard_version": "0.4"}
    model = models.AlgoritmeVersion(**body)
    response = db_list_to_python_list(model)
    assert response.impacttoetsen == ["a", "b"]

    body: dict[str, str] = {"impacttoetsen": '{"a a",b}', "standard_version": "0.4"}
    model = models.AlgoritmeVersion(**body)
    response = db_list_to_python_list(model)
    assert response.impacttoetsen == ["a a", "b"]

    body: dict[str, str] = {"type": '{"a a",b}', "standard_version": "0.4"}
    model = models.AlgoritmeVersion(**body)
    response = db_list_to_python_list(model)
    assert response.type == '{"a a",b}'


def test_field_db_list_to_python_list():
    field = "{a,b}"
    response = field_db_list_to_python_list(field)
    assert response == ["a", "b"]

    field = '{"a a",b}'
    response = field_db_list_to_python_list(field)
    assert response == ["a a", "b"]

    field = "ineligible string"
    response = field_db_list_to_python_list(field)
    assert response == field
