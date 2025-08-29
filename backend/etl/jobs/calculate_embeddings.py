from sqlalchemy import text
from app.database.database import SessionLocal
from sqlalchemy.orm import Session
from app.embeddors.bert import Embeddor
from etl.logger import get_logger

logger = get_logger(__name__)

# Embedding column name
COLUMN_NAME = "embedding_nfi"

# Initialize embeddor
embeddor = Embeddor("NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers")


def update_embeddings(db: Session):
    placeholder_vector = "[" + ", ".join(map(str, [0.0] * embeddor.modelsize)) + "]"
    query = text(f"""
        SELECT * FROM algoritme_version 
        WHERE {COLUMN_NAME} = :placeholder
    """)
    rows = db.execute(query, {"placeholder": placeholder_vector}).fetchall()
    for i, row in enumerate(rows):
        if not row.description_short:
            continue
        logger.info(f"embedding {i + 1} / {len(rows)} ")
        txt = row.description_short + " - " + row.name
        vect = embeddor.embed_query(txt)
        query = text(
            f"""UPDATE algoritme_version SET {COLUMN_NAME} = :embedding where id=:row"""
        )
        db.execute(query, {"embedding": vect, "row": row.id})
        
        if (i + 1) % 100 == 0:
            db.commit()
            logger.info(f"Committed batch up to row {i + 1}")
    db.commit()


def main():
    db = SessionLocal()
    update_embeddings(db)
    db.close()


if __name__ == "__main__":
    main()
