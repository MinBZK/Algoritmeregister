from typing import Any
from enum import Enum


def stringify(value: Any) -> str | None:
    # Handles list[str] | list[dict] | number | str
    if not value:
        return None
    if isinstance(value, list):
        if len(value) == 0:
            return None
        if isinstance(value[0], Enum):
            return ", ".join([str(v.value) for v in value])
        if isinstance(value[0], str):
            return ", ".join(list[str](value))
        elif isinstance(value[0], dict):
            listified_dicts = []
            for n, cell in enumerate(list[dict](value)):
                stringified_dict = ", ".join(filter(None, cell.values()))
                listified_dicts.append(f"{n+1}: {stringified_dict}")
            return ". ".join(listified_dicts)
    if isinstance(value, Enum):
        return str(value.value)

    return str(value)
