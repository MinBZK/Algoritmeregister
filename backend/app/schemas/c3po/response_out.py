from pydantic import BaseModel


class RuleResults(BaseModel):
    rule_code: str
    description: str
    feedback_message: str
    result: bool | None


class C3poResults(BaseModel):
    rules: list[RuleResults]


class Rule(BaseModel):
    rule_code: str
    rule_variant: str
    description: str
    severity_level: str


class RuleSetOut(BaseModel):
    code: str
    rules: list[Rule]
