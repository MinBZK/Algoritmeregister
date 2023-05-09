from pydantic import BaseModel, create_model
from typing import Union
from functools import lru_cache
from sqlalchemy import Integer, Boolean, VARCHAR, DateTime
from datetime import datetime
import os
from app import schemas, models


class ExportBase(BaseModel):
    class Config:
        orm_mode = True


def _translate_type(type_class):
    if type(type_class) == VARCHAR:
        return str
    elif type(type_class) == Boolean:
        return bool
    elif type(type_class) == Integer:
        return int
    elif type(type_class) == DateTime:
        return datetime
    else:
        raise TypeError


@lru_cache(maxsize=2)
def get_algorithm_export_schema(truncated: bool):
    columns = models.AlgoritmeVersion.__table__.columns

    always_ignore = [
        "id",
        "algoritme_id",
        "preview_active",
    ]
    ignore_on_trunc = [
        "create_dt",
        "published",
        "released",
    ]
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
        fields["leverancier_id"] = (str, None)

    prefix = "truncated__" if truncated else ""
    schema = create_model(prefix + "AlgoritmeInDB", **fields, __base__=ExportBase)
    return schema


def get_all_output_schemas_union():
    file_names = os.listdir(os.path.dirname(schemas.__file__) + "/config")
    version_names = [f.replace(".json", "") for f in file_names]

    output_schemas = []
    for v in version_names:
        schema = schemas.versions.create_algorithm_schema(v)
        output_schemas.append(schema)
    schemas_union = Union[*output_schemas]  # type: ignore
    return schemas_union
