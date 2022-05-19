"""Test cases for the utils module."""
from typing import Optional
from unittest.mock import Mock
from unittest.mock import patch

import pytest

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


def test_trim_doc_path() -> None:
    """It removes leading project information from a firestore document path."""
    assert (
        trim_doc_path("projects/proj-id/databases/(default)/documents/prod/roar-prod")
        == "prod/roar-prod"
    )


SIDE_EFFECT = [
    b"""
    [{
        "CreateTime": "2022-04-07T17:49:47.202419Z",
        "Data": {
            "classId": "g1",
            "completed": true,
            "timeStarted": "2022-04-07T17:49:47.108Z"
        },
        "ID": "test-id-0",
        "Path": "databases/(default)/documents/users/0001/runs/test-id-0",
        "ReadTime": "2022-05-16T21:26:38.099915Z",
        "UpdateTime": "2022-04-07T17:58:45.371248Z"
    }]
    """,
    b"""
    [{
        "CreateTime": "2022-03-31T16:16:39.917163Z",
        "Data": {
            "classId": "KG",
            "completed": true,
            "timeStarted": "2022-03-31T16:16:39.854Z"
        },
        "ID": "test-id-1",
        "Path": "databases/(default)/documents/users/0001/runs/test-id-1",
        "ReadTime": "2022-05-16T21:26:38.099915Z",
        "UpdateTime": "2022-03-31T16:24:33.472658Z"
    }]
    """,
    b"""
    [{
        "CreateTime": "2022-03-30T17:24:51.524695Z",
        "Data": {
            "classId": "G1",
            "completed": true,
            "timeStarted": "2022-03-30T17:24:51.475Z"
        },
        "ID": "test-id-2",
        "Path": "databases/(default)/documents/users/0001/runs/test-id-2",
        "ReadTime": "2022-05-16T21:26:38.099915Z",
        "UpdateTime": "2022-03-30T17:33:11.711777Z"
    }]
    """,
    b"""
    [{
        "CreateTime": "2022-03-30T15:50:44.723343Z",
        "Data": {
            "classId": "KG",
            "completed": true,
            "timeStarted": "2022-03-30T15:50:44.676Z"
        },
        "ID": "test-id-3",
        "Path": "databases/(default)/documents/users/0001/runs/test-id-3",
        "ReadTime": "2022-05-16T21:26:38.099915Z",
        "UpdateTime": "2022-03-30T15:59:14.023472Z"
    }]
    """,
    b"",
]


@pytest.mark.parametrize("limit", [1, None])
@patch("subprocess.check_output", side_effect=SIDE_EFFECT)
def test_page_results(mock_subproc_check_output: Mock, limit: Optional[int]) -> None:
    """It returns the results of a query."""
    results = page_results(
        ["fuego", "query", "prod/roar-prod/users/0001/runs", 'classId=="c1"'],
        limit=limit,
    )
    mock_subproc_check_output.assert_called()

    expected = [bytes2json(result)[0] for result in drop_empty(SIDE_EFFECT)]
    if limit == 1:
        assert expected == results
        mock_subproc_check_output.assert_called_with(
            [
                "fuego",
                "query",
                "--startafter",
                "users/0001/runs/test-id-3",
                "--limit",
                "1",
                "prod/roar-prod/users/0001/runs",
                'classId=="c1"',
            ]
        )
    else:
        assert [expected[0]] == results
        print(mock_subproc_check_output.call_args)
        mock_subproc_check_output.assert_called_with(
            [
                "fuego",
                "query",
                "--limit",
                "100",
                "prod/roar-prod/users/0001/runs",
                'classId=="c1"',
            ]
        )
