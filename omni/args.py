from typing import Any


def unraw(val: str) -> Any:
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
    def _unraw_terminal(val: str) -> Any:
        if val == "":
            return None
        elif val == "true":
            return True
        elif val == "false":
            return False
        elif val.isnumeric():
            return int(val)
        else:
            return val
        
    if "," not in val:
        if ":" in val:
            k,v = val.split(":")
            return {k: unraw(v)}
        else:
            return _unraw_terminal(val)
        

    val = [unraw(el) for el in val.split(",")]
    # Try building a dict, if it fails, return a list
    out = {}
    for el in val:
        if not isinstance(el, dict):
            # At least one element is not a dict, return a list
            return val

        for k,v in el.items():
            if k in out:
                # If the key already exists, append the value to a list
                if isinstance(out[k], list):
                    out[k].append(v)
                else:
                    out[k] = [out[k], v]
            else:
                out[k] = v

    return out





