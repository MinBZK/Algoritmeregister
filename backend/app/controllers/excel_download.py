import datetime
import io
from typing import Literal
import pandas as pd
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, status
from app import schemas
from app.repositories import AlgoritmeVersionRepository
from app.schemas.versions import create_algorithm_in_schema
from app.util.config_load import get_ttl_hash, collect_structure_data
from app.util.stringify import stringify


version_options = Literal["published", "latest"]


@lru_cache(maxsize=8)
def get_column_name_mapping(version: str) -> dict[str, str]:
    standards, _ = collect_structure_data(get_ttl_hash())

    standard = standards[version]
    mapping = {}
    for key in standard.keys():
        mapping[key] = standard[key].title
    return mapping


def get_excel_data(
    db: Session,
    lars: str | None,
    org_name: str | None,
    lang: schemas.Language,
    which_version: version_options,
) -> list[schemas.AlgoritmeVersionDownload]:
    """
    Prepare algorithm data for download.
    """
    algoritme_version_repository = AlgoritmeVersionRepository(db)
    algorithms: list[schemas.AlgoritmeVersionDB] = []

    if org_name:
        if which_version == "latest":
            algorithms = algoritme_version_repository.get_latest_by_org_by_lang(
                org_name, lang
            )
        elif which_version == "published":
            algorithms = algoritme_version_repository.get_published_by_org_by_lang(
                org_name, lang
            )
    elif lars:
        if which_version == "latest":
            algorithm = algoritme_version_repository.get_latest_by_lars_by_lang(
                lars, lang
            )
        elif which_version == "published":
            algorithm = algoritme_version_repository.get_published_by_lars_by_lang(
                lars, lang
            )
        if not algorithm:
            return []
        algorithms = [algorithm]
    else:
        if which_version == "latest":
            algorithms = algoritme_version_repository.get_latest_by_lang(lang)
        if which_version == "published":
            algorithms = algoritme_version_repository.get_published_by_lang(lang)
    return [schemas.AlgoritmeVersionDownload(**alg.dict()) for alg in algorithms]


def build_excel_doc(
    algorithms: list[schemas.AlgoritmeVersionDownload],
) -> io.BytesIO:
    dataframes: dict[str, pd.DataFrame] = {}
    for algorithm in algorithms:
        # Detect version filter based on that schema
        std = algorithm.standard_version
        if not std:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="STANDARD_VALUE_NOT_FOUND"
            )
        schema = create_algorithm_in_schema("v" + std.replace(".", "_"))
        data = schema(**algorithm.dict()).dict()

        # Remove lists from data
        stringified_data = {key: stringify(data[key]) for key in data.keys()}

        # Group DataFrames by standard_version
        if std not in dataframes:
            dataframes[std] = pd.DataFrame(stringified_data, index=[0])
        else:
            df = pd.DataFrame(stringified_data, index=[0])
            dataframes[std] = pd.concat([dataframes[std], df], ignore_index=True)

    stream = io.BytesIO()
    with pd.ExcelWriter(stream) as writer:
        for key in dataframes.keys():
            df = dataframes[key]
            df = df.rename(columns=get_column_name_mapping(key))
            df = df.replace(r"\n", "", regex=True).T
            df.to_excel(writer, sheet_name=key, index=True, header=False)
    stream.seek(0)

    return stream


def generate_excel_download(
    db: Session,
    lang: schemas.Language = schemas.Language.NLD,
    *,
    org_name: str | None = None,
    lars: str | None = None,
    which_version: version_options = "published",
):
    """
    Generates excel file. Can do so for all descriptions under and org or a single one (by lars).

    Args:
        - db (Session): SQLAlchemy Session
        - lang (Language): specified language, defaults to NLD
        *,
        - org_name (str|None): organisation name. Causes excel to be for whole organisation
        - lars (str|None): lars-code for a description. Causes excel to be for one description only.
        Either org_name or lars can be specified, never both. If neither are specified, the whole DB will be queried.
        - which_version (published|latest): Specifies whether you want the published version or the latest
        (possibly unpublished) version.
    """
    if lars and org_name:
        raise ValueError("Please enter one of two identifiers: lars | org_name")

    algorithms = get_excel_data(db, lars, org_name, lang, which_version)
    if len(algorithms) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NO_DATA_FOUND",
        )

    stream = build_excel_doc(algorithms)

    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename: str = ""
    if lars:
        filename = f"{algorithms[0].name} {timestamp}.xlsx"
    elif org_name:
        filename = (
            f"Algoritmebeschrijvingen van {algorithms[0].organization} {timestamp}.xlsx"
        )
    else:
        filename = f"Algoritmebeschrijvingen {timestamp}.xlsx"

    media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = StreamingResponse(io.BytesIO(stream.read()), media_type=media_type)
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
