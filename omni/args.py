"""
Utilities for parsing CLI arguments
"""
from typing import Any, Union, List, Dict

# An alias for a primitive type
PrimType = Union[None, bool, int, str]

# An alias for all supported types
CliArgType = Union[PrimType, List["CliArgType"], Dict[str, "CliArgType"]]

def unraw(val: str) -> CliArgType:
    """
    Can be used to convert a raw value received as
    CLI param to a Python value.
    Here are the supported formats:
    - "" -> None
    - "foo" -> "foo"
    - "false" -> False
    - "true" -> True
    - "123" -> 123
    - "foo,bar,baz" -> ["foo", "bar", "baz"]
    - "foo:bar,baz:" -> {"foo": "bar", "baz": None}
    - "foo:bar,baz:123" -> {"foo": "bar", "baz": 123}
    - "foo:bar,baz:123,foo:bar2" -> {"foo": ["bar", "bar2"], "baz": 123}
    - "foo,bar:baz" -> ["foo", {"bar": "baz"}]
    """

    def _unraw_terminal(val: str) -> PrimType:
        val_normalized = val.strip().lower()
        if val_normalized == "":
            return None
        if val_normalized == "true":
            return True
        if val_normalized == "false":
            return False
        if val_normalized.isnumeric():
            return int(val_normalized)
        return val

    if "," not in val:
        if ":" in val:
            # If the string contains a colon, it's a dict
            k, v = val.split(":")
            return {k: unraw(v)}
        # No comma, no colon, it's a terminal value
        return _unraw_terminal(val)

    # If the string contains a comma, it's a list of entries
    val_list : List[Any] = [unraw(el) for el in val.split(",")]

    # Try building a dict, if it fails, return a list
    out = {}
    for el in val_list:
        if not isinstance(el, dict):
            # At least one element is not a dict, return a list
            return val_list

        for k, v in el.items():
            if k in out:
                # If the key already exists, append the value to a list
                if isinstance(out[k], list):
                    out[k].append(v)
                else:
                    out[k] = [out[k], v]
            else:
                out[k] = v

    return out
