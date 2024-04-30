from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi import Depends
from keycloak import KeycloakOpenID
from fastapi import HTTPException, status
import jwt
from jwt.exceptions import ExpiredSignatureError
import logging
import time
from app.config.settings import Keycloak
from app import schemas

logger = logging.getLogger(__name__)

settings = Keycloak()
URI = settings.KEYCLOAK_URI
CLIENT = settings.KEYCLOAK_CLIENT
REALM = settings.KEYCLOAK_REALM

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{URI}/realms/{REALM}/protocol/openid-connect/token",
)

cache = dict()

logger.info(f"{URI}/realms/{REALM}/protocol/openid-connect/auth")


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
        logger.info("fetching public key")
        cache["keycloak_public_key"] = keycloak_openid.public_key()
        cache["keycloak_public_key_updated"] = time.time()
    return cache["keycloak_public_key"]


def _decode_token(token: str):
    """
    Fetch the public key from Keycloak and decode the token from the frontend.
    Note: Data in the token is NOT encrypted. the public key is only to validate.
    """
    logger.info("authorizing")
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
        logger.info(f'session for {decoded["preferred_username"]} still active')
        return decoded

    except ExpiredSignatureError:
        logger.info("session expired")
        raise UserUnauthorizedException()

    except jwt.exceptions.DecodeError:
        if _update_public_key(keycloak_openid):
            logger.info("Could not decode token. Updating public key and retry once")
            return _decode_token(token)
        logger.info("Could not decode token")
        raise UserUnauthorizedException()

    except jwt.exceptions.ImmatureSignatureError:
        logger.info("token not yet valid, retrying")
        time.sleep(0.5)
        return _decode_token(token)


def get_current_user(token=Depends(oauth2_scheme)) -> schemas.User:
    user = _decode_token(token)
    logger.debug(f"received token for {user['preferred_username']}")
    # Keycloak gives organisations with a '/' before the organisation, slice it.
    organizations = [org[1:] for org in user.get("group", [])]
    user_schema = schemas.User(
        organizations=organizations,
        name=user.get("preferred_username"),
        role=user.get("role"),
    )
    return user_schema
