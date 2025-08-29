from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )


class Settings(BaseSettingsConfig):
    enable_debug: bool = Field(default=False)
    enable_translation: bool = Field(default=False)
    preview_url: str = Field(default="localhost:3001")
    webform_url: str = Field(default="localhost:3001/webformulier")
    retract_preview_time: int = Field(default=600)
    debugger_logging: bool = Field(default=True)

    application_mail_address: str = Field(default="Algoritmeregister@<MAIL_DOMAIN>")
    c3po_url: str = Field(default="http://localhost:8500/api")
    use_c3po: bool = Field(default=False)
    send_emails: bool = Field(default=True)
    # Will only work if send_emails is also True
    notify_c3po_errors: bool = Field(default=True)
    MAIL_RELAY: str = Field(default="<MAIL_RELAY>")
    MAIL_PASSWORD: str = Field(default="<MAIL_PASSWORD>")


class Keycloak(BaseSettingsConfig):
    KEYCLOAK_URI: str = Field(default="<KEYCLOAK_URI>")
    KEYCLOAK_REALM: str = Field(default="algreg_dev")
    KEYCLOAK_CLIENT: str = Field(default="authentication-client")
    ENABLE_AUTH: bool = Field(default=True)
    KEYCLOAK_API_URI: str = Field(
        default="<KEYCLOAK_API_URI>"
    )
    KEYCLOAK_API_CLIENT: str = Field(default="service-client")
    KEYCLOAK_API_SECRET: str = Field(default="")


class AzureTranslation(BaseSettingsConfig):
    AZURE_TRANSLATE_API_KEY: str
    AZURE_TRANSLATE_ENDPOINT: str
    AZURE_TRANSLATE_REGION: str


class DeepLSettings(BaseSettingsConfig):
    DEEPL_API_KEY: str


class WebSpellChecker(BaseSettingsConfig):
    WEBSPELLCHECKER_API_KEY: str
    WEBSPELLCHECKER_URL: str


class Preditor(BaseSettingsConfig):
    get_url: str = Field(default="/api/static-content", env="GET_URL")
    put_url: str = Field(default="/preditor/static-content", env="PUT_URL")
    static_content_path_pub: str = Field(
        default="app/data/preditor/static_content_pub.json",
        env="STATIC_CONTENT_PATH_PUB",
    )
    static_content_path_draft: str = Field(
        default="app/data/preditor/static_content_draft.json",
        env="STATIC_CONTENT_PATH_DRAFT",
    )
    # Fallback contents file
    static_content_path_default: str = Field(
        default="app/data/static_content_default.json",
        env="STATIC_CONTENT_PATH_DEFAULT",
    )
    preditor_shared_secret_key: str
    preditor_shared_totp_seed: str
