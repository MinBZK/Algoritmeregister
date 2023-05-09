from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging
from app import schemas, models

logger = logging.getLogger(__name__)


def authorized_user_only(func):
    """Validates that the user has authorization to access the requested resource.

    Returns the same function as the input (including the args and kwargs).

    The decorator makes several assumptions regarding the database structure, and is
    fit-for-purpose. It is not a general tool to check your authorization.

    Only to be used as a @decorator with FastAPI routing."""

    @wraps(func)
    async def wrapper(
        *args,
        db: Session,
        lars: str | None = None,
        as_org: str,
        user: schemas.User,
        **kwargs,
    ):
        # Tests if the user can act on behalf of this organisation
        if as_org not in user.organizations:
            logger.error(
                f"Authorization error, requested org: {as_org}.\nOrganisations under this user: \n{user.organizations}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Er zijn geen accountsrechten gevonden voor een organisatie '{as_org}'.",
            )

        # if no code is given, only authorisation for organisation is needed
        if lars is None:
            return await func(*args, **kwargs, db=db, as_org=as_org, user=user)

        # Tests if the algorithm requested is in the scope of this organisation
        algos_in_scope = (
            db.query(models.algoritme.Algoritme.lars)
            .filter(models.algoritme.Algoritme.owner == as_org)
            .all()
        )
        algos_in_scope_dict = [algo[0] for algo in algos_in_scope]
        if lars not in algos_in_scope_dict:
            logger.error(
                f"""Authorization error, requested LARS-code: {lars}.\nAvailable LARS-codes for this organisation:
                \n{algos_in_scope_dict}"""
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Er is geen algoritme gevonden met LARS-code '{lars}' onder de organisatie '{as_org}'.",
            )

        # After authorization, return decorated function
        return await func(*args, **kwargs, db=db, lars=lars, as_org=as_org, user=user)

    return wrapper


def publisher_only(func):
    @wraps(func)
    async def wrapper(*args, user: schemas.User, **kwargs):
        if (user.role != "publisher") and (user.role != "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform this action.",
            )
        return await func(*args, user=user, **kwargs)

    return wrapper


def admin_only(func):
    @wraps(func)
    async def wrapper(*args, user: schemas.User, **kwargs):
        if user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to perform this action.",
            )
        return await func(*args, user=user, **kwargs)

    return wrapper
