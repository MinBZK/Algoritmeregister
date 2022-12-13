from enum import Enum


class Columns(str, Enum):
    all = "*"

    algoritme_organization = "algoritme.organization"
    algoritme_name = "algoritme.name"
    algoritme_department = "algoritme.department"
    algoritme_description_short = "algoritme.description_short"
    algoritme_type = "algoritme.type"
    algoritme_category = "algoritme.category"
    algoritme_website = "algoritme.website"
    algoritme_status = "algoritme.status"
    algoritme_uuid = "algoritme.uuid"
    algoritme_toegevoegd_op = "algoritme.toegevoegd_op"
    algoritme_slug = "algoritme.slug"

    inzet_goal = "inzet.goal"
    inzet_impact = "inzet.impact"
    inzet_proportionality = "inzet.proportionality"
    inzet_decision_making_process = "inzet.decision_making_process"
    inzet_documentation = "inzet.documentation"
    inzet_toegevoegd_op = "inzet.toegevoegd_op"

    juridisch_competent_authority = "juridisch.competent_authority"
    juridisch_lawful_basis = "juridisch.lawful_basis"
    juridisch_iama = "juridisch.iama"
    juridisch_iama_description = "juridisch.iama_description"
    juridisch_dpia = "juridisch.dpia"
    juridisch_dpia_description = "juridisch.dpia_description"
    juridisch_objection_procedure = "juridisch.objection_procedure"
    juridisch_toegevoegd_op = "juridisch.toegevoegd_op"

    metadata_schema = "metadata.schema"
    metadata_uuid = "metadata.uuid"
    metadata_url = "metadata.url"
    metadata_contact_email = "metadata.contact_email"
    metadata_area = "metadata.area"
    metadata_lang = "metadata.lang"
    metadata_revision_date = "metadata.revision_date"
    metadata_toegevoegd_op = "metadata.toegevoegd_op"

    toepassing_description = "toepassing.description"
    toepassing_application_url = "toepassing.application_url"
    toepassing_publiccode = "toepassing.publiccode"
    toepassing_mprd = "toepassing.mprd"
    toepassing_source_data = "toepassing.source_data"
    toepassing_methods_and_models = "toepassing.methods_and_models"
    toepassing_toegevoegd_op = "toepassing.toegevoegd_op"

    toezicht_monitoring = "toezicht.monitoring"
    toezicht_human_intervention = "toezicht.human_intervention"
    toezicht_risks = "toezicht.risks"
    toezicht_performance_standard = "toezicht.performance_standard"
    toezicht_toegevoegd_op = "toezicht.toegevoegd_op"


# columns=metadata.contact_email
# columns=metadata.toegevoegd_op

# columns=toepassing.toegevoegd_op

# columns=toezicht.human_intervention
# columns=toezicht.toegevoegd_op
