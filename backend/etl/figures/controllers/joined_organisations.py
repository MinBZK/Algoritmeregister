from app import schemas
from app.services.keycloak.repository import KeycloakRepository
from app.middleware import kc_settings


def get_all_organisations_joined_date() -> list[schemas.OrganisationJoinedDate]:
    """
    Returns a list of all organisations and their 'aansluitdatum';
    This is the date that the oldest account associated with them was first created.
    """
    kc_repo = KeycloakRepository(kc_settings)
    all_users = kc_repo.get_all()

    organisation_oldest_date = {}
    for user in all_users:
        groups = user.groups
        created_at = user.created_at
        for group in groups:
            if group not in organisation_oldest_date:
                organisation_oldest_date[group] = created_at
            elif created_at < organisation_oldest_date[group]:
                organisation_oldest_date[group] = created_at

    formatted_organisation_dates = [
        schemas.OrganisationJoinedDate(code=code, create_dt=date)
        for code, date in organisation_oldest_date.items()
    ]

    return formatted_organisation_dates
