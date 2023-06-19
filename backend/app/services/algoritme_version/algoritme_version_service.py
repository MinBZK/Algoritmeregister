import re


def db_list_to_python_list(model):
    """Converts lists found in the SQLAlchemy model (=sql data) into python lists.

    There are certain columns which store a list of values. These columns do not have an
    enumeration type, as legacy Publication Standards did not have the enumeration restriction.
    Because of this the column has to be a free field format -- varchar.

    Still, it needs to be converted to a python format. This conversion looks as follows:

    "{a, b}" as str -> ["a", "b"] as list[str]
    """
    pattern = r"^\{([^{}]+)\}$"
    for c in model.__table__.columns:
        column_value = str(getattr(model, c.key))
        list_match = re.match(pattern, column_value)
        if list_match:
            new_value = list_match.group(1).split(",")

            # SQLAlchemy sometimes stores array entries as with double quotes, e.g. on this string:
            # DPIA: https://google.com
            # The space seems to create these additional quotes. This is handled by taking them away
            # here.
            quote_pattern = r"^\"([^\"]+)\"$"
            for i, v in enumerate(new_value):
                quote_match = re.match(quote_pattern, v)
                if quote_match:
                    new_value[i] = quote_match.group(1)

            setattr(model, c.key, new_value)
    return model
