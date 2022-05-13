import json

import pandas as pd
import subprocess

from typing import List, Optional

from .utils import trim_doc_path, page_results


def to_csv(results: List[dict], filename: str) -> None:
    df = pd.DataFrame(results)
    df.to_csv(filename)


def get_trials_from_run(runPath: str) -> List[dict]:
    """Get all trials from a run.

    Parameters
    ----------
    runPath : str
        The Firestore path to the run.

    Returns
    -------
    List[dict]
        The trials from the run.
    """
    trial_path = f"{trim_doc_path(runPath)}/trials"
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
    rootDoc: str = "prod/roar-prod",
    query_kwargs: Optional[dict] = None,
) -> List[dict]:
    """Get all runs that satisfy a specific query.

    Parameters
    ----------
    rootDoc : str, optional, default="prod/roar-prod"
        The Firestore root document. The returned runs will all be under this document.

    query_kwargs : dict, optional, default=None
        The query to run. If None, all runs will be returned.

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

    query = ["-g", "runs"]
    for key, value in query_kwargs.items():
        query.append(f'{key} == "{value}"')

    fuego_args.extend(query)
    output = page_results(fuego_args)

    if not output:
        raise ValueError("Your query returned no results.")

    # Get rid of results that are not in the rootDoc
    output = [result for result in output if rootDoc in result["Path"]]

    return output
