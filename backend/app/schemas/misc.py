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
    OTHER = "Overig"
    NONE = "Geen"


standard_impact_assessment_titles = [
    ImpactAssessments.IAMA,
    ImpactAssessments.DPIA,
    ImpactAssessments.FRIA,
]


class SortOption(enum.StrEnum):
    sort_name = "sort_name"
    sort_number = "sort_number"
