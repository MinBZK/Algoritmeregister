from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()


def get_database_url() -> str:
    USERNAME = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD = urllib.parse.quote(os.getenv("POSTGRES_PASSWORD", "postgres"))
    HOST = os.getenv("POSTGRES_SERVER", "localhost")
    SCHEMA = os.getenv("POSTGRES_DB", "algreg_db")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    connection_string = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{SCHEMA}"
    return connection_string
