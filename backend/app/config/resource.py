from enum import Enum


class Columns(str, Enum):
    all = "*"

    algoritme_organization = "organization"
    algoritme_name = "name"
    algoritme_department = "department"
    algoritme_description_short = "description_short"
    algoritme_type = "type"
    algoritme_category = "category"
    algoritme_website = "website"
    algoritme_status = "status"
    algoritme_uuid = "uuid"
    algoritme_create_dt = "create_dt"

    inzet_goal = "goal"
    inzet_impact = "impact"
    inzet_proportionality = "proportionality"
    inzet_decision_making_process = "decision_making_process"
    inzet_documentation = "documentation"

    juridisch_competent_authority = "competent_authority"
    juridisch_lawful_basis = "lawful_basis"
    juridisch_iama = "iama"
    juridisch_iama_description = "iama_description"
    juridisch_dpia = "dpia"
    juridisch_dpia_description = "dpia_description"
    juridisch_objection_procedure = "objection_procedure"

    metadata_schema = "schema"
    metadata_uuid = "uuid"
    metadata_url = "url"
    metadata_contact_email = "contact_email"
    metadata_area = "area"
    metadata_lang = "lang"
    metadata_revision_date = "revision_date"

    toepassing_description = "description"
    toepassing_application_url = "application_url"
    toepassing_publiccode = "publiccode"
    toepassing_mprd = "mprd"
    toepassing_source_data = "source_data"
    toepassing_methods_and_models = "methods_and_models"

    toezicht_monitoring = "monitoring"
    toezicht_human_intervention = "human_intervention"
    toezicht_risks = "risks"
    toezicht_performance_standard = "performance_standard"
