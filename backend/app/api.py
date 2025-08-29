import re
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

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
api.include_router(routers.organisation_details.router, tags=["Organisatiedetails"])
api.include_router(routers.organisation.router, tags=["Organisatie"])
api.include_router(routers.algoritme.router, tags=["Algoritme"])
api.include_router(routers.c3po.router, prefix="/c3po", tags=["C3PO"])
api.include_router(routers.templates.router, prefix="/templates", tags=["Templates"])
api.include_router(routers.user.router, tags=["User"])
api.include_router(routers.broken_links.router, tags=["Dashboard"])
api.include_router(routers.national_organisations.router, tags=["Dashboard"])
api.include_router(routers.aggregations.router, tags=["Aggregations"])

# Includes fastapi instances in routers folders dynamically.
version_pattern = re.compile(r"v\d_\d[a-z]?")
file_names = [item for item in dir(routers) if version_pattern.match(item)]
for f in file_names:
    file = getattr(routers, f)
    mount_router = getattr(file, "api")
    api.mount(f"/{f}", mount_router)


@api.middleware("http")
async def redirect_legacy_aanleverapi(request, call_next):
    """
    Dynamically redirect valid API calls with an extra zero to the corresponding new version.
    """
    version_mapping = {f"{version}_0": version for version in file_names}
    request_url = request.url.path
    if not request_url.startswith("/aanleverapi"):
        response = await call_next(request)
        return response

    request_api_version = request_url.split("/")[2]
    if request_api_version not in version_mapping.keys():
        response = await call_next(request)
        return response

    new_url = request_url.replace(
        request_api_version, version_mapping[request_api_version]
    )
    response = RedirectResponse(url=new_url)
    return response


api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
