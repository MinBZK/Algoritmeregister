with algoritme as (
    select
        algoritme.*,
        inzet.decision_making_process,
        inzet.documentation,
        inzet.goal,
        inzet.impact,
        inzet.proportionality,
        juridisch.competent_authority,
        juridisch.dpia,
        juridisch.dpia_description,
        juridisch.lawful_basis,
        juridisch.objection_procedure,
        metadata.area,
        metadata.contact_email,
        metadata.lang,
        metadata.revision_date,
        metadata.schema,
        metadata.url,
        toepassing.application_url,
        toepassing.description,
        toepassing.methods_and_models,
        toepassing.mprd,
        toepassing.publiccode,
        toepassing.source_data,
        toezicht.human_intervention,
        toezicht.monitoring,
        toezicht.performance_standard,
        toezicht.risks
    from
        algoritme
        join inzet on inzet.algoritme_id = algoritme.id
        join juridisch on juridisch.algoritme_id = algoritme.id
        join metadata on metadata.algoritme_id = algoritme.id
        join toepassing on toepassing.algoritme_id = algoritme.id
        join toezicht on toezicht.algoritme_id = algoritme.id
)
select
    *
from
    algoritme