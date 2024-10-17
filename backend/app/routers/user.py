from typing import Annotated
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from app.middleware.authorisation.authoriser import AuthType, Authoriser
from app.middleware.authorisation.schemas import Role
from app.middleware.keycloak_authenticator import get_current_user
from app.middleware.middleware import get_db
from app.schemas.user import User
from app.services.keycloak.schemas import (
    KeycloakUser,
    KeycloakUserNew,
    KeycloakUserUpdate,
)
from app.schemas import GetUsersResponse
from app.controllers import user as user_controller

router = APIRouter()


@router.get(
    "/user",
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.ICTU))],
)
async def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    limit: int = Query(ge=1, le=50, default=10),
    skip: int = Query(ge=0, default=0),
    q: str | None = Query(max_length=50, default=None),
    role: str | None = None,
    org: str | None = None,
) -> GetUsersResponse:
    return user_controller.get_all_users(db, limit, skip, q, role, org)


@router.post(
    "/user",
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.ICTU))],
)
async def create_user(
    db: Annotated[Session, Depends(get_db)],
    body: KeycloakUserNew,
) -> User:
    return user_controller.create_user(db, body)


@router.get(
    "/user/me",
    dependencies=[Depends(Authoriser(AuthType.BaseOnly))],
)
async def get_me(
    db: Session = Depends(get_db),
    user: KeycloakUser = Depends(get_current_user),
) -> User:
    return user_controller.get_user(db, user.id)


@router.get(
    "/user/{user_id}",
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.ICTU))],
)
async def get_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: str,
) -> User:
    return user_controller.get_user(db, user_id)


@router.put(
    "/user/{user_id}",
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator))],
)
async def update_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: str,
    body: KeycloakUserUpdate,
) -> User:
    return user_controller.update_user(db, user_id, body)


@router.delete(
    "/user/{user_id}",
    dependencies=[Depends(Authoriser(AuthType.RoleOnly, role=Role.Administrator))],
)
async def delete_user(
    user_id: str,
) -> None:
    return user_controller.delete_user(user_id)
