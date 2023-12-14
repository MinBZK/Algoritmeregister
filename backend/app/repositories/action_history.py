from sqlalchemy.orm import Session
from app import models, schemas
from .index import IRepository


class ActionHistoryRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.ActionHistoryDB]:
        actions = self.session.query(models.ActionHistory).all()
        return [schemas.ActionHistoryDB.from_orm(a) for a in actions]

    def add(self, action: schemas.ActionHistoryIn) -> schemas.ActionHistoryDB:
        action_model = models.ActionHistory(**action.dict())
        self.session.add(action_model)
        self.session.flush()

        return schemas.ActionHistoryDB.from_orm(action_model)
