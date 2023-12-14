from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.repositories.organisation import OrganisationRepository


def get_orgs(db: Session, user: schemas.User) -> list[schemas.OrganisationIn]:
    if user.role == "publisher" or user.role == "admin":
        all_orgs = (
            db.query(models.Organisation).order_by(models.Organisation.name).all()
        )
        return [schemas.OrganisationIn.from_orm(org) for org in all_orgs]
    else:
        org_list = user.organizations
        some_orgs = (
            db.query(models.Organisation)
            .order_by(models.Organisation.name)
            .filter(models.Organisation.code.in_(org_list))
            .all()
        )
        if not some_orgs:
            return []
        return [schemas.OrganisationIn.from_orm(org) for org in some_orgs]


def is_unique_code(db: Session, organisation: schemas.OrganisationIn) -> bool:
    """Test for presence of the organisation code in the DB. If found, throws an HTTPExcetion"""
    organisation_repo = OrganisationRepository(db)
    duplicate_code = organisation_repo.get_by_code(organisation.code)
    if duplicate_code is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CODE_TAKEN")
    return True


def is_unique_name(db: Session, organisation: schemas.OrganisationIn) -> bool:
    """Test for presence of the organisation name in the DB. If found, throws an HTTPExcetion"""
    organisation_repo = OrganisationRepository(db)
    duplicate_name = organisation_repo.get_by_name(organisation.name)
    if duplicate_name is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NAME_TAKEN")
    return True


def create_org(db: Session, organisation: schemas.OrganisationIn):
    is_unique_name(db, organisation)
    is_unique_code(db, organisation)

    org_model = models.Organisation(**organisation.dict())
    db.add(org_model)
    db.commit()


def update_org(db: Session, org_code: str, organisation: schemas.OrganisationIn):
    if org_code != organisation.code:
        # On code change, test for uniqueness.
        is_unique_code(db, organisation)

    current_org_query = db.query(models.Organisation).filter(
        models.Organisation.code == org_code
    )
    current_org: models.Organisation | None = current_org_query.first()
    if not current_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ORG_NOT_FOUND"
        )

    if current_org.name != organisation.name:
        # On name change, test for uniqueness.
        is_unique_name(db, organisation)

    current_org_query.update(
        {
            models.Organisation.code: organisation.code,
            models.Organisation.name: organisation.name,
            models.Organisation.type: organisation.type,
        },
        synchronize_session=False,
    )
    db.commit()
