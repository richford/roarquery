"""Test cases for the runs module."""
import pytest
from datetime import date
from datetime import datetime
from unittest.mock import patch
from roarquery.runs import filter_run_dates
from roarquery.runs import get_runs
from roarquery.runs import merge_data_with_metadata
from roarquery.utils import _FuegoResponse
from typing import cast
from typing import List
from typing import Type
from typing import Union


@pytest.mark.parametrize("date_or_datetime", [date, datetime])
def test_filter_run_dates(date_or_datetime: Union[Type[date], Type[datetime]]) -> None:
    runs = cast(
        List[_FuegoResponse],
        [
            {
                "CreateTime": "2020-01-01T00:00:00.000Z",
                "Data": {
                    "name": "run-1",
                    "timeStarted": "2020-01-01T00:00:00.000Z",
                    "classId": "class-1",
                    "completed": "true",
                },
                "ID": "run-1",
                "Path": "prod/roar-prod/runs/run-1",
                "ReadTime": "2020-01-01T00:00:00.000Z",
                "UpdateTime": "2020-01-01T00:00:00.000Z",
            },
            {
                "CreateTime": "2020-02-01T00:00:00.000Z",
                "Data": {
                    "name": "run-2",
                    "timeStarted": "2020-02-01T00:00:00.000Z",
                    "classId": "class-2",
                    "completed": "true",
                },
                "ID": "run-2",
                "Path": "prod/roar-prod/runs/run-1",
                "ReadTime": "2020-02-01T00:00:00.000Z",
                "UpdateTime": "2020-02-01T00:00:00.000Z",
            },
            {
                "CreateTime": "2020-03-01T00:00:00.000Z",
                "Data": {
                    "name": "run-3",
                    "timeStarted": "2020-03-01T00:00:00.000Z",
                    "classId": "class-2",
                    "completed": "true",
                },
                "ID": "run-3",
                "Path": "prod/roar-prod/runs/run-1",
                "ReadTime": "2020-03-01T00:00:00.000Z",
                "UpdateTime": "2020-03-01T00:00:00.000Z",
            },
        ],
    )

    filtered = filter_run_dates(runs, started_before=date_or_datetime(2020, 1, 20))
    assert filtered == [runs[0]]

    filtered = filter_run_dates(runs, started_before=date_or_datetime(1900, 1, 1))
    assert filtered == []

    filtered = filter_run_dates(
        runs,
        started_before=date_or_datetime(2020, 2, 15),
        started_after=date_or_datetime(2020, 1, 15),
    )
    assert filtered == [runs[1]]

    filtered = filter_run_dates(runs)
    assert filtered == runs
