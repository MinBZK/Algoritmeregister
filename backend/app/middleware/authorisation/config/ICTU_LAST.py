from app.schemas.action import EmailType, StateChangeAction
from ..schemas import Role, Permission, State

"""
The original publication flow: One person at the organisation 'releases' the content
To ICTU, which publishes it.
"""

# Names used in frontend
FLOW_ALIAS: str = "ICTU Publiceert"

ROLE_LABEL_MAPPING: dict[Role, str] = {
    Role.ROLE_1: "Redacteur",
    Role.ICTU: "ICTU-medewerker",
}

STATE_LABEL_MAPPING: dict[State, str] = {
    State.STATE_1: "In bewerking",
    State.STATE_2: "Vrijgegeven",
    State.PUBLISHED: "Gepubliceerd",
}

# Define the actions to change state and their properties.
STATE_CHANGE_ACTIONS: dict[str, StateChangeAction] = {
    "release": StateChangeAction(
        label="Vrijgeven",
        key="release",
        origin_state=State.STATE_1,
        target_state=State.STATE_2,
        send_email_type=EmailType.RELEASE_ICTU_LAST,
    ),
    "publish": StateChangeAction(
        label="Publiceren",
        key="publish",
        origin_state=State.STATE_2,
        target_state=State.PUBLISHED,
    ),
    "retract": StateChangeAction(
        label="Depubliceren",
        key="retract",
        origin_state=State.PUBLISHED,
        target_state=State.STATE_1,
        send_email_type=EmailType.RETRACT,
    ),
}

# For each role, define the actions they are allowed to take.
ROLE_STATE_CHANGE_ACTIONS_MAPPING: dict[Role, list[StateChangeAction]] = {
    Role.ROLE_1: [STATE_CHANGE_ACTIONS["release"], STATE_CHANGE_ACTIONS["retract"]],
    Role.ICTU: [STATE_CHANGE_ACTIONS["publish"], STATE_CHANGE_ACTIONS["retract"]],
}

# For each role, what are their permissions? What can they see and access?
ROLE_PERMISSION_MAPPING: dict[Role, list[Permission]] = {
    Role.ROLE_1: [
        Permission.GET_ALGORITHM_VERSION,
        Permission.POST_ALGORITHM_VERSION,
        Permission.PUT_ALGORITHM_VERSION,
    ],
    Role.ICTU: [
        Permission.GET_ALGORITHM_VERSION,
        Permission.PUT_ALGORITHM_VERSION,
    ],
}
