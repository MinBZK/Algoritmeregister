from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    type: str = Field("PUB")
    enable_debug: bool = Field(False)
    preview_url: str = Field("localhost:3000/concept")
    retract_preview_time: int = Field(600)


class Keycloak(BaseSettings):
    KEYCLOAK_URI: str = Field(default="https://s04.i8s.nl")
    KEYCLOAK_REALM: str = Field(default="algreg_dev")
    KEYCLOAK_CLIENT: str = Field(default="authentication-client")
