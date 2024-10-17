from sqlalchemy import text
from app.middleware.middleware import get_db
import app.models as models


def test_get_db():
    """Test if the db is reachable"""
    db = next(get_db())
    assert db
    assert db.execute(text("SELECT 1"))


def test_alembic():
    """Test if the alembic has properly initialized tables"""
    db = next(get_db())
    try:
        db.query(models.Algoritme).all()
    except Exception:
        assert False
