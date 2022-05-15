"""Query and return ROAR runs."""
from datetime import date
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd
from dateutil.parser import isoparse
from tqdm.auto import tqdm

from .utils import page_results
from .utils import trim_doc_path


def get_trials_from_run(run_path: str) -> List[Dict[str, str]]:
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

    # We want to merge the trial data with some of the metadata stored in
    # raw_trials. In Python 3.9 we could use the | operator but we want to be
    # backward compatible so we iterate over the trial data and trial metadata
    # and merge them together.
    trial_data = [trial["Data"] for trial in raw_trials]
    for trial, raw_trial in zip(trial_data, raw_trials):
        trial.update(
            {"CreateTime": raw_trial["CreateTime"], "trialId": raw_trial["ID"]}
        )

    return trial_data


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
    if roar_uid is None:
        runs = [run for run in runs if root_doc in run["Path"]]

    # Get rid of runs that are outside of the date range
    if started_before is not None:
        runs = [run for run in runs if isoparse(run["timeStarted"]) < started_before]

    if started_after is not None:
        runs = [run for run in runs if isoparse(run["timeStarted"]) > started_after]

    df_runs = pd.DataFrame(runs)
    df_runs.set_index("ID", inplace=True)
    df_runs.index.names = ["runId"]

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
        df["runId"] = run_id

    df_trials = pd.concat(run_trials.values())
    df_trials.set_index("trialId", inplace=True)
    df_trials = df_trials.merge(df_runs, left_on="runId", right_index=True, how="left")

    return df_trials
