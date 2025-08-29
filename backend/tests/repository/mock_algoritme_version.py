import datetime
from sqlalchemy.orm import Session

from app import schemas
from app.repositories.index import IRepository


class MockAlgoritmeVersionRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, item: schemas.AlgoritmeVersionIn) -> schemas.AlgoritmeVersionDB:
        fields_to_add = {
            "algoritme_id": 0,
            "language": "NLD",
            "id": 0,
            "state": "STATE_1",
            "preview_active": False,
            "create_dt": datetime.datetime(2000, 1, 1),
            "lars": "00000000",
            "owner": "",
            "code": "",
            "org_id": "",
        }
        schema = schemas.AlgoritmeVersionDB(**item.model_dump(), **fields_to_add)
        return schema
