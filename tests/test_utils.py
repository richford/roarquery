"""Test cases for the utils module."""
from roarquery.utils import bytes2json
from roarquery.utils import camel_case
from roarquery.utils import drop_empty
from roarquery.utils import page_results
from roarquery.utils import trim_doc_path


def test_bytes2json() -> None:
    """It exits with a status code of zero."""
    input_singleton = (
        b'[{"ID": "1", "Data": {"a": "b"}, "Path": "prod/roar-prod", '
        b'"CreateTime": "2020-04-01T00:00:00Z", '
        b'"ReadTime": "2020-04-01T00:00:00Z", '
        b'"UpdateTime": "2020-04-01T00:00:00Z"}]'
    )

    output_singleton = [
        {
            "ID": "1",
            "Data": {"a": "b"},
            "Path": "prod/roar-prod",
            "CreateTime": "2020-04-01T00:00:00Z",
            "ReadTime": "2020-04-01T00:00:00Z",
            "UpdateTime": "2020-04-01T00:00:00Z",
        }
    ]

    input_pair = (
        b'[{"ID": "1", "Data": {"a": "b"}, "Path": "prod/roar-prod", '
        b'"CreateTime": "2020-04-01T00:00:00Z", '
        b'"ReadTime": "2020-04-01T00:00:00Z", '
        b'"UpdateTime": "2020-04-01T00:00:00Z"}, '
        b'{"ID": "2", "Data": {"c": "d"}, "Path": "prod/roar-prod", '
        b'"CreateTime": "2020-04-02T00:00:00Z", '
        b'"ReadTime": "2020-04-02T00:00:00Z", '
        b'"UpdateTime": "2020-04-02T00:00:00Z"}]'
    )

    output_pair = [
        {
            "ID": "1",
            "Data": {"a": "b"},
            "Path": "prod/roar-prod",
            "CreateTime": "2020-04-01T00:00:00Z",
            "ReadTime": "2020-04-01T00:00:00Z",
            "UpdateTime": "2020-04-01T00:00:00Z",
        },
        {
            "ID": "2",
            "Data": {"c": "d"},
            "Path": "prod/roar-prod",
            "CreateTime": "2020-04-02T00:00:00Z",
            "ReadTime": "2020-04-02T00:00:00Z",
            "UpdateTime": "2020-04-02T00:00:00Z",
        },
    ]

    assert bytes2json(input_singleton) == output_singleton
    assert bytes2json(input_pair) == output_pair
    assert bytes2json(b"") == []


def test_camel_case() -> None:
    """It converts a string to camel case."""
    assert camel_case("foo_bar") == "fooBar"
    assert camel_case("foo_bar_baz") == "fooBarBaz"
    assert camel_case("foo-bar_baz") == "fooBarBaz"
    assert camel_case("foo-bar-baz") == "fooBarBaz"


def test_drop_empty() -> None:
    """It drops empty strings from a list."""
    assert drop_empty(["", "a", "", "b"]) == ["a", "b"]


def test_page_results() -> None:
    """It returns the results of a query."""
    pass


def test_trim_doc_path() -> None:
    """It removes leading project information from a firestore document path."""
    assert (
        trim_doc_path("projects/proj-id/databases/(default)/documents/prod/roar-prod")
        == "prod/roar-prod"
    )
