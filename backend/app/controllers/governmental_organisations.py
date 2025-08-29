import re
import pandas as pd
from sqlalchemy.orm import Session

from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.repositories.organisation import OrganisationRepository
from app.schemas.misc import OrgType
from app.schemas.organization import OrganisationGovernmental
from app.util.logger import get_logger
from etl.figures.controllers.joined_organisations import (
    get_all_organisations_joined_date,
)

logger = get_logger(__name__)


mapping_provinces: dict[str, str] = {"provincie-fryslân": "provincie-friesland"}
mapping_water_authorities: dict[str, str] = {
    "wetterskip-fryslân": "waterschap-friesland",
    "hoogheemraadschap-van-delfland": "hh-delfland",
    "waterschap-hunze-en-aas": "waterschap-hunze-aas",
}
mapping_environmental_services: dict[str, str] = {
    "omgevingsdienst-midden--en-west-brabant": "omgevingsdienst-west-brabant",
    "dcmr-milieudienst-rijnmond": "DCMR-milieudienst-rijnmond",
    "fryske-utfieringstsjinst-miljeu-en-omjouwing": "omgevingsdienst-friesland",
    "omgevingsdienst-midden-holland": "odmh",
}

mapping_safety_regions: dict[str, str] = {
    "veiligheidsregio-fryslân": "veiligheidsregio-friesland",
    "veiligheidsregio-noord--en-oost-gelderland": "veiligheidsregio-noord-en-oost-gelderland",
    "veiligheids--en-gezondheidsregio-gelderland-midden": "veiligheids-en-gezondheidsregio-gelderland-midden",
    "veiligheidsregio-midden--en-west-brabant": "veiligheidsregio-midden-en-west-brabant",
}


def name_to_code(name: str, org_type: OrgType) -> str:
    without_outer_whitespace = name.strip()
    replace_and_character = without_outer_whitespace.replace("&", "en").lower()
    with_dashes = replace_and_character.replace(" ", "-")
    without_forbidden = re.sub(r"[\(\)'\.,]", "", with_dashes)
    if org_type == OrgType.provincie:
        return mapping_provinces.get(without_forbidden, without_forbidden)
    elif org_type == OrgType.waterschap:
        return mapping_water_authorities.get(without_forbidden, without_forbidden)
    elif org_type == OrgType.omgevingsdienst:
        return mapping_environmental_services.get(without_forbidden, without_forbidden)
    elif org_type == OrgType.veiligheidsregio:
        return mapping_safety_regions.get(without_forbidden, without_forbidden)

    return without_forbidden


def get_governmental_organisations(
    db: Session, org_type: OrgType
) -> list[OrganisationGovernmental]:
    """
    For a given governmental organisation type, builds summaries containing:
    - joined status
    - number of published algorithm descriptions
    - whether a public page should be shown
    """
    csv_files = {
        OrgType.gemeente: "etl/figures/csv/Gemeenten.csv",
        OrgType.waterschap: "etl/figures/csv/Waterschappen.csv",
        OrgType.provincie: "etl/figures/csv/Provincies.csv",
        OrgType.omgevingsdienst: "etl/figures/csv/Omgevingsdiensten.csv",
        OrgType.veiligheidsregio: "etl/figures/csv/Veiligheidsregios.csv",
    }
    csv_file = csv_files[org_type]

    csv_data = pd.read_csv(csv_file, sep=";", encoding="utf-8")
    # To improve the number of loops, we start with a dictionary, and convert to a list later.
    all_gov_organisations: dict[str, OrganisationGovernmental] = {}

    for org in csv_data.itertuples():
        code = name_to_code(org[1], org_type)
        org_id = org[3] if len(org) > 3 else org[2]
        org_gov = OrganisationGovernmental(
            name=org[1],
            identifier=org[2],
            code=code,
            org_id=org_id,
        )
        all_gov_organisations[org_id] = org_gov
    all_gov_org_ids = set(all_gov_organisations.keys())

    # Add joined property.
    joined_organisations = get_all_organisations_joined_date(db)
    for joined_org in joined_organisations:
        if joined_org.org_id in all_gov_org_ids:
            all_gov_organisations[joined_org.org_id].joined = True

    # Add number of published algorithms.
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    all_published = algoritme_version_repo.get_all_published_first_version()
    for published in all_published:
        if published.org_id in all_gov_org_ids:
            all_gov_organisations[published.org_id].number_of_algorithmdescriptions += 1

    # Add show_page property.
    org_repo = OrganisationRepository(db)
    db_gov_organisations = org_repo.get_by_type(
        org_type
        if org_type
        not in [
            OrgType.omgevingsdienst,
            OrgType.veiligheidsregio,
        ]
        else OrgType.regionaal_samenwerkingsorgaan
    )

    if org_type == OrgType.veiligheidsregio:
        db_gov_organisations = [
            gov_organisation
            for gov_organisation in db_gov_organisations
            if gov_organisation.org_id in all_gov_org_ids
        ]

    if org_type == OrgType.omgevingsdienst:
        db_gov_organisations = [
            gov_organisation
            for gov_organisation in db_gov_organisations
            if gov_organisation.org_id in all_gov_org_ids
        ]

    for gov_organisation in db_gov_organisations:
        if (
            org_type == OrgType.gemeente
            and gov_organisation.org_id not in all_gov_org_ids
        ):
            logger.error(
                f"Organisation with org_id {gov_organisation.org_id} not found"
            )
            continue
        all_gov_organisations[
            gov_organisation.org_id
        ].show_page = gov_organisation.show_page

    return [v for _, v in all_gov_organisations.items()]
