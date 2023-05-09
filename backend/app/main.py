from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from app.routers import default, aggregations, text_loader
from app.api import api
from app.etl.load import load_json
from app.util.logger import get_logger
from app.config.settings import Settings, Keycloak

logger = get_logger(__name__)

# Only do automatic data loading on the public website
env_settings = Settings()
logger.info(f"Environment variable TYPE: {env_settings.type}")

if (env_settings.type == "PUB") or (env_settings.type == "DEV"):
    data_loaded = load_json()
    if data_loaded:
        logger.info("Algoritmes loaded")
    else:
        logger.info("Data not loaded")

if (env_settings.type == "PUB") or (env_settings.type == "DEV"):
    fe_api_url = "/api"
else:
    fe_api_url = "/conceptapi"

logger.info(f"API prefix set to {fe_api_url}")


app = FastAPI(
    docs_url=f"{fe_api_url}/api-docs",
    openapi_url=f"{fe_api_url}/openapi.json",
    title="Application API",
    swagger_ui_parameters={"displayRequestDuration": True},
)

router = APIRouter()
app.include_router(default.router, prefix=fe_api_url, tags=["default"])
app.include_router(aggregations.router, prefix=fe_api_url, tags=["aggregations"])
app.include_router(text_loader.router, tags=["text loader"])

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

if (env_settings.type == "API") or (env_settings.type == "DEV"):
    logger.info(f"Mounting {env_settings.type}")
    app.mount("/aanleverapi", api)


if (env_settings.type == "API") or (env_settings.type == "DEV"):

    @app.get("/conceptapi/config")
    def get_config():
        """I cannot get variables in the frontend relating to differentiate between test, acc and prod"""
        settings = Keycloak()
        response = {
            "keycloak_uri": settings.KEYCLOAK_URI,
            "keycloak_realm": settings.KEYCLOAK_REALM,
            "keycloak_client": settings.KEYCLOAK_CLIENT,
        }
        return response
