from typing import TypedDict
from pydantic import BaseModel
import enum


class Message(BaseModel):
    detail: str


class PreviewUrl(BaseModel):
    url: str


class Language(enum.Enum):
    NLD = "NLD"
    ENG = "ENG"
    FRY = "FRY"


class OperationEnum(str, enum.Enum):
    created = "created"
    new_version = "new_version"
    released = "released"
    published = "published"
    retracted = "retracted"
    preview_activated = "preview_activated"
    preview_used = "preview_used"
    preview_timeout = "preview_timeout"
    archived = "archived"
    unarchived = "unarchived"


class OrgType(str, enum.Enum):
    adviescollege = "adviescollege"
    agentschap = "agentschap"
    brandweer = "brandweer"
    caribisch_openbaar_lichaam = "caribisch_openbaar_lichaam"
    gemeente = "gemeente"
    grensoverschrijdend_regionaal_samenwerkingsorgaan = (
        "grensoverschrijdend_regionaal_samenwerkingsorgaan"
    )
    hoog_college_van_staat = "hoog_college_van_staat"
    interdepartementale_commissie = "interdepartementale_commissie"
    kabinet_van_de_koning = "kabinet_van_de_koning"
    koepelorganisatie = "koepelorganisatie"
    ministerie = "ministerie"
    omgevingsdienst = "omgevingsdienst"
    openbaar_lichaam_voor_beroep_en_bedrijf = "openbaar_lichaam_voor_beroep_en_bedrijf"
    organisatie_met_overheidsbemoeienis = "organisatie_met_overheidsbemoeienis"
    organisatieonderdeel = "organisatieonderdeel"
    politie = "politie"
    provincie = "provincie"
    regionaal_samenwerkingsverband = "regionaal_samenwerkingsverband"
    rechtspraak = "rechtspraak"
    regionaal_samenwerkingsorgaan = "regionaal_samenwerkingsorgaan"
    waterschap = "waterschap"
    zelfstandig_bestuursorgaan = "zelfstandig_bestuursorgaan"
    overig = "overig"
    veiligheidsregio = "veiligheidsregio"
    inspectie = "inspectie"


class RelationWithMinistry(str, enum.Enum):
    algemene_zaken = "Algemene Zaken"
    asiel_en_migratie = "Asiel en Migratie"
    binnenlandse_zaken_en_koninkrijksrelaties = (
        "Binnenlandse Zaken en Koninkrijksrelaties"
    )
    buitenlandse_zaken = "Buitenlandse Zaken"
    defensie = "Defensie"
    economische_zaken = "Economische Zaken"
    financiën = "Financiën"
    infrastructuur_en_waterstaat = "Infrastructuur en Waterstaat"
    justitie_en_veiligheid = "Justitie en Veiligheid"
    klimaat_en_groene_groei = "Klimaat en Groene Groei"
    landbouw_visserij_voedselzekerheid_en_natuur = (
        "Landbouw, Visserij, Voedselzekerheid en Natuur"
    )
    onderwijs_cultuur_en_wetenschap = "Onderwijs, Cultuur en Wetenschap"
    sociale_zaken_en_werkgelegenheid = "Sociale Zaken en Werkgelegenheid"
    volksgezondheid_welzijn_en_sport = "Volksgezondheid, Welzijn en Sport"
    volkshuisvesting_en_ruimtelijke_ordening = (
        "Volkshuisvesting en Ruimtelijke Ordening"
    )


class ImpacttoetsenGrouping(TypedDict):
    title: str
    link: str | None


class SourceDataGrouping(TypedDict):
    title: str
    link: str


class LawfulBasisGrouping(TypedDict):
    title: str
    link: str


class ImpactAssessments(enum.StrEnum):
    DPIA = "Data Protection Impact Assessment (DPIA)"
    IAMA = "Impact Assessment Mensenrechten en Algoritmes (IAMA)"
    FRIA = "Fundamental Rights Impact Assessment (FRIA)"
    AIIA = "AI Impact Assessment (AIIA)"
    FRAIA = "Fundamentele Rechten en Algoritme Impact Assessment (FRAIA)"
    DEDA = "De Ethische Data Assistant (DEDA)"
    UTHIEK = "Utrecht Uthiek Assessment"
    TOETSINGKADER = "Toetsingskader Algemene Rekenkamer"
    Z_INSPECTION = "Z-Inspection"
    ETHISCHE_BIJSLUITER = "De Ethische Bijsluiter"
    QUICKSCAN = "Privacy Quickscan"
    PRESCAN_DPIA = "Pre-scan DPIA"
    OTHER = "Overig"
    NONE = "Geen"


standard_impact_assessment_titles = [
    ImpactAssessments.DPIA,
    ImpactAssessments.IAMA,
    ImpactAssessments.FRIA,
    ImpactAssessments.AIIA,
    ImpactAssessments.FRAIA,
    ImpactAssessments.DEDA,
    ImpactAssessments.UTHIEK,
    ImpactAssessments.TOETSINGKADER,
    ImpactAssessments.Z_INSPECTION,
    ImpactAssessments.ETHISCHE_BIJSLUITER,
    ImpactAssessments.QUICKSCAN,
    ImpactAssessments.PRESCAN_DPIA,
]

standard_impact_assessment_titles_mapping = {
    Language.NLD: {
        ImpactAssessments.DPIA: "Data Protection Impact Assessment (DPIA)",
        ImpactAssessments.IAMA: "Impact Assessment Mensenrechten en Algoritmes (IAMA)",
        ImpactAssessments.FRIA: "Fundamental Rights Impact Assessment (FRIA)",
        ImpactAssessments.AIIA: "AI Impact Assessment (AIIA)",
        ImpactAssessments.FRAIA: "Fundamentele Rechten en Algoritme Impact Assessment (FRAIA)",
        ImpactAssessments.DEDA: "De Ethische Data Assistant (DEDA)",
        ImpactAssessments.UTHIEK: "Utrecht Uthiek Assessment",
        ImpactAssessments.TOETSINGKADER: "Toetsingskader Algemene Rekenkamer",
        ImpactAssessments.Z_INSPECTION: "Z-Inspection",
        ImpactAssessments.ETHISCHE_BIJSLUITER: "De Ethische Bijsluiter",
        ImpactAssessments.QUICKSCAN: "Privacy Quickscan",
        ImpactAssessments.PRESCAN_DPIA: "Pre-scan DPIA",
        ImpactAssessments.OTHER: "Overig",
        ImpactAssessments.NONE: "Geen",
    },
    Language.ENG: {
        ImpactAssessments.DPIA: "Data Protection Impact Assessment (DPIA)",
        ImpactAssessments.IAMA: "Human Rights and Algorithms Impact Assessment (IAMA)",
        ImpactAssessments.FRIA: "Fundamental Rights and Impact Assessment (FRIA)",
        ImpactAssessments.AIIA: "AI Impact Assessment (AIIA)",
        ImpactAssessments.FRAIA: "Fundamental Rights and Algorithm Impact Assessment (FRAIA)",
        ImpactAssessments.DEDA: "Data Ethics Decision Aid (DEDA)",
        ImpactAssessments.UTHIEK: "Utrecht Uthiek Assessment",
        ImpactAssessments.TOETSINGKADER: "Assessment framework of the Court of Audit",
        ImpactAssessments.Z_INSPECTION: "Z-Inspection",
        ImpactAssessments.ETHISCHE_BIJSLUITER: "The Ethical Guide",
        ImpactAssessments.QUICKSCAN: "Privacy Quickscan",
        ImpactAssessments.PRESCAN_DPIA: "Pre-scan DPIA",
        ImpactAssessments.OTHER: "Other",
        ImpactAssessments.NONE: "None",
    },
    Language.FRY: {
        ImpactAssessments.DPIA: "Data Protection Impact Assessment (DPIA)",
        ImpactAssessments.IAMA: "Ympact Assessment Minskerjochten en Algoritmes (IAMA)",
        ImpactAssessments.FRIA: "Fundamental Rights Impact Assessment (FRIA)",
        ImpactAssessments.AIIA: "AI Ympact Assessment (AIIA)",
        ImpactAssessments.FRAIA: "Fûnemintele rjochten en algoritme-ynfloedbeoardieling (FRAIA)",
        ImpactAssessments.DEDA: "De Ethische Data Assistant (DEDA)",
        ImpactAssessments.UTHIEK: "Utrecht Uthiek Assessment",
        ImpactAssessments.TOETSINGKADER: "Beoardielingskader fan 'e Rekkenkeamer",
        ImpactAssessments.Z_INSPECTION: "Z-ynspeksje",
        ImpactAssessments.ETHISCHE_BIJSLUITER: "De Etyske Folder",
        ImpactAssessments.QUICKSCAN: "Privacy Quickscan",
        ImpactAssessments.PRESCAN_DPIA: "DPIA foarôf scan",
        ImpactAssessments.OTHER: "Oar",
        ImpactAssessments.NONE: "Gjin",
    },
}

reverse_impact_assessment_titles_mapping = {
    lang: {label: enum_key for enum_key, label in mapping.items()}
    for lang, mapping in standard_impact_assessment_titles_mapping.items()
}


class SortOption(enum.StrEnum):
    sort_name = "sort_name"
    sort_number = "sort_number"


class PreComputedValues(enum.StrEnum):
    highlighted_algorithms = "highlighted_algorithms"


class OrganisationCluster(enum.StrEnum):
    Name = "name"
    Total = "Total"
    KD = "KD"
    Agency = "Agentschap"
    UTO = "UTO"
    BOO = "BOO"
    Overig = "Overig"
