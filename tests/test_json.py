"""
Test the json module
"""
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from frittomisto.json import JSONSerializable

@dataclass
class TestClass1(JSONSerializable):
    """
    Test class
    """
    __test__ = False
    test_property: str


@dataclass
class TestClass2(JSONSerializable):
    """
    Test class
    """
    __test__ = False
    # Built-in types
    str_list: List[str]
    dict_dict: Dict[str, Dict[str, int]]
    opt: Optional[str]
    any: Any

    # Custom types
    test_class: TestClass1
    test_class_list: List[TestClass1]
    test_class_dict: Dict[str, TestClass1]

JSON_MIRROR = {
    # Built-in types
    "str_list": ["a", "b", "c"],
    "dict_dict": {"a": {"b": 1}, "c": {"d": 2}},
    "opt": None,
    "any": 1,

    # Custom types
    "test_class": {"test_property": "test"},
    "test_class_list": [{"test_property": "test"}],
    "test_class_dict": {"a": {"test_property": "test"}},
}


def test_json_serializable():
    """
    Test JSON serializable
    """
    c = TestClass2(**JSON_MIRROR) # type: ignore
    assert c.to_dict() == JSON_MIRROR
    assert TestClass2.from_dict(JSON_MIRROR).to_dict() == JSON_MIRROR
    