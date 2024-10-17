from typing import Union
from functools import lru_cache
import os
import re
from app import schemas


@lru_cache(maxsize=1)
def get_all_output_schemas_union():
    file_names = os.listdir("app/schemas/config")
    version_pattern = re.compile(r"v\d_\d[a-z]?")
    version_names = [item[:-5] for item in file_names if version_pattern.match(item)]

    output_schemas = []
    for v in version_names:
        schema = schemas.versions.create_algorithm_schema(v)
        output_schemas.append(schema)
    schemas_union = Union[*output_schemas]  # type: ignore
    return schemas_union
