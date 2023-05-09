from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from common.database_url import get_database_url
from app.config.settings import Settings

SQLALCHEMY_DATABASE_URL = get_database_url()


env_settings = Settings()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=env_settings.enable_debug,
    max_overflow=40,
    pool_timeout=10,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
