"""Test cases for the collections module."""
from unittest.mock import Mock
from unittest.mock import patch

from roarquery.collections import get_collections


@patch("subprocess.check_output", return_value=b"admin\nci\ndev\nprod\n\n")
def test_get_collections(mock_subproc_check_output: Mock) -> None:
    """It returns a list of collections."""
    collections = get_collections()
    assert collections == ["admin", "ci", "dev", "prod"]
    mock_subproc_check_output.assert_called_once()
    mock_subproc_check_output.assert_called_with(["fuego", "c"])
