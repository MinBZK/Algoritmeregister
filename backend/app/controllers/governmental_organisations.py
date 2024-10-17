import re
from typing import Literal
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

GROUPING_TO_INDIVIDUAL_MUNICPALITIES: dict[str, list[str]] = {
    "gemeente-nuenen": [],
    "gemeente-gerwen": [],
    "gemeente-nederwetten": [],
    "gemeente-nuenen-gerwen-en-nederwetten": ["gemeente-nuenen-ca"],
    "servicecentrum-mer": [
        "gemeente-maasgouw",
        "gemeente-echt-susteren",
        "gemeente-roerdalen",
    ],
    "samenwerking-a2-gemeenten": [
        "gemeente-heeze-leende",
        "gemeente-cranendonck",
        "gemeente-valkenswaard",
    ],
}

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

KEYWORDS_ENVIRONMENTAL_SERVICES: list[str] = ["dcmr", "omgevingsdienst", "rud", "odmh"]
KEYWORDS_WATER_AUTHORITIES: list[str] = ["waterschap", "hoogheemraadschap", "hh-"]


def name_to_code(name: str, org_type: OrgType) -> str:
    without_outer_whitespace = name.strip()
    replace_and_character = without_outer_whitespace.replace("&", "en").lower()
    with_dashes = replace_and_character.replace(" ", "-")
    without_forbidden = re.sub(r"[\(\)'\.]", "", with_dashes)
    if org_type == OrgType.provincie:
        return mapping_provinces.get(without_forbidden, without_forbidden)
    elif org_type == OrgType.waterschap:
        return mapping_water_authorities.get(without_forbidden, without_forbidden)
    elif org_type == OrgType.omgevingsdienst:
        return mapping_environmental_services.get(without_forbidden, without_forbidden)

    return without_forbidden


def handle_code_not_found(
    code: str,
    all_municipalities: dict[str, OrganisationGovernmental],
    attribute: Literal["joined", "show_page", "number_of_algorithmdescriptions"],
    *,
    show_page: bool | None = None,
) -> None:
    """
    If the code from the DB can't be found in the list of gemeentes, not all is lost.
    There are some situations where municipalities work together. Their joined name is handled here.
    """
    found_aliases = GROUPING_TO_INDIVIDUAL_MUNICPALITIES.get(code, None)
    if found_aliases is None:
        logger.error(f"{code} NOT FOUND, municipality data incomplete. ({attribute})")
        return
    elif found_aliases == []:
        # Special case: ignore this municipality
        return

    for alias in found_aliases:
        match attribute:
            case "joined":
                all_municipalities[alias].joined = True
            case "show_page":
                if show_page is None:
                    raise ValueError(
                        "When changing show_page, you must supply the show_page kwarg."
                    )
                all_municipalities[alias].show_page = show_page
            case "number_of_algorithmdescriptions":
                all_municipalities[alias].number_of_algorithmdescriptions += 1


def get_governmental_organisations(
    db: Session, org_type: OrgType
) -> list[OrganisationGovernmental]:
    """
    For all governmental organisations, builds summaries.
    """
    if org_type == OrgType.gemeente:
        csv_file = "etl/figures/csv/Gemeenten.csv"
    elif org_type == OrgType.waterschap:
        csv_file = "etl/figures/csv/Waterschappen.csv"
    elif org_type == OrgType.provincie:
        csv_file = "etl/figures/csv/Provincies.csv"
    elif org_type == OrgType.omgevingsdienst:
        csv_file = "etl/figures/csv/Omgevingsdiensten.csv"

    csv_data = pd.read_csv(csv_file, sep=";", encoding="utf-8")
    # To improve the number of loops, we start with a dictionary, and convert to a list later.
    all_gov_organisations: dict[str, OrganisationGovernmental] = {}
    for org in csv_data.itertuples():
        code = name_to_code(org[1], org_type)
        org_gov = OrganisationGovernmental(name=org[1], identifier=org[2], code=code)
        all_gov_organisations[code] = org_gov
    all_codes = all_gov_organisations.keys()

    # Add joined property.
    joined_organisations = get_all_organisations_joined_date()
    joined_gov_organisations = [
        o
        for o in joined_organisations
        if (org_type in o.code)
        or (
            org_type == OrgType.waterschap
            and any(keyword in o.code.lower() for keyword in KEYWORDS_WATER_AUTHORITIES)
        )
        or (
            org_type == OrgType.omgevingsdienst
            and any(
                keyword in o.code.lower() for keyword in KEYWORDS_ENVIRONMENTAL_SERVICES
            )
        )
    ]
    for org in joined_gov_organisations:
        if org_type == OrgType.gemeente and org.code not in all_codes:
            handle_code_not_found(org.code, all_gov_organisations, "joined")
            continue
        all_gov_organisations[org.code].joined = True

    # Add number of published algorithms.
    algoritme_version_repo = AlgoritmeVersionRepository(db)
    all_published = algoritme_version_repo.get_all_published_first_version()
    gov_organisation_published = [
        a
        for a in all_published
        if (org_type in a.code)
        or (
            org_type == OrgType.waterschap
            and any(keyword in a.code.lower() for keyword in KEYWORDS_WATER_AUTHORITIES)
        )
        or (
            org_type == OrgType.omgevingsdienst
            and any(
                keyword in a.code.lower() for keyword in KEYWORDS_ENVIRONMENTAL_SERVICES
            )
        )
    ]
    for published in gov_organisation_published:
        if org_type == OrgType.gemeente and published.code not in all_codes:
            handle_code_not_found(
                published.code, all_gov_organisations, "number_of_algorithmdescriptions"
            )
            continue
        all_gov_organisations[published.code].number_of_algorithmdescriptions += 1

    # Add show_page property.
    org_repo = OrganisationRepository(db)
    db_gov_organisations = org_repo.get_by_type(
        org_type
        if org_type != OrgType.omgevingsdienst
        else OrgType.regionaal_samenwerkingsorgaan
    )
    if org_type == OrgType.omgevingsdienst:
        db_gov_organisations = [
            gov_organisation
            for gov_organisation in db_gov_organisations
            if any(
                gov_organisation.code.split("-")[0].lower() in keyword
                for keyword in KEYWORDS_ENVIRONMENTAL_SERVICES
            )
        ]

    for gov_organisation in db_gov_organisations:
        if org_type == OrgType.gemeente and gov_organisation.code not in all_codes:
            handle_code_not_found(
                gov_organisation.code,
                all_gov_organisations,
                "show_page",
                show_page=gov_organisation.show_page,
            )
            continue
        all_gov_organisations[
            gov_organisation.code
        ].show_page = gov_organisation.show_page

    return [v for _, v in all_gov_organisations.items()]
