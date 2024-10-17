import httpx
from pydantic import BaseModel, Field, create_model, validator
from functools import lru_cache
import re
import enum
from datetime import datetime
from app.middleware.authorisation.schemas import State
from app.util.logger import get_logger
from app.schemas.config.types import SchemaJson, SchemaProperty
from . import Language
from app.util.html import strip_html, sanitize_string_fields
from .c3po.reponse_in import SeverityLevel
from app.config.settings import Settings
from app.services.c3po import handle_c3po_exception

logger = get_logger(__name__)
env_settings = Settings()


class AlgorithmBase(BaseModel):
    class Config:
        orm_mode = True


def validate_max_length(cls, value, **kwargs):
    if not isinstance(value, str):
        return value

    field_name = kwargs["field"].name
    max_length = cls.__fields__[field_name].field_info.extra.get(
        "max_length_without_html"
    )
    if not max_length:
        return value

    if len(strip_html(value)) > max_length:
        raise ValueError(
            f"{field_name} exceeds the maximum length of {max_length} characters."
        )
    return value


def apply_c3po_rules(cls, value, **kwargs):
    if not isinstance(value, str) or not value:
        return value

    field_name = kwargs["field"].name
    if field_name not in cls.__fields__:
        return value

    rule_code = "BROKEN_LINKS"
    notify_critical_finding = False
    try:
        validation_results = httpx.Client().post(
            f"{env_settings.c3po_url}/processing-request/",
            json={
                "payload": value,
                "rule_code": rule_code,
            },
        )
        validation_results.raise_for_status()
        rule_result = validation_results.json()["tasks"][0]
        notify_critical_finding = (
            rule_result["rule"]["severity_level"] == SeverityLevel.ERROR
            and rule_result["passed"] is False
        )
    except (httpx.ConnectError, httpx.HTTPStatusError) as e:
        handle_c3po_exception(e, rule_code)

    if notify_critical_finding:
        raise ValueError(
            f"One or more writing assistance checks failed with severity level "
            f"'{SeverityLevel.ERROR}'."
        )
    return value


def _get_versioned_name(name: str, version: str):
    model_name = version + "__" + name
    return model_name


def _get_schema_json(version: str):
    version_pattern = re.compile(r"v\d_\d[a-z]?")
    if not version_pattern.match(version):
        raise ValueError(
            f"_get_schema_json: version {version} does not match version_pattern. It checks for v\\d_\\d_\\d[a-z]?"
        )

    file_name = f"app/schemas/config/{version}.json"
    data = SchemaJson.parse_file(file_name)
    return data


def _get_type_from_json_schema(properties: SchemaProperty, key: str, version: str):
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
                raise ValueError(field_type)
        elif properties.recommended_items and field_type == "array":
            return list[str]
        elif properties.items:
            # Enter recursion, there is an object within an object.
            sub_properties = properties.items
            fields = _build_schema_fields(
                SchemaJson(properties=sub_properties), version
            )
            sub_schema_name = "Object" + "".join(
                [s.capitalize() for s in key.split("_")]
            )
            sub_schema = create_model(
                _get_versioned_name(sub_schema_name, version),
                **fields,
                __base__=AlgorithmBase,
            )
            return list[sub_schema]
    else:
        raise ValueError(field_type)


def _get_prop_dict(field_props: SchemaProperty):
    field_dict = {
        "title": field_props.title,
        "max_length_without_html": field_props.max_length,
        "max_items": field_props.max_items,
        "show_always": field_props.show_always,
        "help_text": field_props.help_text,
        "instructions": field_props.instructions,
        "example": field_props.example,
        "default": (...) if field_props.required else None,
        "type": field_props.type,
        "recommended_items": field_props.recommended_items,
        "allowed_html_tags": field_props.allowed_html_tags,
    }

    return field_dict


def _build_schema_fields(data: SchemaJson, version: str):
    fields = {}
    for key in data.properties:
        prop_dict = _get_prop_dict(data.properties[key])
        field_props = Field(**prop_dict)
        field_type = _get_type_from_json_schema(data.properties[key], key, version)
        fields[key] = (field_type, field_props)
    return fields


def _get_algorithm_in_validators(schema: type[AlgorithmBase]):
    validators = {}
    max_length_fields = []
    string_fields = []
    for value in schema.__fields__.values():
        if value.type_ == str:
            string_fields.append(value.name)

        add_max_length_validator = value.field_info.extra.get("max_length_without_html")
        if add_max_length_validator:
            max_length_fields.append(value.name)

    if len(max_length_fields) > 0:
        validators["max_length_validator"] = validator(
            *max_length_fields, allow_reuse=True
        )(validate_max_length)

    if len(string_fields) > 0:
        validators["html_validator"] = validator(
            *string_fields, pre=True, allow_reuse=True
        )(sanitize_string_fields)
        if env_settings.use_c3po:
            validators["c3po_validator"] = validator(
                *string_fields, pre=True, allow_reuse=True
            )(apply_c3po_rules)

    return validators


@lru_cache(maxsize=8)
def create_algorithm_base_schema(version: str):
    """Expected version format: v0_1"""
    data = _get_schema_json(version)
    fields = _build_schema_fields(data, version)

    schema_algorithm_base = create_model(
        "AlgorithmBase",
        **fields,
        __base__=AlgorithmBase,
    )
    return schema_algorithm_base


@lru_cache(maxsize=8)
def create_algorithm_in_schema(version: str):
    """Expected version format: v0_1"""
    base = create_algorithm_base_schema(version)
    validators = _get_algorithm_in_validators(base)

    schema_algorithm_in = create_model(
        "AlgorithmIn",
        __base__=base,
        __validators__=validators,
    )
    return schema_algorithm_in


@lru_cache(maxsize=8)
def create_algorithm_schema(version: str):
    """Expected version format: v0_1"""
    base = create_algorithm_base_schema(version)

    fields = {
        "lars": (str, ...),
        "create_dt": (datetime, ...),
        "language": (Language, ...),
        "state": (State, ...),
    }

    model_name = _get_versioned_name("Algorithm", version)
    algorithm = create_model(model_name, **fields, __base__=base)
    return algorithm
