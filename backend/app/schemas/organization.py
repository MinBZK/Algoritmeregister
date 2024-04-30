from pydantic import BaseModel
from .misc import OrgType


class OrganisationIn(BaseModel):
    name: str
    code: str
    type: OrgType | None

    class Config:
        orm_mode = True


class OrganisationDB(OrganisationIn):
    id: int

    class Config:
        orm_mode = True


class OrganisationGrouping(BaseModel):
    type: OrgType | None
    name: str
    count: int

    class Config:
        orm_mode = True
