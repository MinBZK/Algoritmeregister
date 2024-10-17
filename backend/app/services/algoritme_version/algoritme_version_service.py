import re
from typing import TypeVar

from app.schemas.algoritme_version import (
    AlgoritmeVersionLastEdit,
    AlgoritmeVersionQuery,
    AlgoritmeVersionDB,
)
from app.util.config_load import get_ttl_hash, collect_structure_data
from app import models


T = TypeVar("T", AlgoritmeVersionQuery, AlgoritmeVersionDB, AlgoritmeVersionLastEdit)


def convert_potential_list(field: str) -> list[str] | str:
    if not isinstance(field, str):
        return field
    # First check is to match anything like this {.....}
    pattern = r"^\{(.+)\}$"
    list_match = re.match(pattern, field)
    if not list_match:
        return field

    # # SQLAlchemy sometimes stores array entries as with double quotes, e.g. on this string:
    # # DPIA: https://google.com
    # # The space seems to create these additional quotes. This is handled by taking them away
    # # here. Because comma's can appear in the substrings, can't do a split, but regex works.
    list_entries: list[str] = re.findall(r"(\"[^\"]+\"|[^\"{},]+)", field)
    new_value: list[str] = []
    for list_entry in list_entries:
        new_value.append(list_entry.replace('"', ""))
    return new_value


def field_db_list_to_python_list(field: str) -> list[str] | str:
    return convert_potential_list(field)


def db_list_to_python_list(model: models.AlgoritmeVersion) -> models.AlgoritmeVersion:
    """Converts lists found in the SQLAlchemy model (=sql data) into python lists.

    There are certain columns which store a list of values. These columns do not have an
    enumeration type, as legacy Publication Standards did not have the enumeration restriction.
    Because of this the column has to be a free field format -- varchar.

    Still, it needs to be converted to a python format. This conversion looks as follows:

    "{a, b}" as str -> ["a", "b"] as list[str]
    """
    standards, _ = collect_structure_data(get_ttl_hash())
    schema = standards[model.standard_version]
    for c in model.__table__.columns:  # type: ignore
        # Check if the field is eligible for conversion. Don't want to convert lists where it is not allowed
        # (by Pydantic).'
        if c.key not in schema:
            continue
        if schema[c.key].type != "array":
            continue
        column_value = getattr(model, c.key)

        # Catch; if for some reason the column that should be an array is an empty string.
        if column_value == "":
            setattr(model, c.key, [])
            continue

        if column_value:
            new_value = convert_potential_list(column_value)
            setattr(model, c.key, new_value)
    return model


def db_list_to_python_list_schema(
    schema: T,
) -> T:
    """Converts lists found in the SQLAlchemy model (=sql data) into python lists.

    There are certain columns which store a list of values. These columns do not have an
    enumeration type, as legacy Publication Standards did not have the enumeration restriction.
    Because of this the column has to be a free field format -- varchar.

    Still, it needs to be converted to a python format. This conversion looks as follows:

    "{a, b}" as str -> ["a", "b"] as list[str]
    """
    if not schema.standard_version:
        return schema

    standards, _ = collect_structure_data(get_ttl_hash())
    standard = standards[schema.standard_version]
    for c in dict(schema).keys():  # type: ignore
        # Check if the field is eligible for conversion. Don't want to convert lists where it is not allowed
        # (by Pydantic).'
        if c not in standard:
            continue
        if standard[c].type != "array":
            continue
        column_value = getattr(schema, c)
        if column_value:
            new_value = convert_potential_list(column_value)
            setattr(schema, c, new_value)
    return schema
