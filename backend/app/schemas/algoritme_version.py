from pydantic import BaseModel
from datetime import datetime
from .misc import (
    Language,
    OrgType,
    ImpacttoetsenGrouping,
    SourceDataGrouping,
    LawfulBasisGrouping,
)


# api
class AlgorithmSummary(BaseModel):
    name: str | None
    schema_version: str | None
    last_update_dt: datetime
    lars: str
    source_id: str | None
    published: bool
    current_version_released: bool
    current_version_published: bool
    last_update_by: str | None

    class Config:
        orm_mode = True


class HighlightedAlgorithmResponse(BaseModel):
    name: str
    lars: str
    organization: str

    class Config:
        orm_mode = True


class NewAlgorithmResponse(BaseModel):
    lars_code: str


class AlgorithmActionResponse(BaseModel):
    message: str | None


class AlgoritmeVersionContent(BaseModel):
    name: str | None
    organization: str | None
    department: str | None
    description_short: str | None
    type: str | None
    category: str | list[str] | None
    website: str | None
    status: str | None
    goal: str | None
    impact: str | None
    proportionality: str | None
    decision_making_process: str | None
    documentation: str | None
    competent_authority: str | None
    lawful_basis: str | None
    iama: str | None
    iama_description: str | None
    dpia: str | None
    dpia_description: str | None
    objection_procedure: str | None
    standard_version: str | None
    uuid: str | None
    url: str | None
    contact_email: str | None
    area: str | None
    lang: str | None
    revision_date: str | None
    description: str | None
    application_url: str | None
    publiccode: str | None
    mprd: str | None
    source_data: str | None
    methods_and_models: str | None
    monitoring: str | None
    human_intervention: str | None
    risks: str | None
    performance_standard: str | None
    provider: str | None
    process_index_url: str | None
    tags: str | None
    source_id: str | None
    begin_date: str | None
    end_date: str | None
    lawful_basis_link: str | None
    impacttoetsen: str | list[str] | None
    source_data_link: str | None
    publication_category: str | None
    lawful_basis_grouping: list[LawfulBasisGrouping] | None
    impacttoetsen_grouping: list[ImpacttoetsenGrouping] | None
    source_data_grouping: list[SourceDataGrouping] | None

    class Config:
        orm_mode = True


class AlgoritmeVersionIn(AlgoritmeVersionContent):
    algoritme_id: int
    language: Language

    published: bool | None
    released: bool | None
    preview_active: bool | None
    create_dt: datetime | None


class AlgoritmeVersionDB(AlgoritmeVersionContent):
    algoritme_id: int
    language: Language
    id: int
    published: bool
    released: bool
    preview_active: bool
    create_dt: datetime

    lars: str
    owner: str

    class Config:
        orm_mode = True


class AlgoritmeVersionTemplate(AlgoritmeVersionContent):
    id: str
    name: str


class AlgoritmeVersionDownload(AlgoritmeVersionContent):
    lars: str


class AlgoritmeVersionDownloadJson(AlgoritmeVersionContent):
    published: bool
    released: bool
    create_dt: datetime
    owner: str


class AlgoritmeVersionQuery(AlgoritmeVersionContent):
    lars: str
    language: Language
    create_dt: datetime


class AlgoritmeVersionGetOne(AlgoritmeVersionContent):
    lars: str
    create_dt: datetime
    released: bool
    published: bool
    language: Language


class AlgoritmeQuery(BaseModel):
    page: int = 1
    limit: int = 10
    searchtext: str = ""
    organisation: str | None = None


class OrganisationPresenceCount(BaseModel):
    name: str
    count: int


class OrganisationFilterGroup(BaseModel):
    type: OrgType
    organisations: list[OrganisationPresenceCount]


class FilterData(BaseModel):
    organisation: list[OrganisationFilterGroup]


class SelectedFilters(BaseModel):
    name: str
    value: str | None


class AlgoritmeQueryResponse(BaseModel):
    results: list[AlgoritmeVersionQuery]
    total_count: int
    filter_data: FilterData
    selected_filters: list[SelectedFilters]


class SearchSuggestionAlgorithms(BaseModel):
    name: str
    organization: str
    lars: str

    class Config:
        orm_mode = True


class SearchSuggestionResponse(BaseModel):
    algorithms: list[SearchSuggestionAlgorithms]
