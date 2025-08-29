import httpx
import urllib.parse
from fastapi import Request, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.datastructures import MutableHeaders
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from app.middleware import get_current_user
from app.config.settings import WebSpellChecker
from app.util.logger import get_logger

logger = get_logger(__name__)
spell_check_api = FastAPI(docs_url=None)
spell_check_api.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@spell_check_api.post("/")
async def forward_spellcheck_request(request: Request):
    """
    This endpoint serves as a forwarding interface to the WebSpellChecker API.
    It receives a POST request from the WebSpellChecker SDK.
    The request body received from this SDK contains the 'customerid' parameter, which represents the user token.
    The token is authenticated and the request is forwarded to the WebSpellChecker API.
    """
    request_body = await request.body()
    token = _parse_token(request_body)
    get_current_user(token)

    async with httpx.AsyncClient() as client:
        webspellchecker_settings = WebSpellChecker()
        request_body = request_body.replace(
            b"customerid=" + token.encode(),
            b"customerid=" + webspellchecker_settings.WEBSPELLCHECKER_API_KEY.encode(),
        )
        mutable_headers = MutableHeaders(request.headers)
        mutable_headers["Content-Length"] = str(len(request_body))
        response = await client.request(
            method="POST",
            url=webspellchecker_settings.WEBSPELLCHECKER_URL,
            headers=mutable_headers,
            content=request_body,
        )
        return response.json()


def _parse_token(request_body):
    parsed_body = urllib.parse.parse_qs(request_body.decode())
    token = parsed_body["customerid"][0]
    return token


limiter = Limiter(key_func=get_remote_address, default_limits=["160/minute"])
spell_check_api.state.limiter = limiter
spell_check_api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
spell_check_api.add_middleware(SlowAPIMiddleware)
