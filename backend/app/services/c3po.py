import httpx
from fastapi import HTTPException
from starlette import status

from app.config.settings import Settings
from app.schemas import c3po as c3po_schemas
from app.util.html import strip_html
from app.util.logger import get_logger
from app import mailing

logger = get_logger(__name__)
env_settings = Settings()

_LANGUAGE_CHECK_RULE_CODES = [
    "BROKEN_LINKS",
    "B1_LANGUAGE_LEVEL",
    "LIMITED_SENTENCE_LENGTH",
]


def handle_c3po_exception(
    error: Exception,
    rule_codes: str | list[str] = "",
    organisation_name: str = "",
    algorithm_name: str = "",
) -> None:
    """
    Generate an informative error message.

    Distinct messages are returned for service related exceptions and unknown exceptions.

    :raises HTTPException: If the connection with the C3PO API fails
    """
    if not (env_settings.send_emails and env_settings.notify_c3po_errors):
        logger.info(
            "Notification of C3PO errors is disabled in this environment, email sending aborted."
        )
        return

    if not rule_codes:
        rule_codes_text = "Niet beschikbaar"
    elif isinstance(rule_codes, list):
        rule_codes_text = ", ".join(rule_codes)
    elif isinstance(rule_codes, str):
        rule_codes_text = rule_codes
    else:
        raise TypeError("Invalid type for rule_codes")

    organisation_name_text = organisation_name or "Niet beschikbaar"
    algorithm_name_text = algorithm_name or "Niet beschikbaar"

    prefix = "Dit is een automatisch gegenereerd bericht."
    feedback_message = (
        f"Tijdens het gebruik van de C3PO service in het Algoritmeregister"
        f" is een fout opgetreden van het type '{type(error).__name__}'."
    )
    error_message = str(error)
    postfix = "Bekijk de logging voor meer informatie."

    plain_text_message = (
        f"{prefix}\r\n"
        f"{feedback_message}\r\n"
        f"{postfix}\r\n"
        f"Organisatienaam: {organisation_name_text}.\r\n"
        f"Algoritmenaam: {algorithm_name_text}.\r\n"
        f"Regelcode(s): {rule_codes_text}.\r\n"
    )

    html_message = f"""
        <html>
            <body>
                <p>{prefix}</p>
                <p>{feedback_message}</p>
                <p>
                    <h4>Details foutmelding</b>
                    <h5>Naam algoritme</h5>
                    <p>{algorithm_name_text}<p>
                    <h5>Naam organisatie</h5>
                    <p>{organisation_name_text}<p>
                    <h5>Regelcode(s)</h5>
                    <p>{rule_codes_text}<p>
                    <h5>Technische foutmelding</h5>
                    <code>{error_message}</code>
                </p>
                <p>{postfix}</p>
            </body>
        </html>
    """
    mailing.send_notification_mail(
        receivers=["devops@ictu.nl"],
        sender=env_settings.application_mail_address,
        subject="Fout in connectie met C3PO API",
        plain_message=plain_text_message,
        html_message=html_message,
    )


def fetch_c3po_results(body: c3po_schemas.C3poRequest) -> c3po_schemas.C3poResults:
    text_raw = strip_html(body.text)
    data = c3po_schemas.ProcessingRequestOut(
        payload=text_raw,
        org_code="ictu-devops",
        project_code="algreg",
        # This parameter does nothing for now, will be implemented in the future
        rule_codes=_LANGUAGE_CHECK_RULE_CODES,
    )
    response = post_c3po_request(data)
    response = c3po_schemas.C3poResults(rules=response.json())
    return response


def post_c3po_request(data: c3po_schemas.ProcessingRequestOut) -> httpx.Response:
    with httpx.Client() as client:
        try:
            post_response = client.post(
                f"{env_settings.c3po_url}/processing-request/batch",
                json=data,
                timeout=45,
            )

            if post_response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"C3PO_REQUEST_FAILED: {post_response.status_code}",
                )
            return post_response
        except (httpx.ConnectError, httpx.HTTPStatusError) as e:
            handle_c3po_exception(
                e,
                rule_codes=(
                    "Niet beschikbaar, regels zijn uitgevoerd in bulk. "
                    "Zie Expert Service logging voor meer info."
                ),
            )
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="EXPERT_SERVICE_CONN_ERROR",
            )
