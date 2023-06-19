from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    type: str = Field("PUB")
    enable_debug: bool = Field(False)
    preview_url: str = Field("localhost:3000/concept")
    webform_url: str = Field("localhost:3001/webformulier")
    retract_preview_time: int = Field(600)

    application_mail_address: str = Field("Algoritmeregister@i8s.nl")


class Keycloak(BaseSettings):
    KEYCLOAK_URI: str = Field(default="https://s04.i8s.nl")
    KEYCLOAK_REALM: str = Field(default="algreg_dev")
    KEYCLOAK_CLIENT: str = Field(default="authentication-client")
