from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import re
from app import routers
from app.util.logger import get_logger

logger = get_logger(__name__)


api = FastAPI(
    docs_url="/api-docs",
    title="Algoritmeregister aanlevering API",
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1,
    },
)

router = APIRouter()

# Includes fastapi instances in routers folders dynamically.
version_pattern = re.compile("v[0-9]_[0-9]_[0-9][a-z]?")
file_names = [item for item in dir(routers) if version_pattern.match(item)]
for f in file_names:
    file = getattr(routers, f)
    mount_router = getattr(file, "api")
    api.mount(f"/{f}", mount_router)


api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
