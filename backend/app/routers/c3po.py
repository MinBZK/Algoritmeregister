from fastapi import APIRouter, Depends
from app.middleware.authorisation.authoriser import AuthType, Authoriser

import app.services.c3po
from app.util.logger import get_logger
from app.schemas.c3po import C3poResults, C3poRequest
from app.config.settings import Settings

logger = get_logger(__name__)
env_settings = Settings()

router = APIRouter()


@router.post(
    "/processing-request",
    response_model=C3poResults,
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
def post_c3po_request(body: C3poRequest):
    return app.services.c3po.fetch_c3po_results(body)
