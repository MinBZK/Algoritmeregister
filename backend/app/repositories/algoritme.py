from sqlalchemy.orm import Session
from app import models, schemas
from .index import IRepository


class AlgoritmeRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.commit()

    def get_all(self) -> list[schemas.AlgoritmeDB]:
        algoritmes = self.session.query(models.Algoritme).all()
        return [schemas.AlgoritmeDB.from_orm(a) for a in algoritmes]

    def get_by_lars(self, lars: str) -> schemas.AlgoritmeDB | None:
        algoritme = (
            self.session.query(models.Algoritme)
            .filter(models.Algoritme.lars == lars)
            .first()
        )
        if not algoritme:
            return None
        return schemas.AlgoritmeDB.from_orm(algoritme)

    def add(self, item: schemas.AlgoritmeIn) -> schemas.AlgoritmeDB:
        algoritme = models.Algoritme(**item.dict())
        self.session.add(algoritme)
        self.session.flush()

        return schemas.AlgoritmeDB.from_orm(algoritme)

    def get_all_lars(self) -> list[str]:
        return [lars[0] for lars in self.session.query(models.Algoritme.lars).all()]

    def delete_by_lars(self, lars: str) -> int:
        n_removed = (
            self.session.query(models.Algoritme)
            .filter(models.Algoritme.lars == lars)
            .delete()
        )
        self.session.commit()
        return n_removed
