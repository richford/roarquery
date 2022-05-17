"""Utilities functions."""
import json
import subprocess  # noqa: S404
from re import sub
from typing import Any
from typing import cast
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import TypedDict


_FuegoKey = Literal["CreateTime", "Data", "ID", "Path", "ReadTime", "UpdateTime"]


class _FuegoResponse(TypedDict):
    CreateTime: str
    Data: Dict[str, Any]
    ID: str
    Path: str
    ReadTime: str
    UpdateTime: str


def camel_case(string: str) -> str:
    """Convert a string to camel case.

    Parameters
    ----------
    string : str
        The string to convert.

    Returns
    -------
    str
        The camel case string.

    Examples
    --------
    >>> camel_case("an_example_string")
    anExampleString

    >>> camel_case("an-example-string-with-dashes")
    anExampleStringWithDashes
    """
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return "".join([string[0].lower(), string[1:]])


def bytes2json(bytes: bytes) -> List[_FuegoResponse]:
    r"""Convert bytes to json.

    Parameters
    ----------
    bytes : bytes
        The bytes to convert.

    Returns
    -------
    List[_FuegoResponse]
        The converted json.

    Examples
    --------
    An empty string will return an empty list:
    >>> bytes2json(b"")
    []

    >>> json_out = bytes2json(
    ...    b'[{"ID": "1", "Data": {"a": "b"}, "Path": "prod/roar-prod", '
    ...    b'"CreateTime": "2020-04-01T00:00:00Z", '
    ...    b'"ReadTime": "2020-04-01T00:00:00Z", '
    ...    b'"UpdateTime": "2020-04-01T00:00:00Z"}]'
    ... )
    >>> print(json_out == [{
    ...     'ID': '1',
    ...     'Data': {'a': 'b'},
    ...     'Path': 'prod/roar-prod',
    ...     'CreateTime': '2020-04-01T00:00:00Z',
    ...     'ReadTime': '2020-04-01T00:00:00Z',
    ...     'UpdateTime': '2020-04-01T00:00:00Z'
    ... }])
    True
    """
    if not bytes:
        return []
    return cast(List[_FuegoResponse], json.loads(bytes.decode("utf-8")))


def page_results(query: List[str], limit: Optional[int] = None) -> List[_FuegoResponse]:
    """Page through results from a query.

    Parameters
    ----------
    query : List[str]
        The query to run. This is a list of strings that will be passed to
        subprocess.check_output.

    limit : int, optional, default=100
        The number of results to return per page.

    Returns
    -------
    List[_FuegoResponse]
        The results of the query.
    """
    limit = limit if limit is not None else 100
    query_idx = query.index("query")
    query.insert(query_idx + 1, "--limit")
    query.insert(query_idx + 2, str(limit))

    output = []
    this_page = subprocess.check_output(query)  # noqa: S603

    while this_page:
        output.extend(bytes2json(this_page))

        if len(bytes2json(this_page)) == limit:
            if "--startafter" in query:
                start_after_idx = query.index("--startafter")
                query[start_after_idx + 1] = output[-1]["ID"]
            else:
                query.insert(query_idx + 1, "--startafter")
                query.insert(query_idx + 2, output[-1]["ID"])

            this_page = subprocess.check_output(query)  # noqa: S603
        else:
            this_page = b""

    return output


def drop_empty(iterable: List[Any]) -> List[Any]:
    """Drop empty strings from a list.

    Parameters
    ----------
    iterable : list
        The list to drop empty strings from.

    Returns
    -------
    list
        The list with empty strings dropped.

    Examples
    --------
    >>> drop_empty(["", "a", "", "b"])
    ['a', 'b']
    """
    return [x for x in iterable if x]


def trim_doc_path(path: str) -> str:
    """Remove leading project information from firestore document path.

    Parameters
    ----------
    path : str
        The path to standardize.

    Returns
    -------
    str
        The standardized path.

    Examples
    --------
    >>> trim_doc_path("projects/proj-id/databases/(default)/documents/prod/roar-prod")
    prod/roar-prod
    """
    return path.split("databases/(default)/documents/")[-1]
