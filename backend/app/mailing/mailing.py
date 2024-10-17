from email.message import EmailMessage
import smtplib
from app.config.settings import Settings
from app.util.logger import get_logger

env_settings = Settings()
logger = get_logger(__name__)

EMAIL_DOMAIN = "<EMAIL_DOMAIN>"


def send_notification_mail(
    receivers: list[str],
    sender: str,
    subject: str,
    plain_message: str,
    html_message: str,
) -> None:
    """
    Sends a notification mail individually to all receivers.
    """
    if not env_settings.send_emails:
        logger.info(
            "Sending emails is disabled for this environment, email sending aborted."
        )
        return
    if not sender.endswith(EMAIL_DOMAIN):
        logger.error(
            "Cannot send email since incorrect sender mail address is configured."
        )
        return

    for receiver in receivers:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(plain_message)
        msg.add_alternative(
            html_message,
            subtype="html",
        )
        try:
            logger.info(f"Sending mail to {receiver}: {subject}")
            session = smtplib.SMTP("mail-relay-algoritmeregister")
            session.send_message(msg, sender, receiver)
            session.quit()
            logger.info(f"Succesfully sent notification mail to: {receiver}")
        except Exception:
            logger.error(f"Failed to send notification mail to: {receiver}")
