from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .misc import Language
from .algoritme_version import AlgoritmeVersionQuery


class OrganisationDetailsUpdatable(BaseModel):
    about: str | None = None
    contact_info: str | None = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class OrganisationDetailsContent(OrganisationDetailsUpdatable):
    name: str


class OrganisationDetailsIn(OrganisationDetailsContent):
    organisation_id: int
    language: Language


class OrganisationDetailsDB(OrganisationDetailsIn):
    id: int
    create_dt: datetime

    show_page: bool
    code: str
    org_id: str
    type: str


class OrganisationDetailsExport(OrganisationDetailsContent):
    language: Language
    code: str
    org_id: str
    type: str
    show_page: bool


class OrganisationDetailsPage(OrganisationDetailsContent):
    show_page: bool
    algoritme_versions: list[AlgoritmeVersionQuery]
