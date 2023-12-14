from sqlalchemy import create_engine
from common.database_url import get_database_url

SQLALCHEMY_DATABASE_URL = get_database_url()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    max_overflow=40,
    pool_timeout=10,
)
