from typing import TypedDict
from pydantic import BaseModel
import enum


class User(BaseModel):
    name: str
    organizations: list[str]
    role: str | None


class Message(BaseModel):
    detail: str


class PreviewUrl(BaseModel):
    url: str


class Language(enum.Enum):
    NLD = "NLD"
    ENG = "ENG"


class OperationEnum(str, enum.Enum):
    created = "created"
    new_version = "new version"
    released = "released"
    published = "published"
    retracted = "retracted"
    preview_activated = "preview activated"
    preview_used = "preview used"
    preview_timeout = "preview timeout"


class OrgType(str, enum.Enum):
    adviescollege = "Adviescollege"
    agentschap = "Agentschap"
    brandweer = "Brandweer"
    caribisch_openbaar_lichaam = "Caribisch openbaar lichaam"
    gemeente = "Gemeente"
    grensoverschrijdend_regionaal_samenwerkingsorgaan = (
        "Grensoverschrijdend regionaal samenwerkingsorgaan"
    )
    hoog_college_van_staat = "Hoog College van Staat"
    interdepartementale_commissie = "Interdepartementale commissie"
    kabinet_van_de_koning = "Kabinet van de Koning"
    koepelorganisatie = "Koepelorganisatie"
    ministerie = "Ministerie"
    openbaar_lichaam_voor_beroep_en_bedrijf = "Openbaar lichaam voor beroep en bedrijf"
    organisatie_met_overheidsbemoeienis = "Organisatie met overheidsbemoeienis"
    organisatieonderdeel = "Organisatieonderdeel"
    politie = "Politie"
    provincie = "Provincie"
    rechtspraak = "Rechtspraak"
    regionaal_samenwerkingsorgaan = "Regionaal samenwerkingsorgaan"
    waterschap = "Waterschap"
    zelfstandig_bestuursorgaan = "Zelfstandig bestuursorgaan"
    overig = "Overig"


class ImpacttoetsenGrouping(TypedDict):
    title: str
    link: str


class SourceDataGrouping(TypedDict):
    title: str
    link: str


class LawfulBasisGrouping(TypedDict):
    title: str
    link: str
