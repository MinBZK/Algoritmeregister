from app.schemas.action import StateChangeAction
from .schemas import Permission, Role
from app.schemas.user import User
from .config._base import load_flow_configurations


class UserConfiguration:
    """
    Provides helper methods to translate user and flow configuration
    to useful statements about permissions, rights.
    """

    def __init__(self, user: User) -> None:
        self.user = user
        all_configs = load_flow_configurations()
        self.flows = {org.code: all_configs[org.flow] for org in user.organisations}

    def has_permission(self, org_context: str, permission: Permission) -> bool:
        return True if permission in self._permissions(org_context) else False

    def check_state_change_permission(self, org_context: str, action_key: str) -> bool:
        """
        Returns true if any of the available actions match the requested state change.
        """
        permissions = self._state_change_permissions(org_context)
        return any(a for a in permissions if a.key == action_key)

    def _permissions(self, org_context: str) -> list[Permission]:
        # Only permissions within the context (of the given organisation) is checked.
        context = self.flows.get(org_context, None)
        if context is None:
            return []

        permission_mapping = context["role_permission_mapping"]
        # Collects all permissions given by the roles of the user.
        permissions: list[Permission] = []
        for role in self.user.roles:
            permissions.extend(permission_mapping.get(role, []))
        return list(set(permissions))

    def _state_change_permissions(self, org_context: str) -> list[StateChangeAction]:
        """
        Collects all allowed state change actions.
        """
        context = self.flows.get(org_context, None)
        if context is None:
            return []
        state_change_mapping = context["role_state_change_actions_mapping"]

        all_permissions: list[StateChangeAction] = []
        if Role.Administrator in self.user.roles:
            # Give all permissions to admin. The comprehension unfolds list of lists.
            all_permissions = [x for xs in state_change_mapping.values() for x in xs]
        else:
            # Give only the permissions you have the role for.
            for role in self.user.roles:
                role_permissions = state_change_mapping.get(role, [])
                all_permissions.extend(role_permissions)
        ordered_actions = [
            a for a in context["state_change_actions"].values() if a in all_permissions
        ]
        return [StateChangeAction(**a.dict()) for a in ordered_actions]
