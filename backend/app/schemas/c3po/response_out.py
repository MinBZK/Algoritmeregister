from typing import Optional, Union, Any

from pydantic import BaseModel


class RuleResults(BaseModel):
    rule_code: str
    title: str
    feedback_message: str
    passed: bool | None
    result: Optional[Union[str, list[Any], dict[str, Any]]]
    severity_level: str


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
