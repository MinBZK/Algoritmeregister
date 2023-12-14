from pydantic import BaseModel, create_model
from typing import Union
from functools import lru_cache
from sqlalchemy import JSON, Integer, Boolean, VARCHAR, DateTime
from datetime import datetime
import os
import re
from app import schemas, models


class ExportBase(BaseModel):
    class Config:
        orm_mode = True


def _translate_type(type_class):
    if isinstance(type_class, VARCHAR):
        return str
    elif isinstance(type_class, Boolean):
        return bool
    elif isinstance(type_class, Integer):
        return int
    elif isinstance(type_class, DateTime):
        return datetime
    elif isinstance(type_class, JSON):
        return list[dict]
    else:
        raise TypeError(type_class)


@lru_cache(maxsize=2)
def get_algorithm_export_schema(truncated: bool):
    columns = models.AlgoritmeVersion.__table__.columns

    always_ignore = [
        "id",
        "algoritme_id",
        "preview_active",
        "language",
        "vector",
    ]
    ignore_on_trunc = ["create_dt", "published", "released"]
    fields = {}
    for c in columns:
        if c.key in always_ignore:
            continue
        if c.key in ignore_on_trunc and truncated:
            continue
        fields[c.key] = (_translate_type(c.type), None)
    fields["lars"] = (str, ...)

    if not truncated:
        fields["owner"] = (str, ...)

    prefix = "truncated__" if truncated else ""
    schema = create_model(prefix + "AlgoritmeInDB", **fields, __base__=ExportBase)
    return schema


@lru_cache(maxsize=1)
def get_all_output_schemas_union():
    file_names = os.listdir("app/schemas/config")
    version_pattern = re.compile(r"v\d_\d_\d[a-z]?")
    version_names = [item[:-5] for item in file_names if version_pattern.match(item)]

    output_schemas = []
    for v in version_names:
        schema = schemas.versions.create_algorithm_schema(v)
        output_schemas.append(schema)
    schemas_union = Union[*output_schemas]  # type: ignore
    return schemas_union
