from typing import Any
from pydantic import ValidationError


class NotAListError(Exception):
    pass


class NotValidError(Exception):
    def __init__(self, obj: Any, error: ValidationError):
        if isinstance(obj, list) and len(obj) >= 1:
            if isinstance(obj[0], dict):
                keys = ", ".join(obj[0].keys())
            else:
                keys = str(obj[0])
        elif isinstance(obj, dict):
            keys = ", ".join(list(obj.keys()))
        else:
            keys = str(obj)

        wrong_keys: list[str] = [str(e._loc) for e in error.raw_errors]  # type: ignore
        super().__init__(
            error.__str__()
            + "\n\nAvailable keys from object: "
            + keys
            + "\n\nWrong key in validation: "
            + ", ".join(wrong_keys)
        )
