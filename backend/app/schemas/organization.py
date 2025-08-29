from pydantic import BaseModel, ConfigDict, Field
from app import schemas
from app.middleware.authorisation.config._base import Flow
from app.schemas.algoritme_version import FilterData
from .misc import OrgType
from datetime import datetime


class OrganisationConfigIn(BaseModel):
    name: str
    code: str
    org_id: str
    type: OrgType
    flow: Flow


class OrganisationConfig(OrganisationConfigIn):
    show_page: bool
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrganisationIn(BaseModel):
    code: str
    org_id: str
    type: OrgType
    show_page: bool
    flow: Flow
    official_name: str | None = None
    alternative_name: str | None = None
    abbreviation: str | None = None
    label: str | None = None
    official_name_with_type: str | None = None
    official_name_without_type: str | None = None
    official_name_for_sorting: str | None = None
    preferred_name_without_type: str | None = None
    preferred_name_including_type: str | None = None
    preferred_name_for_sorting: str | None = None
    tooi_alternative_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OrganisationDB(OrganisationIn):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrganisationGrouping(BaseModel):
    type: OrgType
    name: str
    code: str
    org_id: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class OrganisationOverview(BaseModel):
    code: str
    count: int
    name: str
    show_page: bool
    type: OrgType
    org_id: str

    model_config = ConfigDict(from_attributes=True)


class OrganisationTypeFilter(BaseModel):
    key: str
    type_label: str


class OrganisationFilterData(BaseModel):
    organisationtype: list[FilterData]


class OrganisationQueryResponse(BaseModel):
    results: list[OrganisationOverview]
    total_count: int
    filter_data: OrganisationFilterData
    selected_filters: list[schemas.SelectedFilters]


class OrganisationQuery(BaseModel):
    page: int = Field(ge=1, default=1)
    limit: int = Field(ge=1, default=10, le=100)
    searchtext: str | None = None
    organisationtype: OrgType | None = Field(
        default=None, description="Example: OrgType.gemeente"
    )


class OrganisationMappingResult(BaseModel):
    name: str
    code: str
    org_id: str | None = None
    show_page: bool | None = None
    count: int | None = None

    model_config = ConfigDict(from_attributes=True)


class OrganisationSearchSuggestionResponse(BaseModel):
    organisations: list[OrganisationMappingResult]


class GetOrganisationsResponse(BaseModel):
    organisations: list[OrganisationConfig]
    count: int


class OrganisationTop20(BaseModel):
    name: str
    count: int


class OrganisationCodeResponse(BaseModel):
    code: str
    org_id: str


class OrganisationRelationHierarchy(BaseModel):
    org_id: str
    name: str | None = None


class OrganisationRelationResponse(BaseModel):
    org_id: str
    hierarchy_path: str
    hierarchy: list[OrganisationRelationHierarchy]


class OrganisationJoinedDate(BaseModel):
    org_id: str
    create_dt: datetime

    model_config = ConfigDict(from_attributes=True)


class OrganisationGovernmental(BaseModel):
    name: str
    identifier: str
    number_of_algorithmdescriptions: int = 0
    show_page: bool = False
    joined: bool = False
    code: str
    org_id: str


class OrganisationJoinedCount(BaseModel):
    date: str
    count: int


class NationalOrganisationsCount(BaseModel):
    name: str
    Total: int
    KD: int
    UTO: int
    BOO: int
    Overig: int


class NationalOrganisationsCountDashboard(BaseModel):
    name: str
    Total: int
    KD: int
    Agentschap: int
    Overig: int
