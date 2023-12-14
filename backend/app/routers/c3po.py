from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.middleware.middleware import get_db
from app.util.logger import get_logger
from app import schemas, controllers
from app.middleware.keycloak_authenticator import get_current_user
from app.config.settings import Settings
from app.middleware.decorators import publisher_only

logger = get_logger(__name__)
env_settings = Settings()

router = APIRouter()


@router.post("/processing-request", response_model=schemas.C3poResults)
@publisher_only
async def post_c3po_request(
    body: schemas.C3poRequest,
    user: schemas.User = Depends(get_current_user),
):
    return await controllers.forward_request(body, user)


@router.get("/rule", response_model=list[schemas.RuleSetOut])
@publisher_only
async def get_version_rules(
    user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return controllers.get_version_rules()
