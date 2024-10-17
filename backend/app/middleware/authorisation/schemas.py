from enum import Enum, StrEnum


class State(StrEnum):
    """
    An arbitrary number of states to be used by flows.
    An old version of an algorithm version has status EXPIRED.
    Meaning only the newest versions have STATE_X and other versions
    always have PUBLISHED / EXPIRED / ARCHIVED.
    """

    STATE_1 = "STATE_1"
    STATE_2 = "STATE_2"
    PUBLISHED = "PUBLISHED"
    EXPIRED = "EXPIRED"
    ARCHIVED = "ARCHIVED"


class Role(StrEnum):
    # You need an activated account to do anything
    Disabled = "disabled"
    # Access to all groups, used by ICTU-employees
    AllGroups = "all_groups"
    # Administrator, can do anything
    Administrator = "admin"

    # Has acces to the org detailpage
    OrgDetail = "orgdetail"
    # ICTU-employee, has special publication rights in some flows
    ICTU = "ictu"
    # Generic role, rights to be configured by flow
    ROLE_1 = "role_1"
    # Generic role, rights to be configured by flow
    ROLE_2 = "role_2"


class Permission(Enum):
    GET_ALGORITHM_VERSION = "GET_ALGORITHM_VERSION"
    POST_ALGORITHM_VERSION = "POST_ALGORITHM_VERSION"
    PUT_ALGORITHM_VERSION = "PUT_ALGORITHM_VERSION"
    UPDATE_ORG_DETAIL = "UPDATE_ORG_DETAIL"
