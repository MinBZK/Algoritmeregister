import pytest
from fastapi import HTTPException
from app.controllers import file_download
from app.middleware.middleware import get_db

db = next(get_db())


def test_generate_file_download():
    with pytest.raises(HTTPException):
        file_download.generate_download_file(db, org_name="sandbox")
