from email.message import EmailMessage
from email.utils import formatdate
import uuid
import smtplib
from app.config.settings import Settings
from app.util.logger import get_logger

env_settings = Settings()
logger = get_logger(__name__)

EMAIL_DOMAIN = "<EMAIL_DOMAIN>"
CUSTOMER_ACCOUNT = "<CUSTOMER_ACCOUNT>"


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
        message_id = "AR_" + uuid.uuid4().hex[:16]
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg["Date"] = formatdate(localtime=True)
        msg.add_header("Message-ID", message_id)
        msg.set_content(plain_message)
        msg.add_alternative(
            html_message,
            subtype="html",
        )
        try:
            logger.info(f"Sending mail to {receiver}: {subject}")
            session = smtplib.SMTP(env_settings.MAIL_RELAY, 25)
            session.set_debuglevel(1)
            session.ehlo()
            session.starttls()
            session.ehlo()
            session.login(CUSTOMER_ACCOUNT, env_settings.MAIL_PASSWORD)
            session.send_message(msg, sender, receiver)
            session.quit()
            logger.info(f"Succesfully sent notification mail to: {receiver}")
        except Exception:
            logger.error(f"Failed to send notification mail to: {receiver}")
