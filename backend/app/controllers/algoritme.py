from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.repositories.organisation import OrganisationRepository


def get_algoritme_owner(
    db: Session, user: schemas.User, lars: str
) -> schemas.OrganisationIn:
    organisation_repo = OrganisationRepository(db)
    organisation = organisation_repo.get_by_lars(lars)
    if not organisation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    if user.role == "admin" or user.role == "publisher":
        return organisation

    if organisation.code not in user.organizations:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NO_ACCESS")

    return organisation
