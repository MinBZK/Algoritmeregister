from app.database.database import SessionLocal
from app.controllers.algoritme_version.endpoints import set_highlighted_algorithms
from app.repositories.precomputed_values import PreComputedValuesRepository
from app.schemas import PreComputedValues

def main():
    db = SessionLocal()
    pre_comp_value_repo = PreComputedValuesRepository(db)
    pre_comp_value_repo.delete_by_key(PreComputedValues.highlighted_algorithms)
    set_highlighted_algorithms(db)
    db.close()

if __name__ == "__main__":
    main()