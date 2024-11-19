from sqlalchemy.orm import Session
from datetime import datetime, time
import hashlib
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi_cache import FastAPICache
from starlette.middleware.cors import CORSMiddleware
from app.api import api
from fastapi_cache.backends.inmemory import InMemoryBackend

from fastapi_utils.tasks import repeat_every
from app.routers.public import (
    aggregations,
    algorithm,
    default,
    organisation_details,
    text_loader,
    downloads,
    organisation,
    dashboard,
    precomputed_values,
)
from app.spell_checker import spell_check_api
from app.util.logger import get_logger
from app.config.settings import Settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from starlette.types import Message
from starlette.background import BackgroundTask

logger = get_logger(__name__)

# Only do automatic data loading on the public website
env_settings = Settings()

app = FastAPI(
    docs_url="/api-docs",
    openapi_url="/api/openapi.json",
    title="Application API",
    swagger_ui_parameters={"displayRequestDuration": True},
)
limiter = Limiter(key_func=get_remote_address, default_limits=["25/minute"])
api.state.limiter = limiter
api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
api.add_middleware(SlowAPIMiddleware)

app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(algorithm.router, prefix="/api", tags=["Algoritmebeschrijvingen"])
app.include_router(aggregations.router, prefix="/api", tags=["Dashboard"])
app.include_router(organisation.router, prefix="/api", tags=["Organisaties"])
app.include_router(
    organisation_details.router,
    prefix="/api/organisation-details",
    tags=["Organisaties"],
)
app.include_router(downloads.router, prefix="/api", tags=["Downloads"])
app.include_router(default.router, prefix="/api", tags=["Miscellaneous"])
app.include_router(text_loader.router, tags=["text_loader"])
app.include_router(
    precomputed_values.router, prefix="/api", tags=["Algoritmebeschrijvingen"]
)

app.mount("/aanleverapi", api)
app.mount("/spellcheck", spell_check_api)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    def key_builder(
        func: Callable,
        namespace: str | None = "",
        request: Request | None = None,
        response: Response | None = None,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ):
        """
        Builds a key for the caching based off of the function parameters.
        Same as default_key_builder, but it removes a kwarg with type == Session,
        to avoid detecting a false difference between calls. Session is a unique
        object every call.
        """
        if not kwargs:
            filtered_kwargs = None
        else:
            filtered_kwargs = {
                k: v for k, v in kwargs.items() if not isinstance(v, Session)
            }
        prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
        cache_key = (
            prefix
            + hashlib.md5(  # nosec:B303
                f"{func.__module__}:{func.__name__}:{args}:{filtered_kwargs}".encode()
            ).hexdigest()
        )
        return cache_key

    FastAPICache.init(InMemoryBackend(), key_builder=key_builder)


@app.on_event("startup")
@repeat_every(seconds=60)  # 1 minute
async def cache_clearing():
    """
    Clears the cache if it is just past midnight
    """
    current_time = datetime.now().time()
    start_time = time(0, 0)
    end_time = time(0, 1)
    if start_time <= current_time <= end_time:
        logger.info("Clearing cache")
        await FastAPICache.clear(namespace="dashboard")


def log_info(req_body, req_meth, req_url, res_status):
    if req_body:
        logger.info(
            f"Req Method: {req_meth}, Req URL: {req_url}, Res Status: {res_status}, Req Body: {req_body}"
        )
    else:
        logger.info(
            f"Req Method: {req_meth}, Req URL: {req_url}, Res Status: {res_status}"
        )


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


if env_settings.debugger_logging:

    @app.middleware("http")
    async def request_response_logging_middleware(request: Request, call_next):

        req_body = await request.body()
        await set_body(request, req_body)
        response = await call_next(request)

        res_body = b""
        async for chunk in response.body_iterator:
            res_body += chunk

        task = BackgroundTask(
            log_info, req_body, request.method, request.url, response.status_code
        )
        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task,
        )
