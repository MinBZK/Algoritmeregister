from abc import ABC
from typing import NoReturn, TypedDict, cast
from fastapi import HTTPException
from keycloak import (
    KeycloakAdmin,
    KeycloakConnectionError,
    KeycloakError,
    KeycloakPostError,
)

from .payload_maker import KeycloakPayloadMaker
from .schemas import (
    KeycloakGroup,
    KeycloakUser,
    KeycloakUserFromRepo,
    KeycloakUserNew,
    KeycloakUserUpdate,
)
from .data_validator import KeycloakValidator

from app.util.logger import get_logger

logger = get_logger(__name__)


class ConnectionSettings(TypedDict):
    realm_name: str
    server_url: str
    client_id: str
    client_secret_key: str


class KeycloakRepository(ABC):
    def __init__(self, settings: ConnectionSettings):
        """
        Initiating takes a long time (100ms)
        """
        try:
            self.client = KeycloakAdmin(**settings)
        except KeycloakConnectionError:
            logger.error("Keycloak cannot be found, connection failed")
            raise HTTPException(424)
        self.validate = KeycloakValidator()
        self.make_payload = KeycloakPayloadMaker()

    def __err__(
        self,
        error: KeycloakError,
        msg: str | None = None,
        error_code: int | None = None,
    ) -> NoReturn:
        err: int | None = error_code or int(cast(str, error.response_code))
        logger.error(
            (str(err) or "UNKNOWN ERROR: ") + (msg or str(error.error_message))
        )
        raise HTTPException(int(err) or 400, msg)

    def get_all(self, **kwargs) -> list[KeycloakUserFromRepo]:
        query = self.make_payload.kwargs_to_query(**kwargs) if kwargs else {}
        try:
            users = self.client.get_users(query)
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.users(users)

    def get_count(self, **kwargs) -> int:
        query = self.make_payload.kwargs_to_query(**kwargs) if kwargs else {}
        try:
            count = self.client.users_count(query)
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.count(count)

    def get_user(self, user_id: str) -> KeycloakUser:
        try:
            user = self.client.get_user(user_id)
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.user(user)

    def get_groups(self) -> list[KeycloakGroup]:
        """
        Gets the groups registered in Keycloak.
        """
        try:
            groups = self.client.get_groups()
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.groups(groups)

    def get_group_members(self, group_id: str) -> list[KeycloakUserFromRepo]:
        """
        Gets the members of a groups registered in Keycloak.
        """
        try:
            members = self.client.get_group_members(group_id)
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.users(members)

    def update_user(
        self,
        user_id: str,
        update_values: KeycloakUserUpdate,
    ) -> KeycloakUser:
        try:
            user = self.client.get_user(user_id)
            validated_user = self.validate.user(user)
            payload = self.make_payload.update_user(validated_user, update_values)
            self.client.update_user(user_id, payload)
            updated_user = self.client.get_user(user_id)
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.user(updated_user)

    def delete_user(self, user_id: str) -> None:
        try:
            self.client.delete_user(user_id)
        except KeycloakError as e:
            self.__err__(e)

    def create_user(self, new_user: KeycloakUserNew) -> KeycloakUser:
        try:
            payload = self.make_payload.new_user(new_user)
            user_id = self.client.create_user(payload)
            user = self.client.get_user(user_id)
        except KeycloakPostError as e:
            if e.response_code == 409:
                self.__err__(e, "NOT_UNIQUE_USERNAME")
            elif "error-invalid-email" in str(e.error_message):
                self.__err__(e, "INVALID_EMAIL")
            else:
                self.__err__(e, "Unknown Post Error")
        except KeycloakError as e:
            self.__err__(e)
        return self.validate.user(user)
