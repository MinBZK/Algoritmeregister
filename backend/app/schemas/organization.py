from pydantic import BaseModel, Field
from app import schemas
from app.middleware.authorisation.config._base import Flow
from app.schemas.algoritme_version import FilterData
from .misc import OrgType
from datetime import datetime


class OrganisationConfigIn(BaseModel):
    name: str
    code: str
    type: OrgType
    flow: Flow


class OrganisationConfig(OrganisationConfigIn):
    show_page: bool
    id: int

    class Config:
        orm_mode = True


class OrganisationIn(BaseModel):
    code: str
    type: OrgType
    show_page: bool
    flow: Flow

    class Config:
        orm_mode = True


class OrganisationDB(OrganisationIn):
    id: int

    class Config:
        orm_mode = True


class OrganisationGrouping(BaseModel):
    type: OrgType
    name: str
    code: str
    count: int

    class Config:
        orm_mode = True


class OrganisationOverview(BaseModel):
    code: str
    count: int
    name: str
    show_page: bool
    type: OrgType

    class Config:
        orm_mode = True


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
    organisationtype: OrgType | None = Field(example=OrgType.gemeente)


class OrganisationMappingResult(BaseModel):
    name: str
    code: str

    class Config:
        orm_mode = True


class OrganisationSearchSuggestionResponse(BaseModel):
    organisations: list[OrganisationMappingResult]


class GetOrganisationsResponse(BaseModel):
    organisations: list[OrganisationConfig]
    count: int


class OrganisationTop20(BaseModel):
    name: str
    count: int


class OrganisationJoinedDate(BaseModel):
    code: str
    create_dt: datetime

    class Config:
        orm_mode = True


class OrganisationGovernmental(BaseModel):
    name: str
    identifier: str
    number_of_algorithmdescriptions: int = 0
    show_page: bool = False
    joined: bool = False
    code: str


class OrganisationJoinedCount(BaseModel):
    date: str
    count: int
