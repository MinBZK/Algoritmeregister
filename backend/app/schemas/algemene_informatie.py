from pydantic import BaseModel


class AlgemeneInformatie(BaseModel):
    id: str  

    class Config:
        orm_mode = True
