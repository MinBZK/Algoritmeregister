from email.message import EmailMessage
import smtplib
import logging
from app.config.settings import Settings

env_settings = Settings()
logger = logging.getLogger(__name__)


EMAIL_DOMAIN = "@i8s.nl"


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
    if not sender or not sender.endswith(EMAIL_DOMAIN):
        logger.info(
            "Cannot send email since no or incorrect sender mail address is configured."
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
        logger.info(f"Sending mail to {receiver}")
        session = smtplib.SMTP("mail-relay-algoritmeregister")
        session.send_message(msg, sender, receiver)
        session.quit()
        logger.info(f"Succesfully sent notification mail to: {', '.join(receiver)}")
