from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    enable_debug: bool = Field(default=False)
    enable_translation: bool = Field(default=False)
    preview_url: str = Field(default="localhost:3001")
    webform_url: str = Field(default="localhost:3001/webformulier")
    retract_preview_time: int = Field(default=600)

    application_mail_address: str = Field(default="Algoritmeregister@i8s.nl")
    c3po_url: str = Field(default="http://localhost:8001/api")


class Keycloak(BaseSettings):
    KEYCLOAK_URI: str = Field(default="https://s04.i8s.nl")
    KEYCLOAK_REALM: str = Field(default="algreg_dev")
    KEYCLOAK_CLIENT: str = Field(default="authentication-client")


class AzureTranslation(BaseSettings):
    api_key: str = Field(env="AZURE_TRANSLATE_API_KEY", default="secret")
    endpoint: str = Field(env="AZURE_TRANSLATE_ENDPOINT")
    region: str = Field(env="AZURE_TRANSLATE_REGION")


class DeepLSettings(BaseSettings):
    api_key: str = Field(env="DEEPL_API_KEY")


class EUTranslateSettings(BaseSettings):
    app_id: str = Field(env="EU_TRANSLATE_APP_ID")
    api_key: str = Field(env="EU_TRANSLATE_API_KEY")
    endpoint: str = Field(env="EU_TRANSLATE_ENDPOINT")
