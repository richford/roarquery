"""Utilities functions."""
import json
import subprocess  # noqa: S404
from re import sub
from typing import List


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
    """
    string = sub(r"(_|-)+", " ", string).title().replace(" ", "")
    return "".join([string[0].lower(), string[1:]])


def bytes2json(bytes: bytes) -> List[dict]:
    """Convert bytes to json.

    Parameters
    ----------
    bytes : bytes
        The bytes to convert.

    Returns
    -------
    List[dict]
        The converted json.

    Examples
    --------
    >>> bytes2json(b'[{"ID": "1", "Data": {"a": "b"}}]')
    [{'ID': '1', 'Data': {'a': 'b'}}]
    """
    if not bytes:
        return []
    return json.loads(bytes.decode("utf-8"))


def page_results(query: List[str], limit: int = 100) -> bytes:
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
    bytes
        The results of the query.
    """
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


def drop_empty(iterable: list) -> list:
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
    >>> standardize_firestore_path(
    ...    "projects/project-id/databases/(default)/documents/prod/roar-prod"
    ... )
    prod/roar-prod
    """
    return path.split("databases/(default)/documents/")[-1]
