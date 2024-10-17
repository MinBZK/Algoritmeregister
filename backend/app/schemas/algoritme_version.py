from pydantic import BaseModel, Field
from datetime import datetime

from app.middleware.authorisation.schemas import State
from .misc import (
    Language,
    ImpacttoetsenGrouping,
    OrgType,
    SortOption,
    SourceDataGrouping,
    LawfulBasisGrouping,
    ImpactAssessments,
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


class AlgorithmVersionHistory(AlgoritmeVersionContent):
    id: int
    lars: str
    published: bool | None
    state: State


class AlgoritmeVersionIn(AlgoritmeVersionContent):
    algoritme_id: int
    language: Language

    preview_active: bool = False
    create_dt: datetime | None
    state: State


class AlgoritmeVersionDB(AlgoritmeVersionContent):
    algoritme_id: int
    language: Language
    id: int
    preview_active: bool = False
    create_dt: datetime
    state: State

    lars: str
    owner: str


class AlgoritmeVersionExport(AlgoritmeVersionContent):
    language: Language
    owner: str
    lars: str
    create_dt: datetime
    state: State


class AlgoritmeVersionTemplate(AlgoritmeVersionContent):
    id: str
    name: str


class AlgoritmeVersionLastEdit(AlgorithmVersionHistory):
    create_dt: datetime
    user_id: str
    archive_dt: datetime


class AlgoritmeVersionDownload(AlgoritmeVersionContent):
    lars: str


class AlgoritmeVersionDownloadJson(AlgoritmeVersionContent):
    state: State
    create_dt: datetime
    owner: str


class AlgoritmeVersionQuery(AlgoritmeVersionContent):
    lars: str
    language: Language
    create_dt: datetime


class AlgoritmeVersionGetOne(AlgoritmeVersionContent):
    lars: str
    create_dt: datetime
    language: Language


class AlgoritmeQuery(BaseModel):
    page: int = Field(ge=1, default=1)
    limit: int = Field(ge=1, default=10, le=100)
    searchtext: str = ""
    organisation: str | None = None
    publicationcategory: str | None = None
    organisationtype: OrgType | None = None
    impact_assessment: ImpactAssessments | None = None
    sort_option: SortOption = Field(default=SortOption.sort_name)


class FilterData(BaseModel):
    label: str
    key: str
    count: int


class PublicationCategoryFilter(BaseModel):
    publication_category_label: str


class PublicationCategoryCount(BaseModel):
    category: str
    count: int


class ImpactAssessmentFilter(BaseModel):
    impact_assessment_label: str


class OrganisationTypeFilter(BaseModel):
    organisation_type: str


class AlgoritmeFilterData(BaseModel):
    organisationtype: list[FilterData] | None = None
    publicationcategory: list[FilterData] | None = None
    impact_assessment: list[FilterData] | None = None
    organisation: list[FilterData] | None = None


class SelectedFilters(BaseModel):
    key: str
    value: str | None


class AlgoritmeQueryResponse(BaseModel):
    results: list[AlgoritmeVersionQuery]
    total_count: int
    filter_data: AlgoritmeFilterData
    selected_filters: list[SelectedFilters]


class SearchSuggestionAlgorithms(BaseModel):
    name: str
    organization: str
    lars: str

    class Config:
        orm_mode = True


class SearchSuggestionResponse(BaseModel):
    algorithms: list[SearchSuggestionAlgorithms]


class ArchiveVersionRequest(BaseModel):
    algorithm_version_id: int


class AlgoritmeVersionEarliestPublish(BaseModel):
    algoritme_id: int
    organization: str
    create_dt: datetime
    code: str

    class Config:
        orm_mode = True


class AlgoritmeVersionEarliestPublishCount(BaseModel):
    date: str
    count: int
