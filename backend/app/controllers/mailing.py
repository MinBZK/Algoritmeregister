# flake8: noqa: E221
import pytz
from fastapi import Depends, HTTPException
from sqlalchemy import text
from datetime import datetime
from app.config.settings import Settings
from app import mailing, models
from app.middleware.middleware import get_db
from app.schemas.action import EmailType
from app.schemas.misc import Language
from sqlalchemy.orm import Session
from app.util.logger import get_logger

logger = get_logger(__name__)
env_settings = Settings()

DEFAULT_SENDER = env_settings.application_mail_address
WEBFORM_URL = env_settings.webform_url


def send_email(
    db: Session,
    email_type: EmailType,
    lars: str | None = None,
) -> None:
    match email_type:
        case EmailType.RELEASE_SELF_PUBLISH_TWO:
            raise NotImplementedError("Not yet implemented")
        case EmailType.RELEASE_ICTU_LAST:
            if lars is None:
                raise HTTPException(500)
            handle_release_mail(lars, db)
        case EmailType.RETRACT:
            if lars is None:
                raise HTTPException(500)
            handle_retract_mail(lars, db)


def handle_release_mail(lars: str, db: Session = Depends(get_db)):
    algoritme_version: models.Algoritme = (
        db.query(models.AlgoritmeVersion)
        .join(models.Algoritme)
        .filter(models.Algoritme.lars == lars)
        .order_by(models.AlgoritmeVersion.create_dt.desc())
        .first()
    )
    if not algoritme_version:
        logger.error(f"No algorithm found with lars {lars}. Mail not sent")
        return

    editor_name_query: models.ActionHistory = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.algoritme_version_id == algoritme_version.id)
        .order_by(models.ActionHistory.create_dt.desc())
        .first()
    )
    if not editor_name_query:
        logger.error(
            f"Last edit of algoritme_version {algoritme_version.id} not found. Mail not sent"
        )
        return

    editor_name = editor_name_query.user_id

    previous_publication_count = db.execute(
        text(
            """ select count(*)
        from action_history h
        inner join algoritme_version v on v.id = h.algoritme_version_id
        inner join algoritme a on a.id = v.algoritme_id
        where
        h.operation = 'published'
        and a.lars = :lars
        ;"""
        ),
        {"lars": algoritme_version.lars},
    )
    if previous_publication_count.scalar() == 0:
        subject = f"Vrijgave voor eerste publicatie: {algoritme_version.name}"
        first_publication_addendum = (
            "<p> Deze beschrijving is nog niet eerder gepubliceerd. </p>"
        )
    else:
        subject = f"Vrijgave voor publicatie: {algoritme_version.name}"
        first_publication_addendum = ""

    webform_link = f"{WEBFORM_URL}/algoritme/{algoritme_version.lars}/bewerken"

    time = datetime.time(
        datetime.now().astimezone(pytz.timezone("Europe/Amsterdam"))
    ).strftime("%H:%M")

    receivers = ["devops@ictu.nl"]
    sender = DEFAULT_SENDER

    plain_message = f"""Beste beheerder, Er is een nieuw algoritme vrijgegeven
      van de organisatie {algoritme_version.organization}."""
    html_message = f"""
        <html>
            <body>
                <p>
                    Een nieuwe versie van algoritmebeschrijving {algoritme_version.name} [{algoritme_version.lars}] is
                    door {editor_name} van {algoritme_version.organization}, 
                    op {datetime.date(datetime.now())} om {time}
                    vrijgegeven voor publicatie.
                </p>
                <p> Gelieve deze beschrijving te reviewen en bij goedkeuring te
                publiceren via <a href="{webform_link}"> deze link </a>. </p>
                <p> Gelieve bij afkeuring contact op te nemen met de algoritmehouder om af te stemmen welke aanpassing
                nodig is. </p>

                {first_publication_addendum}

                <p> Dit is een automatisch bericht. </p>
            </body>
        </html>
        """

    mailing.send_notification_mail(
        receivers=receivers,
        sender=sender,
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
    )


def handle_retract_mail(lars: str, db: Session = Depends(get_db)):
    algoritme_version: models.AlgoritmeVersion = (
        db.query(models.AlgoritmeVersion)
        .join(models.Algoritme)
        .filter(
            models.Algoritme.lars == lars,
            models.AlgoritmeVersion.language == Language.NLD,
        )
        .order_by(models.AlgoritmeVersion.create_dt.desc())
        .first()
    )
    if not algoritme_version:
        logger.error("Algoritme_version not found. Retract mail not sent.")
        return

    editor_name_query: models.ActionHistory = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.algoritme_version_id == algoritme_version.id)
        .order_by(models.ActionHistory.create_dt.desc())
        .first()
    )
    if not editor_name_query:
        logger.error("Last edit of algoritme_version not found. Mail not sent.")
        return

    editor_name = editor_name_query.user_id

    time = datetime.time(
        datetime.now().astimezone(pytz.timezone("Europe/Amsterdam"))
    ).strftime("%H:%M")

    receivers = ["devops@ictu.nl"]
    sender = DEFAULT_SENDER
    subject = f"Ingetrokken: {algoritme_version.name}"
    plain_message = f"""Beste beheerder, Er is een algoritme ingetrokken
      van de organisatie {algoritme_version.organization}."""
    html_message = f"""
        <html>
            <body>
                <p>
                    Een algoritmebeschrijving: {algoritme_version.name} [{algoritme_version.lars}] is
                    door {editor_name} van {algoritme_version.organization}, op {datetime.date(datetime.now())} om
                      {time} ingetrokken.
                </p>

                <p> Dit is een automatisch bericht. </p>
            </body>
        </html>
        """

    mailing.send_notification_mail(
        receivers=receivers,
        sender=sender,
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
    )
