from sqlalchemy.orm import Session
from app import schemas
from app.models.precomputed_values import PrecomputedValues
from app.schemas.misc import Language
from .index import IRepository
from fastapi import HTTPException


class PreComputedValuesRepository(IRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, item: schemas.PrecomputedValueIn) -> schemas.PrecomputedValue:
        precomputed_values = PrecomputedValues(**item.dict())
        self.session.add(precomputed_values)
        self.session.commit()
        return schemas.PrecomputedValue.from_orm(precomputed_values)

    def get_all(self) -> list[schemas.PrecomputedValue]:
        actions = self.session.query(PrecomputedValues).all()
        return [schemas.PrecomputedValue.from_orm(a) for a in actions]

    def delete_by_key(self, key: str):
        self.session.query(PrecomputedValues).filter(
            PrecomputedValues.key == key
        ).delete()
        self.session.commit()

    def get_highlighted_values(
        self, lang: Language
    ) -> list[schemas.HighlightedAlgorithmResponse]:
        precomputed_values = (
            self.session.query(PrecomputedValues)
            .filter(PrecomputedValues.language == lang)
            .order_by(PrecomputedValues.create_dt.desc())
        ).first()

        if precomputed_values:
            return [
                schemas.HighlightedAlgorithmResponse(**item)
                for item in precomputed_values.value
            ]
        else:
            raise HTTPException(
                status_code=404, detail="Geen precomputed values gevonden."
            )
