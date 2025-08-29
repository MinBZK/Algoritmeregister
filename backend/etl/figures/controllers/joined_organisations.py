from app import schemas
from app.services.keycloak.repository import KeycloakRepository
from app.middleware import kc_settings
from app.repositories.organisation import OrganisationRepository
from sqlalchemy.orm import Session


def get_all_organisations_joined_date(
    db: Session,
) -> list[schemas.OrganisationJoinedDate]:
    """
    Returns a list of all organisations and their 'aansluitdatum';
    This is the date that the oldest account associated with them was first created.
    """
    kc_repo = KeycloakRepository(kc_settings)
    org_repo = OrganisationRepository(db)
    all_users = kc_repo.get_all()
    org_code_to_org_id = org_repo.get_org_code_to_org_id_mapping()

    organisation_oldest_date = {}
    for user in all_users:
        groups = user.groups
        created_at = user.created_at
        normalized_org_ids = set()
        for group in groups:
            org_id = org_code_to_org_id.get(group, group)
            normalized_org_ids.add(org_id)

        for org_id in normalized_org_ids:
            if org_id not in organisation_oldest_date:
                organisation_oldest_date[org_id] = created_at
            elif created_at < organisation_oldest_date[org_id]:
                organisation_oldest_date[org_id] = created_at
    formatted_organisation_dates = [
        schemas.OrganisationJoinedDate(org_id=org_id, create_dt=date)
        for org_id, date in organisation_oldest_date.items()
    ]
    return formatted_organisation_dates
