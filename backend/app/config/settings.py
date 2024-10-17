from pydantic import BaseSettings, Field


class Settings(BaseSettings):
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


class Keycloak(BaseSettings):
    KEYCLOAK_URI: str = Field(default="<KEYCLOAK_URI>")
    KEYCLOAK_REALM: str = Field(default="algreg_dev")
    KEYCLOAK_CLIENT: str = Field(default="authentication-client")
    ENABLE_AUTH: bool = Field(default=True)
    KEYCLOAK_API_URI: str = Field(
        default="<KEYCLOAK_API_URI>"
    )
    KEYCLOAK_API_CLIENT: str = Field(default="service-client")
    KEYCLOAK_API_SECRET: str = Field(default="")


class AzureTranslation(BaseSettings):
    api_key: str = Field(env="AZURE_TRANSLATE_API_KEY", default="secret")
    endpoint: str = Field(env="AZURE_TRANSLATE_ENDPOINT")
    region: str = Field(env="AZURE_TRANSLATE_REGION")


class DeepLSettings(BaseSettings):
    api_key: str = Field(env="DEEPL_API_KEY")


class WebSpellChecker(BaseSettings):
    api_key: str = Field(env="WEBSPELLCHECKER_API_KEY")
    api_url: str = Field(env="WEBSPELLCHECKER_URL")


