from pydantic import BaseModel, ConfigDict, Field
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
    OperationEnum,
)


# api
class AlgorithmSummary(BaseModel):
    name: str | None = None
    schema_version: str | None = None
    last_update_dt: datetime
    lars: str
    source_id: str | None = None
    published: bool
    current_version_released: bool
    current_version_published: bool
    last_update_by: str | None = None

    model_config = ConfigDict(from_attributes=True)


class HighlightedAlgorithmResponse(BaseModel):
    name: str
    lars: str
    organization: str

    model_config = ConfigDict(from_attributes=True)


class NewAlgorithmResponse(BaseModel):
    lars_code: str


class AlgorithmActionResponse(BaseModel):
    message: str | None = None


class AlgoritmeVersionContent(BaseModel):
    name: str | None = None
    organization: str | None = None
    preferred_name: str | None = None
    department: str | None = None
    description_short: str | None = None
    type: str | None = None
    category: str | list[str] | None = None
    website: str | None = None
    status: str | None = None
    goal: str | None = None
    impact: str | None = None
    proportionality: str | None = None
    decision_making_process: str | None = None
    documentation: str | None = None
    competent_authority: str | None = None
    lawful_basis: str | None = None
    iama: str | None = None
    iama_description: str | None = None
    dpia: str | None = None
    dpia_description: str | None = None
    objection_procedure: str | None = None
    standard_version: str | None = None
    uuid: str | None = None
    url: str | None = None
    contact_email: str | None = None
    area: str | None = None
    lang: str | None = None
    revision_date: str | None = None
    description: str | None = None
    application_url: str | None = None
    publiccode: str | None = None
    mprd: str | None = None
    source_data: str | None = None
    methods_and_models: str | None = None
    monitoring: str | None = None
    human_intervention: str | None = None
    risks: str | None = None
    performance_standard: str | None = None
    provider: str | None = None
    process_index_url: str | None = None
    tags: str | None = None
    source_id: str | None = None
    begin_date: str | None = None
    end_date: str | None = None
    lawful_basis_link: str | None = None
    impacttoetsen: str | list[str] | None = None
    source_data_link: str | None = None
    publication_category: str | None = None
    lawful_basis_grouping: list[LawfulBasisGrouping] | None = None
    impacttoetsen_grouping: list[ImpacttoetsenGrouping] | None = None
    source_data_grouping: list[SourceDataGrouping] | None = None

    model_config = ConfigDict(from_attributes=True)


class AlgorithmVersionHistory(AlgoritmeVersionContent):
    id: int
    lars: str
    published: bool | None = None
    state: State


class AlgoritmeVersionIn(AlgoritmeVersionContent):
    algoritme_id: int
    language: Language

    preview_active: bool = False
    create_dt: datetime | None = None
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
    code: str
    org_id: str
    publication_dt: datetime | None = None


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


class AlgoritmeVersionPublishHistory(AlgorithmVersionHistory):
    publication_dt: datetime
    operation: OperationEnum


class AlgoritmeVersionDownload(AlgoritmeVersionContent):
    lars: str
    publication_dt: datetime | None = None


class AlgoritmeVersionDownloadJson(AlgoritmeVersionContent):
    state: State
    create_dt: datetime
    owner: str


class AlgoritmeVersionQuery(AlgoritmeVersionContent):
    lars: str
    language: Language
    create_dt: datetime
    code: str
    org_id: str


class AlgoritmeVersionGetOne(AlgoritmeVersionContent):
    lars: str
    create_dt: datetime
    language: Language
    code: str
    org_id: str


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
    value: str | None = None


class AlgoritmeQueryResponse(BaseModel):
    results: list[AlgoritmeVersionQuery]
    total_count: int
    filter_data: AlgoritmeFilterData
    selected_filters: list[SelectedFilters]


class AlgoritmeSimilarQueryResponse(AlgoritmeQueryResponse):
    scores: list[float]


class SearchSuggestionAlgorithms(BaseModel):
    name: str
    organization: str
    lars: str

    model_config = ConfigDict(from_attributes=True)


class SearchSuggestionResponse(BaseModel):
    algorithms: list[SearchSuggestionAlgorithms]


class ArchiveVersionRequest(BaseModel):
    algorithm_version_id: int


class AlgoritmeVersionEarliestPublish(BaseModel):
    algoritme_id: int
    organization: str
    create_dt: datetime
    code: str
    org_id: str

    model_config = ConfigDict(from_attributes=True)


class AlgoritmeVersionEarliestPublishCount(BaseModel):
    date: str
    count: int
