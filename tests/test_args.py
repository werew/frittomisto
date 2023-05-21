import pytest
from omni.args import unraw

def test_unraw():
    """
    Test the unraw function
    """
    assert unraw("") == None
    assert unraw("foo") == "foo"
    assert unraw("true") == True
    assert unraw("false") == False
    assert unraw("123") == 123
    assert unraw("foo,bar,baz") == ["foo", "bar", "baz"]
    assert unraw("foo:bar,baz:") == {"foo": "bar", "baz": None}
    assert unraw("foo:bar,baz:123") == {"foo": "bar", "baz": 123}
    assert unraw("foo:bar,baz:123,foo:bar2") == {"foo": ["bar", "bar2"], "baz": 123}
    assert unraw("foo,bar:baz") == ["foo", {"bar": "baz"}]