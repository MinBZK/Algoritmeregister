from app.schemas.action import EmailType, StateChangeAction
from ..schemas import Role, Permission, State

"""
Two roles exists at the organisation. One of the roles has publication rights.
"""

# Names used in frontend
FLOW_ALIAS: str = "De organisatie publiceert in twee stappen."

ROLE_LABEL_MAPPING: dict[Role, str] = {
    Role.ROLE_1: "Redacteur",
    Role.ROLE_2: "Goedkeurder",
}

# Define the actions to change state and their properties.
STATE_CHANGE_ACTIONS: dict[str, StateChangeAction] = {
    "release_to_2": StateChangeAction(
        label="Vrijgeven naar goedkeurder",
        key="release_to_2",
        origin_state=State.STATE_1,
        target_state=State.STATE_2,
        send_email_type=EmailType.RELEASE_SELF_PUBLISH_TWO,
    ),
    "publish": StateChangeAction(
        label="Publiceren",
        key="publish",
        origin_state=State.STATE_2,
        target_state=State.PUBLISHED,
    ),
    "reject_to_1": StateChangeAction(
        label="Terugzetten naar redacteur",
        key="reject_to_1",
        origin_state=State.STATE_2,
        target_state=State.STATE_1,
    ),
    "retract": StateChangeAction(
        label="Depubliceren",
        key="retract",
        origin_state=State.PUBLISHED,
        target_state=State.STATE_2,
        send_email_type=EmailType.RETRACT,
    ),
}

# For each role, define the actions they are allowed to take.
ROLE_STATE_CHANGE_ACTIONS_MAPPING: dict[Role, list[StateChangeAction]] = {
    Role.ROLE_1: [STATE_CHANGE_ACTIONS["release_to_2"]],
    Role.ROLE_2: [
        STATE_CHANGE_ACTIONS["publish"],
        STATE_CHANGE_ACTIONS["reject_to_1"],
        STATE_CHANGE_ACTIONS["retract"],
    ],
}

# For each role, what are their permissions? What can they see and access?
ROLE_PERMISSION_MAPPING: dict[Role, list[Permission]] = {
    Role.ROLE_1: [
        Permission.GET_ALGORITHM_VERSION,
        Permission.POST_ALGORITHM_VERSION,
        Permission.PUT_ALGORITHM_VERSION,
    ],
    Role.ROLE_2: [Permission.GET_ALGORITHM_VERSION, Permission.PUT_ALGORITHM_VERSION],
}
