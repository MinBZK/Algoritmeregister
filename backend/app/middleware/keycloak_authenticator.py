from typing import Annotated
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import ExpiredSignatureError
import time
from app.config.settings import Keycloak
from app.middleware.authorisation.schemas import Role
from app.services.keycloak import KeycloakUser
from app.services.keycloak.data_validator import KeycloakValidator
from app.util.logger import get_logger

logger = get_logger(__name__)

settings = Keycloak()
URI = settings.KEYCLOAK_URI
CLIENT = settings.KEYCLOAK_CLIENT
REALM = settings.KEYCLOAK_REALM

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/token",
    auto_error=False,
)

cache = dict()

logger.debug(f"{URI}/realms/{REALM}/protocol/openid-connect/auth")


class UserUnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inloggegevens konden niet succesvol worden gevalideerd.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _update_public_key(keycloak_openid: KeycloakOpenID, update_interval=30):
    """
    Update cache by fetching a new public key
    Returns false if last update is less than <update_interval> seconds ago to prevent overusage and infinite loops
    """
    if time.time() - cache["keycloak_public_key_updated"] > update_interval:
        cache["keycloak_public_key"] = keycloak_openid.public_key()
        cache["keycloak_public_key_updated"] = time.time()
        return True
    return False


def _get_public_key(keycloak_openid: KeycloakOpenID):
    if "keycloak_public_key" not in cache:
        logger.debug("fetching public key")
        cache["keycloak_public_key"] = keycloak_openid.public_key()
        cache["keycloak_public_key_updated"] = time.time()
    return cache["keycloak_public_key"]


def _decode_token(token: str):
    """
    Fetch the public key from Keycloak and decode the token from the frontend.
    Note: Data in the token is NOT encrypted. the public key is only to validate.
    """
    logger.debug("authorizing")
    # public access type
    keycloak_openid = KeycloakOpenID(
        server_url=URI,
        client_id=CLIENT,
        realm_name=REALM,
    )

    public_key = _get_public_key(keycloak_openid)
    KEYCLOAK_PUBLIC_KEY = (
        "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"
    )
    try:
        decoded = jwt.decode(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
            algorithms=["RS256"],
        )
        logger.debug(f'session for {decoded["preferred_username"]} still active')
        return decoded

    except ExpiredSignatureError:
        logger.debug("session expired")
        raise UserUnauthorizedException()

    except jwt.exceptions.DecodeError:
        if _update_public_key(keycloak_openid):
            logger.debug("Could not decode token. Updating public key and retry once")
            return _decode_token(token)
        logger.debug("Could not decode token")
        raise UserUnauthorizedException()

    except jwt.exceptions.ImmatureSignatureError:
        logger.debug("token not yet valid, retrying")
        time.sleep(0.5)
        return _decode_token(token)


def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)]
) -> KeycloakUser:
    if not settings.ENABLE_AUTH:
        return KeycloakUser(
            username="local admin",
            roles=[Role.Administrator, Role.AllGroups],
            groups=[],
            id="<UPDATE_WITH_KEYCLOAK_ADMIN_ID>",
            first_name="",
            last_name="",
        )
    elif token is None:
        raise HTTPException(401, "TOKEN_NOT_FOUND")

    user = _decode_token(token)
    user_schema = KeycloakValidator().user_from_token(user)
    logger.debug(f"received token for {user_schema.username}")
    return user_schema
