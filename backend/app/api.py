import re
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
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

api.include_router(routers.downloads.router, prefix="/downloads", tags=["Downloads"])
api.include_router(routers.organization.router, tags=["Organisatie"])
api.include_router(routers.algoritme.router, tags=["Algoritme"])
api.include_router(routers.c3po.router, prefix="/c3po", tags=["C3PO"])
api.include_router(routers.templates.router, prefix="/templates", tags=["Templates"])

# Includes fastapi instances in routers folders dynamically.
version_pattern = re.compile(r"v\d_\d_\d[a-z]?")
file_names = [item for item in dir(routers) if version_pattern.match(item)]
for f in file_names:
    file = getattr(routers, f)
    mount_router = getattr(file, "api")
    api.mount(f"/{f}", mount_router)


api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
