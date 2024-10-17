from functools import lru_cache
import json
import os
import re
import time
from typing import Any, Tuple
from app.schemas.config.types import SchemaProperty, SchemaJson
from app.config.layouts.types import LayoutJson


def get_ttl_hash(seconds=3600):
    """Returns a new value for each interval in `seconds`. Allows resetting of cache, giving an effective TTL of
    `seconds`"""
    return round(time.time() / seconds)


@lru_cache(maxsize=1)
def collect_structure_data(
    ttl_hash=None,
) -> Tuple[dict[str, dict[str, SchemaProperty]], dict[str, LayoutJson]]:
    del ttl_hash

    version_pattern = re.compile(r"v\d_\d[a-z]?")
    filenames = [
        item for item in os.listdir("app/schemas/config") if version_pattern.match(item)
    ]

    versions = [f[1:-5].replace("_", ".") for f in filenames]

    schemas: dict[str, dict[str, SchemaProperty]] = {}
    layouts: dict[str, LayoutJson] = {}
    for v, f in zip(versions, filenames):
        filename = f"app/schemas/config/{f}"
        with open(filename) as file:
            schema: dict[str, Any] = json.load(file)
            schemas[v] = SchemaJson(**schema).properties

        filename = f"app/config/layouts/{f}"
        with open(filename) as file:
            layout: dict[str, Any] = json.load(file)
            layouts[v] = LayoutJson(**layout)

    return schemas, layouts
