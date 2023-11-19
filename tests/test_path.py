"""
Test path utilities
"""
from pathlib import Path
from typing import Optional
import pytest
from frittomisto.path import cd, sanitize_path


def test_cd():
    """
    Test cd
    """
    old_dir = Path.cwd()
    with cd(".."):
        assert Path.cwd() == old_dir.parent
    assert Path.cwd() == old_dir

# A set of tests for sanitize_path
# Each test is a tuple of (path, allowed_dir, expected)
# The expected value is the expected return value of sanitize_path
# if expected is None, then sanitize_path is expected to raise a ValueError
PATH_TESTS = [
    ("foo", "bar", None),
    ("foo/bar", "foo/bar/baz", None),
    ("foo/bar", "foo/bar/baz/", None),
    ("foo/bar", "foo/baz", None),
    ("foo/bar", "foo/baz/", None),
    ("foo/bar", "baz", None),
    ("foo/bar", "baz/", None),
    ("foo/bar", "/foo", None),
    ("foo/bar", "/foo/", None),
    ("foo/bar", "/foo/bar", None),
    ("foo/bar", "/foo/bar/", None),
    ("foo/bar", "/foo/bar/baz", None),
    ("foo/bar", "/foo/bar/baz/", None),
    ("../../../../../..", "foo", None),
    ("../../../../../..", "foo/", None),
    ("../../../../../..", "foo/bar", None),
    ("../../../../../..", "foo/bar/", None),
    ("/foo/.././", "/foo/..", "/"),
    ("/foo/./../", "/foo/", None),
    ("/foo//////../", "/foo/", None),
    ("/foo", "/foo", "/foo"),
    ("/foo/bar", "/foo", "/foo/bar"),
    ("/foo/bar", "/foo/", "/foo/bar"),
    ("/foo/bar", "/foo/bar", "/foo/bar"),
    ("/foo/bar", "/foo/bar/", "/foo/bar"),
    ("/foo/bar/baz", "/foo/bar", "/foo/bar/baz"),
    ("/foo/bar/../baz", "/foo/baz", "/foo/baz"),
]

@pytest.mark.parametrize("path,allowed_dir,expected", PATH_TESTS)
def test_sanitize_path(path: str, allowed_dir: str, expected: Optional[str]) -> None:
    """
    Test sanitize_path
    """
    if expected is None:
        with pytest.raises(ValueError):
            sanitize_path(path, allowed_dir)
    else:
        assert sanitize_path(path, allowed_dir) == expected
