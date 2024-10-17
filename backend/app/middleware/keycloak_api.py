from app.config.settings import Keycloak
from app.services.keycloak.repository import ConnectionSettings


env_settings = Keycloak()
kc_settings: ConnectionSettings = {
    "realm_name": env_settings.KEYCLOAK_REALM,
    "server_url": env_settings.KEYCLOAK_API_URI,
    "client_id": env_settings.KEYCLOAK_API_CLIENT,
    "client_secret_key": env_settings.KEYCLOAK_API_SECRET,
}
