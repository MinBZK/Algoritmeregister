from fastapi import APIRouter, Path
from fastapi import Depends
from app import schemas
from app import repositories
from app.middleware.middleware import get_db
from sqlalchemy.orm import Session
from app.config.settings import Settings
from app.repositories.organisation import OrganisationRepository
from app.repositories.algoritme_version import AlgoritmeVersionRepository
from app.controllers.organisation.public import get_all_organisations_joined_date
from app.util.create_dict import create_dict
from app.schemas.misc import Language, OrgType
from app.schemas.organization import OrganisationGovernmental
from app.util.logger import get_logger
from fastapi_cache.decorator import cache
from app.controllers.html_figures import get_html_figures_recent
from app.controllers.governmental_organisations import get_governmental_organisations


router = APIRouter()
logger = get_logger(__name__)
env_settings = Settings()


@router.get("/organisation/top-20/{lang}")
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_top_20_orgs(
    db: Session = Depends(get_db),
    lang: Language = Path(),
):
    org = OrganisationRepository(db)
    return org.get_top_20(lang)


@router.get(
    "/organisation/joined-permonth",
    response_model=list[schemas.OrganisationJoinedCount],
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_joined_organisations_permonth(db: Session = Depends(get_db)):
    orgs = get_all_organisations_joined_date(db)
    return create_dict(orgs)


@router.get(
    "/algorithm/published-permonth",
    response_model=list[schemas.AlgoritmeVersionEarliestPublishCount],
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_published_algorithmdescriptions_permonth(db: Session = Depends(get_db)):
    algo_repo = AlgoritmeVersionRepository(db)
    algorithms = algo_repo.get_all_published_first_version()
    return create_dict(algorithms)


@router.get(
    "/algorithm/publication-categories/{lang}",
    response_model=list[schemas.PublicationCategoryCount],
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_publication_categories(
    db: Session = Depends(get_db),
    lang: Language = Path(),
):
    algo_version_repo = AlgoritmeVersionRepository(db)
    return algo_version_repo.get_all_published_by_pubcat(lang)


@router.get(
    "/dashboard/figures",
    response_model=schemas.HtmlFiguresOut,
)
async def html_figures(db: Session = Depends(get_db)):
    return get_html_figures_recent(db)


@router.get(
    "/organisation/municipalities", response_model=list[OrganisationGovernmental]
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_all_municipalities(db: Session = Depends(get_db)):
    return get_governmental_organisations(db, OrgType.gemeente)


@router.get("/organisation/provinces", response_model=list[OrganisationGovernmental])
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_all_provinces(db: Session = Depends(get_db)):
    return get_governmental_organisations(db, OrgType.provincie)


@router.get(
    "/organisation/water-authorities", response_model=list[OrganisationGovernmental]
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_all_water_authorities(db: Session = Depends(get_db)):
    return get_governmental_organisations(db, OrgType.waterschap)


@router.get(
    "/organisation/safety-regions", response_model=list[OrganisationGovernmental]
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_all_safety_regions(db: Session = Depends(get_db)):
    return get_governmental_organisations(db, OrgType.veiligheidsregio)


@router.get(
    "/organisation/environmental-services",
    response_model=list[OrganisationGovernmental],
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_all_environmental_services(db: Session = Depends(get_db)):
    return get_governmental_organisations(db, OrgType.omgevingsdienst)


@router.get(
    "/algorithm/national-organisations/{lang}",
    response_model=list[schemas.NationalOrganisationsCountDashboard],
)
@cache(namespace="dashboard", expire=60 * 60)  # 1 hour
async def get_national_organisations(
    db: Session = Depends(get_db),
    lang: Language = Path(),
):
    org_repo = repositories.OrganisationRepository(db)
    return org_repo.get_overview_published_nat_org_public(lang)
