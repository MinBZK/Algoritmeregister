from typing import TypedDict, Literal


class ProcessingRequestOut(TypedDict):
    payload: str
    org_code: str
    project_code: str
    rule_codes: list[str] | Literal["all"]
