from enum import StrEnum
from functools import lru_cache
from typing import TypedDict

from app.schemas.action import StateChangeAction

from ..schemas import Role, Permission
from . import ICTU_LAST, SELF_PUBLISH_TWO


class Flow(StrEnum):
    ICTU_LAST = "ictu_last"
    SELF_PUBLISH_TWO = "self_publish_two"


class FlowMapping(TypedDict):
    role_state_change_actions_mapping: dict[Role, list[StateChangeAction]]
    state_change_actions: dict[str, StateChangeAction]
    role_permission_mapping: dict[Role, list[Permission]]
    role_label_mapping: dict[Role, str]
    alias: str


@lru_cache(maxsize=1)
def load_flow_configurations() -> dict[Flow, FlowMapping]:
    """
    Loads all flows into a single mapping
    """
    return {
        Flow.ICTU_LAST: {
            "role_state_change_actions_mapping": ICTU_LAST.ROLE_STATE_CHANGE_ACTIONS_MAPPING,
            "state_change_actions": ICTU_LAST.STATE_CHANGE_ACTIONS,
            "role_permission_mapping": ICTU_LAST.ROLE_PERMISSION_MAPPING,
            "role_label_mapping": ICTU_LAST.ROLE_LABEL_MAPPING,
            "alias": ICTU_LAST.FLOW_ALIAS,
        },
        Flow.SELF_PUBLISH_TWO: {
            "role_state_change_actions_mapping": SELF_PUBLISH_TWO.ROLE_STATE_CHANGE_ACTIONS_MAPPING,
            "state_change_actions": SELF_PUBLISH_TWO.STATE_CHANGE_ACTIONS,
            "role_permission_mapping": SELF_PUBLISH_TWO.ROLE_PERMISSION_MAPPING,
            "role_label_mapping": SELF_PUBLISH_TWO.ROLE_LABEL_MAPPING,
            "alias": SELF_PUBLISH_TWO.FLOW_ALIAS,
        },
    }
