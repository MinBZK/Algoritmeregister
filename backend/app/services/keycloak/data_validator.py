from typing import Any
from fastapi import HTTPException
from pydantic import ValidationError

from .schemas import KeycloakGroup, KeycloakUser, KeycloakUserFromRepo
from . import NotAListError, NotValidError

from app.util.logger import get_logger

logger = get_logger(__name__)


class KeycloakValidator:
    @classmethod
    def user(cls, user: Any) -> KeycloakUserFromRepo:
        try:
            return KeycloakUserFromRepo(
                username=user.get("username"),
                roles=user.get("attributes", {}).get("roles", []),
                groups=user.get("attributes", {}).get("groups", []),
                id=user.get("id"),
                first_name=user.get("firstName", "Onbekende voornaam"),
                last_name=user.get("lastName", "Onbekende achternaam"),
                created_at=user.get("createdTimestamp"),
            )
        except ValidationError as e:
            raise NotValidError(user, e)

    @classmethod
    def user_from_token(cls, user: Any) -> KeycloakUser:
        """
        The token has a different structure, needs its own validator
        """
        try:
            return KeycloakUser(
                username=user.get("preferred_username"),
                roles=user.get("roles", []),
                groups=user.get("groups", []),
                id=user.get("sub"),
                first_name=user.get("given_name", "Onbekende voornaam"),
                last_name=user.get("family_name", "Onbekende achternaam"),
            )
        except ValidationError as e:
            raise NotValidError(user, e)

    @classmethod
    def count(cls, count: Any) -> int:
        try:
            return int(count)
        except ValueError:
            raise HTTPException(424)

    @classmethod
    def users(cls, users: Any) -> list[KeycloakUserFromRepo]:
        cls.__test_for_list(users)
        return [cls.user(u) for u in users]

    @classmethod
    def group(cls, group: Any) -> KeycloakGroup:
        try:
            return KeycloakGroup(name=group.get("name"), id=group.get("id"))
        except ValidationError as e:
            raise NotValidError(group, e)

    @classmethod
    def groups(cls, groups: Any) -> list[KeycloakGroup]:
        cls.__test_for_list(groups)
        return [cls.group(g) for g in groups]

    @classmethod
    def __test_for_list(cls, obj) -> None:
        if not isinstance(obj, list):
            raise NotAListError
