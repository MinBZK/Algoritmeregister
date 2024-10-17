from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.middleware.authorisation.schemas import Role, State
from app.repositories.organisation import OrganisationRepository
from app.repositories import AlgoritmeVersionRepository
from app.schemas.misc import Language
from app.services.keycloak import KeycloakUser


def get_algoritme_owner(
    db: Session, user: KeycloakUser, lars: str
) -> schemas.OrganisationIn:
    organisation_repo = OrganisationRepository(db)
    organisation = organisation_repo.get_by_lars(lars)
    if not organisation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    if Role.Administrator in user.roles or Role.AllGroups in user.roles:
        return organisation

    if organisation.code not in user.groups:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="NO_ACCESS")

    return organisation


def get_algoritme_versions_by_id(
    db: Session, lars: str, include_archived: bool = False
) -> list[schemas.AlgoritmeVersionLastEdit]:
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    versions = algoritme_version_repo.get_all_versions_by_lars_by_lang(
        lars, Language.NLD
    )
    if not include_archived:
        versions = [
            version for version in versions if not version.state == State.ARCHIVED
        ]
    return versions


def get_archived_versions(
    db: Session, org: str
) -> list[schemas.AlgoritmeVersionLastEdit]:
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    all_versions = algoritme_version_repo.get_archive(org, Language.NLD)
    schema_versions = [
        schemas.AlgoritmeVersionLastEdit.from_orm(version) for version in all_versions
    ]
    return schema_versions
