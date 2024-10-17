# Define any fixtures or OS variables here
import json
import os
import pytest


MOCK_LARS_CODE = "00000000"

os.environ["RETRACT_PREVIEW_TIME"] = "1"


@pytest.fixture
def mock_json_dump(monkeypatch):
    def mock_dump(obj, file, *args, **kwargs):
        return "hello"

    monkeypatch.setattr(json, "dump", mock_dump)
