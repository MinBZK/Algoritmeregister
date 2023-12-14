from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session
from app import schemas, middleware
from app.controllers import get_orgs, create_org, update_org
from app.middleware.decorators import admin_only, publisher_only

router = APIRouter()


@router.get("/organization", response_model=list[schemas.OrganisationIn])
async def get_all_orgs(
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(middleware.get_current_user),
):
    return get_orgs(db, user=user)


@router.post("/organization", response_model=None)
@admin_only
async def post_org(
    body: schemas.OrganisationIn,
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(middleware.get_current_user),
):
    create_org(db, body)


@router.put("/organization/{org_id}", response_model=None)
@publisher_only
async def put_org(
    body: schemas.OrganisationIn,
    as_org: str = Path(alias="org_id"),
    db: Session = Depends(middleware.get_db),
    user: schemas.User = Depends(middleware.get_current_user),
):
    update_org(db, as_org, body)
