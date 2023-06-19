from pydantic import BaseModel, Field, create_model
from functools import lru_cache
import re
import enum
from datetime import datetime


class JsonSchemaProperty(BaseModel):
    title: str
    type: str
    max_length: int | None
    show_always: bool
    help_text: str
    instructions: str
    example: str | list[str]
    required: bool
    permitted_values: list[str] | None
    recommended_items: list[str] | None


class JsonSchema(BaseModel):
    properties: dict[str, JsonSchemaProperty]


class AlgorithmBase(BaseModel):
    class Config:
        orm_mode = True


def _get_versioned_name(name: str, version: str):
    model_name = version + "__" + name
    return model_name


def _get_schema_json(version: str):
    version_pattern = re.compile("v[0-9]_[0-9]_[0-9][a-z]?")
    if not version_pattern.match(version):
        raise ValueError

    file_name = f"app/schemas/config/{version}.json"
    data = JsonSchema.parse_file(file_name)
    return data


def _get_type_from_json_schema(properties: JsonSchemaProperty, key: str, version: str):
    field_type = properties.type
    if field_type == "string":
        return str
    elif field_type == "enum" or field_type == "array":
        if properties.permitted_values:
            # make key from values: Text text -> becomes: text_text
            permitted_values_dict = {
                "_".join(v.split(" ")).lower(): v for v in properties.permitted_values
            }
            # make name from key: text_text -> becomes TextText
            enum_name = "Enum" + "".join([s.capitalize() for s in key.split("_")])

            versioned_name = _get_versioned_name(enum_name, version)
            dynamic_enum = enum.Enum(versioned_name, permitted_values_dict, type=str)

            if field_type == "enum":
                return dynamic_enum
            elif field_type == "array":
                return list[dynamic_enum]
            else:
                raise ValueError
        elif properties.recommended_items:
            if field_type == "array":
                return list[str]
    else:
        raise ValueError


def _get_prop_dict(field_props: JsonSchemaProperty):
    field_dict = {
        "title": field_props.title,
        "max_length": field_props.max_length,
        "show_always": field_props.show_always,
        "help_text": field_props.help_text,
        "instructions": field_props.instructions,
        "example": field_props.example,
        "default": (...) if field_props.required else None,
        "type": field_props.type,
        "recommended_items": field_props.recommended_items,
    }

    return field_dict


def _build_schema_fields(data: JsonSchema, version: str):
    fields = {}
    for key in data.properties:
        prop_dict = _get_prop_dict(data.properties[key])
        field_props = Field(
            **prop_dict,
        )

        field_type = _get_type_from_json_schema(data.properties[key], key, version)
        fields[key] = (field_type, field_props)
    return fields


@lru_cache(maxsize=8)
def create_algorithm_in_schema(version: str):
    data = _get_schema_json(version)

    fields = _build_schema_fields(data, version)

    AlgorithmIn = create_model("AlgorithmIn", **fields, __base__=AlgorithmBase)
    return AlgorithmIn


@lru_cache(maxsize=8)
def create_algorithm_schema(version: str):
    schema_version_in = create_algorithm_in_schema(version)

    fields = {
        "lars": (str, ...),
        "create_dt": (datetime, ...),
        "released": (bool, ...),
        "published": (bool, ...),
    }

    model_name = _get_versioned_name("Algorithm", version)
    Algorithm = create_model(model_name, **fields, __base__=schema_version_in)
    return Algorithm


@lru_cache(maxsize=8)
def create_algorithm_in_loader_schema(version: str):
    schema_version_in = create_algorithm_in_schema(version)

    fields = {
        "create_dt": (datetime, Field(None)),
        "published": (bool, ...),
        "algoritme_id": (str, Field(None)),
    }

    model_name = _get_versioned_name("AlgorithmInLoader", version)
    AlgorithmInLoader = create_model(model_name, **fields, __base__=schema_version_in)
    return AlgorithmInLoader
