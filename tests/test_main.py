"""Test cases for the __main__ module."""
from datetime import date
from unittest.mock import Mock
from unittest.mock import patch

import pandas as pd
import pytest
from click.testing import CliRunner

from .mock_bytes import RUNS
from .mock_bytes import RUNS_BYTES
from .mock_bytes import TRIALS_1_BYTES
from .mock_bytes import TRIALS_4_BYTES
from .mock_bytes import TRIALS_BYTES
from roarquery import __main__
from roarquery.runs import filter_run_dates
from roarquery.runs import merge_data_with_metadata
from roarquery.utils import bytes2json


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_yields_help(runner: CliRunner) -> None:
    """It exits with a status code of zero and returns help."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "Options" in result.output
    assert "Commands" in result.output
    assert "Useful definitions" in result.output


def test_runs_yields_help(runner: CliRunner) -> None:
    """It exits with a status code of zero and yields help."""
    result = runner.invoke(__main__.main, ["runs", "--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "Options" in result.output
    assert "Examples" in result.output


@pytest.mark.parametrize("completed", [True, False])
@patch(
    "subprocess.check_output", side_effect=[RUNS_BYTES, TRIALS_1_BYTES, TRIALS_4_BYTES]
)
def test_runs(
    mock_subproc_check_output: Mock, runner: CliRunner, completed: bool
) -> None:
    """It saves runs to a csv file."""
    cli_args = [
        "runs",
        "--task-id=swr",
        "--return-trials",
        "--started-before=2020-01-15",
    ]

    if completed:
        cli_args.append("--require-completed")

    cli_args.append("trials.csv")

    with runner.isolated_filesystem():
        result = runner.invoke(__main__.main, cli_args)

        assert result.exit_code == 0

        output = pd.read_csv("trials.csv", index_col="trialId")
        df_runs = pd.DataFrame(
            merge_data_with_metadata(
                filter_run_dates(RUNS, started_before=date(2020, 1, 15)),
                metadata_params={"CreateTime": "CreateTime", "runId": "ID"},
            )
        )
        run_ids = pd.unique(df_runs["runId"])
        df_runs.set_index("runId", inplace=True)
        df_trials = pd.DataFrame(
            merge_data_with_metadata(
                bytes2json(TRIALS_BYTES),
                metadata_params={"CreateTime": "CreateTime", "trialId": "ID"},
            )
        )
        df_trials.loc[:6, "runId"] = run_ids[0]
        df_trials.loc[6:, "runId"] = run_ids[1]
        df_trials.set_index("trialId", inplace=True)
        expected = df_trials.merge(
            df_runs, left_on="runId", right_index=True, how="left"
        )
        expected["completed"] = expected["completed"].map(
            {"true": True, "false": False}
        )

        assert output.equals(expected)

    mock_subproc_check_output.assert_called()
    assert mock_subproc_check_output.call_count == 3

    expected_call_args = [
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
        "-g",
        "runs",
        'taskId == "swr"',
    ]

    if completed:
        expected_call_args.append('completed == "true"')

    mock_subproc_check_output.assert_any_call(expected_call_args)
    mock_subproc_check_output.assert_any_call(
        [
            "fuego",
            "query",
            "--limit",
            "100",
            "prod/roar-prod/users/aa-0001/runs/run-1/trials",
        ]
    )
    mock_subproc_check_output.assert_any_call(
        [
            "fuego",
            "query",
            "--limit",
            "100",
            "prod/roar-prod/users/bb-0001/runs/run-4/trials",
        ]
    )
