from typing import TypedDict


class ProcessingRequestOut(TypedDict):
    payload: str
    rule_codes: list[str]
