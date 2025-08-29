from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import schemas
from app.middleware.authorisation.schemas import Role, State
from app.repositories.organisation import OrganisationRepository
from app.repositories import AlgoritmeVersionRepository
from app.schemas.misc import Language
from app.services.keycloak import KeycloakUser
from app.embeddors.bert import Embeddor
import time
from app.util.logger import get_logger

logger = get_logger(__name__)

EMBEDDOR = Embeddor(
    "NetherlandsForensicInstitute/robbert-2022-dutch-sentence-transformers"
)


def get_algoritme_owner(
    db: Session, user: KeycloakUser, lars: str
) -> schemas.OrganisationIn:
    organisation_repo = OrganisationRepository(db)
    organisation = organisation_repo.get_by_lars(lars)
    if not organisation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")

    if Role.Administrator in user.roles or Role.AllGroups in user.roles:
        return organisation

    if organisation.org_id not in user.groups:
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
        schemas.AlgoritmeVersionLastEdit.model_validate(version)
        for version in all_versions
    ]
    return schema_versions


def embed_version(
    db: Session,
    lars: str,
) -> None:
    t0 = time.perf_counter()
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    algoritme_version = algoritme_version_repo.get_latest_by_lars_by_lang(
        lars, Language.NLD
    )
    if algoritme_version is None:
        raise ValueError(f"No algoritme version found for lars: {lars}")

    if not algoritme_version.name or not algoritme_version.description_short:
        raise ValueError("Algoritme version is missing required fields")

    vector = EMBEDDOR.embed_query(
        algoritme_version.name + " - " + algoritme_version.description_short
    )
    algoritme_version.embedding_nfi = vector
    db.add(algoritme_version)
    db.commit()
    logger.info(f"time to embed algoritme {time.perf_counter() - t0}")
