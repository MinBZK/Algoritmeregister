from pydantic import BaseModel, Field


class C3poRequest(BaseModel):
    text: str
    ruleSet: str = Field(default=..., example="ar_v0_4_0_short_description")
