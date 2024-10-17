from enum import Enum
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.controllers.user import get_from_keycloak_user
from app.middleware.keycloak_authenticator import get_current_user
from app.middleware.middleware import get_db
from app.services.keycloak.schemas import KeycloakUser
from .schemas import Role, Permission
from .user_configuration import UserConfiguration


class AuthType(Enum):
    """
    BaseOnly: Only need base rights, that's it.
    OrgOnly: Only need Organisation (Org) membership
    RoleOnly: Only need to have a certain Role
    OrgRole: Need access to Org and a certain Role
    OrgPermission: Org membership + a Permission derived from your role in the flow
    OrgRightStateChange: Org membership + a right to change state (needs action_key as path parameters)
    OrgRightState: Org membership + a right only available at a certain state
    """

    BaseOnly = "base-only"
    OrgOnly = "org-only"
    RoleOnly = "role-only"
    OrgRole = "org-role"
    OrgPermission = "org-permission"
    OrgRightStateChange = "org-right-state-change"


class Authoriser:
    def __init__(
        self,
        authorisation_type: AuthType,
        admin_auto_success: bool = True,
        role: Role | None = None,
        permission: Permission | None = None,
        legacy_action_key: str | None = None,
    ):
        self.authorisation_type = authorisation_type
        self.admin_auto_success = admin_auto_success
        self.role = role
        self.permission = permission
        self.legacy_action_key = legacy_action_key

    async def __call__(
        self,
        keycloak_user: Annotated[KeycloakUser, Depends(get_current_user)],
        db: Annotated[Session, Depends(get_db)],
        request: Request,
    ) -> None:
        """
        Forwards to the correct authorisation method based on authorisation_type.
        Check the 'match-case' to find which parameters are
        required for each authorisation type.
        """
        # Aborts early when user is not activated.
        if Role.Disabled in keycloak_user.roles:
            raise HTTPException(403, "USER_NOT_ACTIVATED")

        # Register path parameters if they are given in the endpoint definition.
        as_org = request.path_params.get("organisation_name", None)
        action_key = request.path_params.get("action_name", None)

        self.db = db
        user = get_from_keycloak_user(db, keycloak_user)
        user_config = UserConfiguration(user)
        # Returns early when the user has admin rights.
        if self.admin_auto_success and Role.Administrator in user.roles:
            return

        match self.authorisation_type:
            case AuthType.BaseOnly:
                # Should always succeed when this place is reached.
                pass
            case AuthType.OrgOnly:
                if as_org is None:
                    raise HTTPException(500)
                self.__check_org_membership(keycloak_user, as_org)
            case AuthType.RoleOnly:
                if self.role is None:
                    raise HTTPException(500)
                self.__check_role_ownership(keycloak_user, self.role)
            case AuthType.OrgRole:
                if as_org is None or self.role is None:
                    raise HTTPException(500)
                self.__check_org_membership(keycloak_user, as_org)
                self.__check_role_ownership(keycloak_user, self.role)
            case AuthType.OrgPermission:
                if as_org is None or self.permission is None:
                    raise HTTPException(500)
                # Org membership is implicitly checked in this method.
                self.__check_permission(user_config, as_org, self.permission)
            case AuthType.OrgRightStateChange:
                if as_org is None or action_key is None:
                    # Could still be hardcoded in the endpoint (in the case of old API endpoints):
                    if not self.legacy_action_key:
                        raise HTTPException(500)
                    action_key = self.legacy_action_key
                # Org membership is implicitly checked in this method.
                self.__check_state_change_permission(user_config, as_org, action_key)
            case _:
                raise NotImplementedError("Unknown authorisation type given.")

    def __check_org_membership(self, user: KeycloakUser, as_org: str) -> None:
        if as_org not in user.groups and Role.AllGroups not in user.roles:
            raise HTTPException(403, f"REQUIRED_ORGANISATION_{as_org.upper()}_MISSING")

    def __check_role_ownership(self, user: KeycloakUser, role: Role) -> None:
        if role not in user.roles:
            raise HTTPException(403, f"REQUIRED_ROLE_{role.value.upper()}_MISSING")

    def __check_permission(
        self, user: UserConfiguration, as_org: str, permission: Permission
    ) -> None:
        if not user.has_permission(as_org, permission):
            raise HTTPException(
                403, f"REQUIRED_PERMISSION_{permission.value.upper()}_MISSING"
            )

    def __check_state_change_permission(
        self,
        user: UserConfiguration,
        as_org: str,
        action_key: str,
    ) -> None:
        if not user.check_state_change_permission(as_org, action_key):
            raise HTTPException(403, "REQUIRED_STATE_CHANGE_PERMISSION_MISSING")
