import app.models

models = {
    "inzet": app.models.Inzet,
    "algoritme": app.models.Algoritme,
    "juridisch": app.models.Juridisch,
    "metadata_algorithm": app.models.Metadata,
    "toepassing": app.models.Toepassing,
    "toezicht": app.models.Toezicht,
}

column_grouping = {
    "inzet": [
        "goal",
        "impact",
        "proportionality",
        "decision_making_process",
        "documentation",
    ],
    "juridisch": [
        "competent_authority",
        "lawful_basis",
        "iama",
        "iama_description",
        "dpia",
        "dpia_description",
        "objection_procedure",
    ],
    "metadata_algorithm": [
        "schema",
        "url",
        "contact_email",
        "area",
        "lang",
        "revision_date",
    ],
    "toepassing": [
        "description",
        "application_url",
        "publiccode",
        "mprd",
        "source_data",
        "methods_and_models",
    ],
    "toezicht": [
        "monitoring",
        "human_intervention",
        "risks",
        "performance_standard",
    ],
    "algoritme": [
        "name",
        "organization",
        "department",
        "description_short",
        "type",
        "category",
        "website",
        "status",
    ],
}
