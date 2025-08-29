from fastapi import BackgroundTasks, Depends, APIRouter, Path
from sqlalchemy.orm import Session
from app import schemas, controllers

from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.authorisation.schemas import Role
from app.middleware.middleware import get_db


router = APIRouter()


@router.get(
    "/organisation-details/{organisation_id}",
    response_model=schemas.OrganisationDetailsDB,
    dependencies=[Depends(Authoriser(AuthType.OrgRole, role=Role.OrgDetail))],
)
async def get_org_detail(
    db: Session = Depends(get_db),
    as_org: str = Path(alias="organisation_id"),
):
    return controllers.get_org_detail(db, as_org)


@router.put(
    "/organisation-details/{organisation_id}",
    response_model=schemas.OrganisationDetailsDB,
    dependencies=[Depends(Authoriser(AuthType.OrgRole, role=Role.OrgDetail))],
)
async def put_org_detail(
    background_tasks: BackgroundTasks,
    body: schemas.OrganisationDetailsUpdatable,
    as_org: str = Path(alias="organisation_id"),
    db: Session = Depends(get_db),
):
    return controllers.update_org_details(background_tasks, db, as_org, body)
