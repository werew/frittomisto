"""
Tests for the url module
"""
from frittomisto.url import extract_urls

VALID_URLS = [
    "http://example.com",
    "https://example.com",
    "http://example.com/foo",
    "https://example.com/foo",
    "http://example.com/foo/bar",
    "https://example.com/foo/bar",
    "http://example.com/foo/bar?baz=qux",
    "https://example.com/foo/bar?baz=qux",
    "http://example.com/foo/bar?baz=qux&quux=quuz",
    "https://example.com/foo/bar?baz=qux&quux=quuz",
    "http://example.com/foo/bar?baz=qux&quux=quuz#corge",
    "https://example.com/foo/bar?baz=qux&quux=quuz#corge",
    "http://example.com:8080",
    "https://example.com:8080",
    "http://example.com:8080/foo",
    "https://example.com:8080/foo",
    "https://example.com:8080/foo.bar",
    "git://example.com/foo",
    "git://example.com/foo/bar",
    "scp://example.com/foo",
]

INVALID_URLS = [
    "example.com",
    "example.com/foo",
    "lol://example.com",
    "lol://example.com/foo",
]


def test_extract_urls() -> None:
    """
    Test extract_urls
    """
    text = " ".join(VALID_URLS) + " " + " ".join(INVALID_URLS)
    urls = extract_urls(text)
    assert len(urls) == len(VALID_URLS)
    for url in urls:
        assert url.geturl() in VALID_URLS