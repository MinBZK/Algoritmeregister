from pydantic import BaseModel


class BaseModelOrmMode(BaseModel):
    class Config:
        orm_mode = True


class Inzet(BaseModelOrmMode):
    id: str
    goal: str
    impact: str
    proportionality: str
    decision_making_process: str
    documentation: str | None
    algoritme_id: str | None


class Juridisch(BaseModelOrmMode):
    id: str
    competent_authority: str | None
    lawful_basis: str
    dpia: bool | None
    dpia_description: str | None
    objection_procedure: str
    algoritme_id: str | None


class Metadata(BaseModelOrmMode):
    id: str
    # schema is an attribute of BaseModel, so name cannot be identical to database
    schema_metadata: str | None
    uuid: str | None
    url: str | None
    contact_email: str
    area: str | None
    lang: str | None
    revision_date: str | None
    algoritme_id: str | None


class Toepassing(BaseModelOrmMode):
    id: str
    description: str | None
    application_url: str | None
    publiccode: str | None
    mprd: bool | None
    source_data: str | None
    methods_and_models: str | None
    algoritme_id: str | None


class Toezicht(BaseModelOrmMode):
    id: str
    monitoring: str | None
    human_intervention: str
    risks: str | None
    performance_standard: str | None
    algoritme_id: str | None


class AlgemeneInformatie(BaseModelOrmMode):
    id: str
    name: str
    organization: str
    department: str
    description_short: str
    type: str
    category: str
    website: str | None
    status: str

    inzet: Inzet | None
    juridisch: Juridisch | None
    metadata_algorithm: Metadata | None
    toepassing: Toepassing | None
    toezicht: Toezicht | None
