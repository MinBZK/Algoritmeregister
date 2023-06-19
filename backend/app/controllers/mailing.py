from fastapi import Depends
from app import middleware, mailing, models
from app.config.settings import Settings
from datetime import datetime
import pytz

env_settings = Settings()

DEFAULT_SENDER = env_settings.application_mail_address
WEBFORM_URL = env_settings.webform_url


def handle_release_mail(lars: str, db=Depends(middleware.get_db)):
    algoritme_version: models.Algoritme = (
        db.query(models.AlgoritmeVersion)
        .filter(models.AlgoritmeVersion.lars == lars)
        .order_by(models.AlgoritmeVersion.create_dt.desc())
        .first()
    )

    webform_link = f"{WEBFORM_URL}/algoritme/{algoritme_version.lars}/bewerken"

    time = datetime.time(
        datetime.now().astimezone(pytz.timezone("Europe/Amsterdam"))
    ).strftime("%H:%M")

    receivers = ["devops@ictu.nl"]
    sender = DEFAULT_SENDER
    subject = f"Vrijgave algoritme: {algoritme_version.name}"
    plain_message = f"""Beste beheerder, Er is een nieuw algoritme vrijgegeven
      van de organisatie {algoritme_version.organization}."""
    html_message = f"""
        <html>
            <body>
                <p>
                    Een nieuwe versie van algoritmebeschrijving {algoritme_version.name} [{algoritme_version.lars}] is
                    op {datetime.date(datetime.now())} om {time} vrijgegeven voor publicatie.
                </p>
                <p> Gelieve deze beschrijving te reviewen en bij goedkeuring te
                publiceren via <a href="{webform_link}"> deze link </a>. </p>
                <p> Gelieve bij afkeuring contact op te nemen met de algoritmehouder om af te stemmen welke aanpassing
                nodig is. </p>

                <p> Dit is een automatisch bericht. </p>
            </body>
        </html>
        """

    mailing.send_release_notification_mail(
        receivers=receivers,
        sender=sender,
        subject=subject,
        plain_message=plain_message,
        html_message=html_message,
    )
