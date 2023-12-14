import pytz
from fastapi import Depends
from sqlalchemy import text
from datetime import datetime
from app.config.settings import Settings
from app import middleware, mailing, models, schemas

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

    editor_name_query: models.ActionHistory = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.algoritme_version_id == algoritme_version.id)
        .order_by(models.ActionHistory.create_dt.desc())
        .first()
    )
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

    print(subject)
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


def handle_retract_mail(lars: str, db=Depends(middleware.get_db)):
    algoritme_version: models.AlgoritmeVersion = (
        db.query(models.AlgoritmeVersion)
        .filter(
            models.AlgoritmeVersion.lars == lars,
            models.AlgoritmeVersion.language == schemas.Language.NLD,
        )
        .order_by(models.AlgoritmeVersion.create_dt.desc())
        .first()
    )

    editor_name_query: models.ActionHistory = (
        db.query(models.ActionHistory)
        .filter(models.ActionHistory.algoritme_version_id == algoritme_version.id)
        .order_by(models.ActionHistory.create_dt.desc())
        .first()
    )
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
