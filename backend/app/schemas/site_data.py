from pydantic import BaseModel
from .algoritme_version import AlgoritmeVersionExport
from .organisation_details import OrganisationDetailsExport


class SiteData(BaseModel):
    algoritme_versions: list[AlgoritmeVersionExport]
    organisation_details: list[OrganisationDetailsExport]
