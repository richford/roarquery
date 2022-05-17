"""Query and return ROAR runs."""
from datetime import date
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
from dateutil.parser import isoparse
from tqdm.auto import tqdm

from .utils import _FuegoKey
from .utils import _FuegoResponse
from .utils import page_results
from .utils import trim_doc_path


def merge_data_with_metadata(
    fuego_response: List[_FuegoResponse], metadata_params: Dict[str, _FuegoKey]
) -> List[Dict[str, Any]]:
    """Merge trial data with metadata.

    We often want to merge the run/trial data with some of the metadata returned
    by Firestore. In Python 3.9 we could use the | operator but we want to be
    backward compatible so we iterate over the data and metadata and merge them
    together.

    Parameters
    ----------
    fuego_response : List[Dict[str, Any]]
        The trial data.

    metadata_params : Dict[str, str]
        The metadata fields that will be merged into the data. The keys are the
        desired keys in the merged data and the values are the metadata keys to
        use.

    Returns
    -------
    List[Dict[str, Any]]
        The merged data.
    """
    item_data = [item["Data"] for item in fuego_response]
    for item, raw_item in zip(item_data, fuego_response):
        item.update(
            {
                data_key: raw_item[metadata_key]
                for data_key, metadata_key in metadata_params.items()
            }
        )

    return item_data


def get_trials_from_run(run_path: str) -> List[Dict[str, Any]]:
    """Get all trials from a run.

    Parameters
    ----------
    run_path : str
        The Firestore path to the run.

    Returns
    -------
    List[Dict[str, str]]
        The trials from the run.
    """
    trial_path = f"{trim_doc_path(run_path)}/trials"
    fuego_query = ["fuego", "query", trial_path]
    raw_trials = page_results(fuego_query)

    return merge_data_with_metadata(
        fuego_response=raw_trials,
        metadata_params={"CreateTime": "CreateTime", "trialId": "ID"},
    )


def filter_run_dates(
    runs: List[_FuegoResponse],
    started_before: Optional[Union[date, datetime]] = None,
    started_after: Optional[Union[date, datetime]] = None,
) -> List[_FuegoResponse]:
    """Filter runs by date.

    Parameters
    ----------
    runs : List[Dict[str, Any]]
        The runs to filter.

    started_before : date, optional, default=None
        Return only runs started before this date.

    started_after : date, optional, default=None
        Return only runs started after this date.

    Returns
    -------
    List[Dict[str, Any]]
        The filtered runs.

    Examples
    --------
    >>> runs = [
    ...     {
    ...         "CreateTime": "2020-01-01T00:00:00.000Z",
    ...         "Data": {
    ...             "name": "run-1",
    ...             "timeStarted": "2020-01-01T00:00:00.000Z",
    ...             "classId": "class-1",
    ...             "completed": "true",
    ...         },
    ...         "ID": "run-1",
    ...         "Path": "prod/roar-prod/runs/run-1",
    ...         "ReadTime": "2020-01-01T00:00:00.000Z",
    ...         "UpdateTime": "2020-01-01T00:00:00.000Z",
    ...     },
    ...     {
    ...         "CreateTime": "2020-02-01T00:00:00.000Z",
    ...         "Data": {
    ...             "name": "run-2",
    ...             "timeStarted": "2020-02-01T00:00:00.000Z",
    ...             "classId": "class-2",
    ...             "completed": "true",
    ...         },
    ...         "ID": "run-2",
    ...         "Path": "prod/roar-prod/runs/run-1",
    ...         "ReadTime": "2020-02-01T00:00:00.000Z",
    ...         "UpdateTime": "2020-02-01T00:00:00.000Z",
    ...     },
    ... ]
    >>> filtered = filter_run_dates(runs, started_before=date(2020, 1, 15))
    >>> print(filtered == [runs[0]])
    True
    """
    if isinstance(started_before, date):
        started_before = datetime(
            started_before.year, started_before.month, started_before.day
        ).astimezone()

    if isinstance(started_after, date):
        started_after = datetime(
            started_after.year, started_after.month, started_after.day
        ).astimezone()

    filtered = [run for run in runs]

    if started_before is not None:
        filtered = [
            run
            for run in filtered
            if isoparse(run["Data"]["timeStarted"]) < started_before
        ]

    if started_after is not None:
        filtered = [
            run
            for run in filtered
            if isoparse(run["Data"]["timeStarted"]) > started_after
        ]

    return filtered


def get_runs(
    root_doc: str = "prod/roar-prod",
    return_trials: bool = False,
    query_kwargs: Optional[Dict[str, str]] = None,
    started_before: Optional[date] = None,
    started_after: Optional[date] = None,
) -> pd.DataFrame:
    """Get all runs that satisfy a specific query.

    Parameters
    ----------
    root_doc : str, optional, default="prod/roar-prod"
        The Firestore root document. The returned runs will all be under this document.

    return_trials : bool, optional, default=False
        If True, return the trials for each run as well.

    query_kwargs : dict, optional, default=None
        The query to run. If None, all runs will be returned.

    started_before : date, optional, default=None
        Return only runs started before this date.

    started_after : date, optional, default=None
        Return only runs started after this date.

    Returns
    -------
    List[dict]
        The runs that satisfy the query.
    """
    # Build the fuego query dynamically
    fuego_args = ["fuego", "query"]
    for select in [
        "classId",
        "completed",
        "districtId",
        "schoolId",
        "studyId",
        "taskId",
        "timeFinished",
        "timeStarted",
        "variantId",
    ]:
        fuego_args.extend(["--select", select])

    query_kwargs = query_kwargs if query_kwargs is not None else {}

    # Treat the roar UID separately
    roar_uid = query_kwargs.pop("roarUid", None)

    if roar_uid is None:
        query = ["-g", "runs"]
    else:
        query = ["/".join([root_doc.rstrip("/"), "users", roar_uid, "runs"])]

    for key, value in query_kwargs.items():
        query.append(f'{key} == "{value}"')

    fuego_args.extend(query)

    runs = page_results(fuego_args)

    if not runs:
        raise ValueError("Your query returned no results.")

    # Get rid of results that are not in the root_doc
    runs = [run for run in runs if root_doc in run["Path"]]

    # Get rid of runs that are outside of the date range
    runs = filter_run_dates(
        runs=runs, started_before=started_before, started_after=started_after
    )

    df_runs = pd.DataFrame(
        merge_data_with_metadata(
            fuego_response=runs,
            metadata_params={"CreateTime": "CreateTime", "runId": "ID"},
        )
    )
    df_runs.set_index("runId", inplace=True)

    if not return_trials:
        return df_runs

    run_paths = {run["ID"]: run["Path"] for run in runs}

    run_trials = {
        run_id: get_trials_from_run(run_path)
        for run_id, run_path in tqdm(run_paths.items(), desc="Getting trials")
    }

    run_trials = {
        run_id: pd.DataFrame(trials) for run_id, trials in run_trials.items() if trials
    }

    for run_id, df in run_trials.items():
        df["runId"] = run_id  # type: ignore [call-overload]

    df_trials = pd.concat(run_trials.values())
    df_trials.set_index("trialId", inplace=True)
    df_trials = df_trials.merge(df_runs, left_on="runId", right_index=True, how="left")

    return df_trials
