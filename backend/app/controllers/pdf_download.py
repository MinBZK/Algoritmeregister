import datetime
import io
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.misc import Language
from .pdf_wrapper import TextStyle, PDF
from app import schemas
from app.schemas.config.types import SchemaProperty
from app.config.layouts.types import LayoutJson
from app.repositories import AlgoritmeVersionRepository
from app.util.config_load import get_ttl_hash, collect_structure_data
from app.util.stringify import stringify


def get_org_data(db: Session, org_name: str) -> list[schemas.AlgoritmeVersionDownload]:
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    algorithms = algoritme_version_repository.get_latest_by_org_by_lang(
        org_name, Language.NLD
    )
    return [schemas.AlgoritmeVersionDownload(**row.dict()) for row in algorithms]


def get_algo_data(db: Session, lars: str) -> schemas.AlgoritmeVersionDownload | None:
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    algorithm = algoritme_version_repository.get_latest_by_lars_by_lang(
        lars, Language.NLD
    )
    if algorithm:
        return schemas.AlgoritmeVersionDownload(**algorithm.dict())


def build_description(
    pdf: PDF,
    algorithm: schemas.AlgoritmeVersionDownload,
    layout: LayoutJson,
    schema: dict[str, SchemaProperty],
) -> PDF:
    pdf.next_page()

    pdf.add_heading(f"{algorithm.name} ({algorithm.lars})", TextStyle.H2)
    pdf.add_paragraph(f"Publicatiestandaard: {algorithm.standard_version}")
    pdf.print_block()

    for tab_group in layout.tabsGrouping:
        pdf.add_heading(tab_group.label, TextStyle.H3)
        pdf.print_block(lower_limit=0.25)

        field_list = tab_group.rows
        for field in field_list:
            key: str = f"{algorithm.lars}__{field}"
            value: str = stringify(getattr(algorithm, field))
            if not value:
                value = ""
            max_length: int = schema[field].max_length or 1000
            pdf.add_heading(schema[field].title, TextStyle.H4)
            pdf.add_textfield(value, key, max_length=max_length)
            pdf.print_block()
    return pdf


def get_all_algorithm_pdf(db: Session, org_name: str):
    data = get_org_data(db, org_name)
    if len(data) == 0:
        return None, None

    organisation = data[0].organization
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    pdf = PDF()
    author = "Webformulier van het Algoritmeregister"
    title = f"Algoritmebeschrijvingen van {organisation}"
    subject = f"Algoritmebeschrijvingen van {organisation}"
    pdf.set_metadata(author=author, title=title, subject=subject)

    introduction: str = f"""Dit document bevat algoritmebeschrijvingen van {organisation} \
uitgedraaid op {timestamp}.\n Gebruik het om algoritmebeschrijvingen intern te reviewen \
en wijzigingen te accorderen voor publicatie \nop het algoritmeregister van de Nederlandse \
overheid. Heeft u vragen of heeft u hulp nodig? \n\
Neem via mail contact op met: algoritmeregister@minbzk.nl."""

    pdf.add_heading("Algoritmebeschrijvingen", TextStyle.H1)
    pdf.add_heading(f"Algoritmes van {organisation}", TextStyle.SUBTITLE)
    pdf.add_paragraph(introduction)
    pdf.print_block()

    schemas, layouts = collect_structure_data(get_ttl_hash())
    for algorithm in data:
        if not algorithm.standard_version:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "STANDARD_VALUE_NOT_FOUND")
        schema = schemas[algorithm.standard_version]
        layout = layouts[algorithm.standard_version]
        pdf = build_description(pdf, algorithm, layout, schema)

    pdf.save()
    stream = pdf.stream
    stream.seek(0)

    filename = f"Algoritmebeschrijvingen van {organisation} op {timestamp}.pdf"
    return stream, filename


def get_one_algorithm_pdf(db: Session, lars: str):
    algorithm = get_algo_data(db, lars)
    if not algorithm:
        return None, None

    organisation = algorithm.organization
    name = algorithm.name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    pdf = PDF()
    author = "Webformulier van het Algoritmeregister"
    title = f"Algoritmebeschrijving van {organisation}"
    subject = f"Algoritmebeschrijving van {organisation}"
    pdf.set_metadata(author=author, title=title, subject=subject)

    introduction: str = f"""Dit document bevat de algoritmebeschrijving: {name},\n \
uitgedraaid op {timestamp}. Gebruik het om de inhoud intern te reviewen  \
en wijzigingen te accorderen \n voor publicatie op het algoritmeregister van de Nederlandse  \
overheid. Heeft u vragen of heeft u hulp nodig? \n\
Neem via mail contact op met: algoritmeregister@minbzk.nl."""

    pdf.add_heading("Algoritmebeschrijvingen", TextStyle.H1)
    pdf.add_heading(f"Algoritmes van {organisation}", TextStyle.SUBTITLE)
    pdf.add_paragraph(introduction)
    pdf.print_block()

    schemas, layouts = collect_structure_data(get_ttl_hash())
    if not algorithm.standard_version:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "STANDARD_VALUE_NOT_FOUND")
    schema = schemas[algorithm.standard_version]
    layout = layouts[algorithm.standard_version]

    pdf = build_description(pdf, algorithm, layout, schema)

    pdf.save()
    stream = pdf.stream
    stream.seek(0)

    filename = f"{algorithm.name.encode('utf-8')} {timestamp}.pdf"
    return stream, filename


def generate_pdf_download(
    db: Session, *, org_name: str | None = None, lars: str | None = None
):
    if lars:
        stream, filename = get_one_algorithm_pdf(db, lars)
    elif org_name:
        stream, filename = get_all_algorithm_pdf(db, org_name)
    else:
        raise ValueError("Please enter one of two identifiers: lars | org_name")

    if stream is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No algorithm descriptions found. Unable to make document",
        )
    media_type = (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response = StreamingResponse(io.BytesIO(stream.read()), media_type=media_type)

    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


if __name__ == "__main__":
    collect_structure_data()
