from pydantic import BaseModel


class C3poRequest(BaseModel):
    text: str
