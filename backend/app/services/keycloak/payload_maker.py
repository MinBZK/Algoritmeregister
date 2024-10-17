from app.services.keycloak.schemas import (
    KeycloakUser,
    KeycloakUserNew,
    KeycloakUserUpdate,
)


class KeycloakPayloadMaker:
    @classmethod
    def update_user(cls, user: KeycloakUser, new_values: KeycloakUserUpdate) -> dict:
        """
        Constructs a payload to be used by the update_user endpoint.
        """
        updated_user = KeycloakUserUpdate(**user.dict())
        # Update values in the KeycloakUserUpdate object whenever a value in update_value is given
        for attr, value in new_values.__dict__.items():
            if value is not None:
                setattr(updated_user, attr, value)

        return {
            "firstName": updated_user.first_name,
            "lastName": updated_user.last_name,
            "email": user.username,  # Must re-define email, else it disappears.
            "attributes": {"roles": updated_user.roles, "groups": updated_user.groups},
        }

    @classmethod
    def new_user(cls, body: KeycloakUserNew) -> dict:
        return {
            "username": body.username,
            "attributes": {"groups": body.groups or [], "roles": body.roles or []},
            "enabled": True,
            "email": body.username,
            "firstName": body.first_name,
            "lastName": body.last_name,
            "requiredActions": [
                "CONFIGURE_TOTP",
                "UPDATE_PASSWORD",
                "VERIFY_EMAIL",
            ],
        }

    @classmethod
    def kwargs_to_query(
        cls,
        *,
        limit: int | None = None,
        skip: int | None = None,
        group: str | None = None,
        role: str | None = None,
        q: str | None = None
    ) -> dict:
        """
        Converts keyword arguments to a query that keycloak API understands.
        https://www.keycloak.org/docs-api/22.0.1/rest-api/index.html

        Available keywords for conversion:
        - limit: The maximum amount of results requested
        - skip: The offset in results, how many results to skip.
        - group: Looks for users with membership in the given group.
        - role: Looks for users with the given role.
        - q: Matches with users in username, first or last name, or email.

        returns: query object for keycloak API.
        """
        query = {}
        if limit is not None:
            query["max"] = limit
        if skip is not None:
            query["first"] = skip
        if group is not None:
            query["q"] = (query.get("q") or "") + " groups:" + group
        if role is not None:
            query["q"] = (query.get("q") or "") + " roles:" + role
        if q is not None:
            query["search"] = "*" + q + "*"
        return query
