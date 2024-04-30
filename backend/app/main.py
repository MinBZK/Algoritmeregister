from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import api
from app.routers.public import aggregations, default, text_loader, downloads
from app.util.logger import get_logger
from app.config.settings import Settings, Keycloak
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

logger = get_logger(__name__)

# Only do automatic data loading on the public website
env_settings = Settings()

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title="Application API",
    swagger_ui_parameters={"displayRequestDuration": True},
)
limiter = Limiter(key_func=get_remote_address, default_limits=["15/minute"])
api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
api.add_middleware(SlowAPIMiddleware)

app.include_router(default.router, prefix="/api", tags=["default"])
app.include_router(aggregations.router, prefix="/api", tags=["Aggregaties"])
app.include_router(text_loader.router, tags=["text_loader"])
app.include_router(downloads.router, prefix="/api/downloads", tags=["Downloads"])

app.mount("/aanleverapi", api)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/api/config")
def get_config():
    """I cannot get variables in the frontend relating to differentiate between test, acc and prod"""
    settings = Keycloak()
    response = {
        "keycloak_uri": settings.KEYCLOAK_URI,
        "keycloak_realm": settings.KEYCLOAK_REALM,
        "keycloak_client": settings.KEYCLOAK_CLIENT,
    }
    return response
