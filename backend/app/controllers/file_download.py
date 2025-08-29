import datetime
import html
import io
import csv
from typing import Any, Literal
import pandas as pd
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from fastapi import HTTPException, status
from app import schemas
from app.repositories import AlgoritmeVersionRepository
from app.schemas.misc import Language
from app.schemas.versions import create_algorithm_in_schema
from app.util.config_load import get_ttl_hash, collect_structure_data
from app.util.stringify import stringify


version_options = Literal["published", "latest", "published_history"]


@lru_cache(maxsize=8)
def get_column_name_mapping(version: str) -> dict[str, str]:
    standards, _ = collect_structure_data(get_ttl_hash())

    standard = standards[version]
    mapping = {}
    for key in standard.keys():
        mapping[key] = standard[key].title
    return mapping


def get_download_data(
    db: Session,
    lars: str | None,
    org_name: str | None,
    lang: Language,
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
        elif which_version == "published_history":
            algorithm_list = (
                algoritme_version_repository.get_all_published_versions_by_lars_by_lang(
                    lars, lang
                )
            )
            return [
                schemas.AlgoritmeVersionDownload(**alg.model_dump())
                for alg in algorithm_list
            ]
        if not algorithm:
            return []
        algorithms = [algorithm]
    else:
        if which_version == "latest":
            algorithms = algoritme_version_repository.get_latest_by_lang(lang)
        if which_version == "published":
            algorithms = algoritme_version_repository.get_published_by_lang(lang)
        if which_version == "published_history":
            algorithm_list = (
                algoritme_version_repository.get_all_published_versions_by_lang(lang)
            )
            return [
                schemas.AlgoritmeVersionDownload(**alg.model_dump())
                for alg in algorithm_list
            ]
    return [schemas.AlgoritmeVersionDownload(**alg.model_dump()) for alg in algorithms]


def generate_download_stream(
    algorithms: list[schemas.AlgoritmeVersionDownload],
    lang: Language,
    file_type: Literal["excel", "csv"] = "excel",
) -> io.BytesIO:
    dataframes: dict[str, pd.DataFrame] = {}
    for algorithm in algorithms:
        # Detect version filter based on that schema
        std = algorithm.standard_version
        if not std:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="STANDARD_VALUE_NOT_FOUND"
            )

        # Remove lists from data, and remove unused fields for this schema
        schema = create_algorithm_in_schema("v" + std.replace(".", "_"))
        data: dict[str, Any] = dict(algorithm)
        stringified_data = {
            key: stringify(data[key])
            for key in data.keys()
            if key in schema.model_fields.keys()
        }

        # Group DataFrames by standard_version
        if std not in dataframes:
            dataframes[std] = pd.DataFrame(stringified_data, index=[0])
        else:
            df = pd.DataFrame(stringified_data, index=[0])
            dataframes[std] = pd.concat([dataframes[std], df], ignore_index=True)

    stream = io.BytesIO()
    if file_type == "excel":
        with pd.ExcelWriter(stream) as writer:
            for key in sorted(dataframes.keys(), reverse=True):
                df = dataframes[key]
                if lang == Language.NLD:
                    df = df.rename(columns=get_column_name_mapping(key))
                df = df.replace(r"\n", "", regex=True).T
                df = df.replace(r"<[^<>]*>", "", regex=True)
                df.to_excel(writer, sheet_name=key, index=True, header=False)
    elif file_type == "csv":
        # concat the dataframed vertically and write to stream
        df = pd.concat(dataframes.values(), ignore_index=True)
        df = df.replace(r"\r?\n", " ", regex=True)
        df = df.replace(r"<[^<>]*>", "", regex=True)
        df = df.rename(columns={"lars": "algorithm_id"})
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].apply(
                lambda x: html.unescape(x) if isinstance(x, str) else x
            )
        # write to stream
        df.to_csv(
            stream,
            index=False,
            header=True,
            sep=",",
            encoding="utf-8-sig",
            quoting=csv.QUOTE_ALL,
        )

    stream.seek(0)

    return stream


def generate_download_file(
    db: Session,
    lang: Language = Language.NLD,
    *,
    org_name: str | None = None,
    lars: str | None = None,
    which_version: version_options = "published",
    file_type: Literal["excel", "csv"] = "excel",
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
        - which_version (published|latest|published_history): Specifies whether you want the published version,
        the latest (possibly unpublished) version or all published versions (history) of the algorithm.
    """
    if lars and org_name:
        raise ValueError("Please enter one of two identifiers: lars | org_name")

    algorithms = get_download_data(db, lars, org_name, lang, which_version)
    if len(algorithms) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NO_DATA_FOUND",
        )
    stream = generate_download_stream(algorithms, lang=lang, file_type=file_type)

    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    filename: str = ""
    file_extension = "xlsx" if file_type == "excel" else "csv"
    if lars:
        name = algorithms[0].name or "Onbekend"
        filename = f"{name.encode('utf-8')} {timestamp}.{file_extension}"
    elif org_name:
        filename = f"Algoritmebeschrijvingen van {algorithms[0].organization} {timestamp}.{file_extension}"
    else:
        filename = f"Algoritmebeschrijvingen {timestamp}.{file_extension}"

    if file_type == "csv":
        media_type = "text/csv"
    else:
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    response = StreamingResponse(io.BytesIO(stream.read()), media_type=media_type)
    response.headers[
        "Content-Disposition"
    ] = f'attachment; filename="{filename}"'  # noqa: E702
    return response
