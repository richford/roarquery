"""Test cases for the runs module."""
from datetime import date
from datetime import datetime
from typing import Optional
from typing import Type
from typing import Union
from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd
import pytest

from .mock_bytes import RUNS
from .mock_bytes import RUNS_BYTES
from .mock_bytes import TRIALS_BYTES
from roarquery.runs import filter_run_dates
from roarquery.runs import get_runs
from roarquery.runs import get_trials_from_run
from roarquery.runs import merge_data_with_metadata
from roarquery.utils import bytes2json


@pytest.mark.parametrize("date_or_datetime", [date, datetime])
def test_filter_run_dates(date_or_datetime: Union[Type[date], Type[datetime]]) -> None:
    """It filters runs by date."""
    filtered = filter_run_dates(RUNS, started_before=date_or_datetime(2020, 1, 20))
    assert filtered == [RUNS[0]]

    filtered = filter_run_dates(RUNS, started_before=date_or_datetime(1970, 2, 1))
    assert filtered == []

    filtered = filter_run_dates(
        RUNS,
        started_before=date_or_datetime(2020, 2, 15),
        started_after=date_or_datetime(2020, 1, 15),
    )
    assert filtered == [RUNS[1]]

    filtered = filter_run_dates(RUNS)
    assert filtered == RUNS


def test_merge_data_with_metadata() -> None:
    """It merges data with metadata."""
    merged = merge_data_with_metadata(
        fuego_response=RUNS, metadata_params={"runId": "ID"}
    )
    expected = [run["Data"] for run in RUNS]
    for run_out, run_in in zip(expected, RUNS):
        run_out["runId"] = run_in["ID"]

    assert merged == expected


@patch("subprocess.check_output", return_value=TRIALS_BYTES)
def test_get_trials_from_runs(mock_subproc_check_output: Mock) -> None:
    """It gets trials from runs."""
    trials = get_trials_from_run(RUNS[0]["Path"])
    mock_subproc_check_output.assert_called_once()
    mock_subproc_check_output.assert_called_with(
        ["fuego", "query", "--limit", "100", f"{RUNS[0]['Path']}/trials"]
    )

    assert trials == merge_data_with_metadata(
        fuego_response=bytes2json(TRIALS_BYTES),
        metadata_params={"CreateTime": "CreateTime", "trialId": "ID"},
    )


@pytest.mark.parametrize("roar_uid", [None, "0001"])
@pytest.mark.parametrize("started_before", [None, date(2020, 2, 15)])
@pytest.mark.parametrize("started_after", [None, date(2020, 1, 15)])
@patch("subprocess.check_output", return_value=RUNS_BYTES)
def test_get_runs(
    mock_subproc_check_output: Mock,
    started_after: Optional[date],
    started_before: Optional[date],
    roar_uid: Optional[str],
) -> None:
    """It gets runs."""
    query_kwargs = dict(foo="bar")

    if roar_uid is not None:
        query_kwargs["roarUid"] = roar_uid

    runs = get_runs(
        query_kwargs=query_kwargs,
        started_before=started_before,
        started_after=started_after,
    )

    expected = pd.DataFrame(
        merge_data_with_metadata(
            filter_run_dates(
                RUNS, started_after=started_after, started_before=started_before
            ),
            metadata_params={"CreateTime": "CreateTime", "runId": "ID"},
        )
    )
    expected.set_index("runId", inplace=True)
    assert runs.equals(expected)

    mock_subproc_check_output.assert_called_once()

    call_args = [
        "fuego",
        "query",
        "--limit",
        "100",
        "--select",
        "classId",
        "--select",
        "completed",
        "--select",
        "districtId",
        "--select",
        "schoolId",
        "--select",
        "studyId",
        "--select",
        "taskId",
        "--select",
        "timeFinished",
        "--select",
        "timeStarted",
        "--select",
        "variantId",
    ]

    if roar_uid is None:
        call_args.extend(["-g", "runs"])
    else:
        call_args.append(f"prod/roar-prod/users/{roar_uid}/runs")

    call_args.append('foo == "bar"')

    mock_subproc_check_output.assert_called_with(call_args)


@patch("subprocess.check_output", return_value=b"")
def test_get_runs_empty_error(
    mock_subproc_check_output: Mock,
) -> None:
    """It returns an error for empty query results."""
    with pytest.raises(ValueError):
        get_runs(
            query_kwargs=dict(),
        )

    mock_subproc_check_output.assert_called_once()


@patch("subprocess.check_output", side_effect=[RUNS_BYTES, TRIALS_BYTES])
def test_get_runs_and_trials(
    mock_subproc_check_output: Mock,
) -> None:
    """It returns merged runs and trials."""
    trials = get_runs(
        query_kwargs=dict(), return_trials=True, started_before=date(2020, 1, 15)
    )

    df_runs = pd.DataFrame(
        merge_data_with_metadata(
            filter_run_dates(RUNS, started_before=date(2020, 1, 15)),
            metadata_params={"CreateTime": "CreateTime", "runId": "ID"},
        )
    )
    run_id = pd.unique(df_runs["runId"])[0]
    df_runs.set_index("runId", inplace=True)
    df_trials = pd.DataFrame(
        merge_data_with_metadata(
            bytes2json(TRIALS_BYTES),
            metadata_params={"CreateTime": "CreateTime", "trialId": "ID"},
        )
    )
    df_trials["runId"] = run_id
    df_trials.set_index("trialId", inplace=True)
    df_trials = df_trials.merge(df_runs, left_on="runId", right_index=True, how="left")

    assert trials.equals(df_trials)
