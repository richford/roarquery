"""Command-line interface."""
import click
import pandas as pd

from .queries import get_runs, get_trials_from_run


@click.command()
@click.version_option()
def main() -> None:
    """Roardb."""
    runs = get_runs(
        query_kwargs={
            "taskId": "swr",
            "studyId": "validate-regularRandom",
        }
    )
    run_paths = {run["ID"]: run["Path"] for run in runs}

    run_trials = {
        run_id: get_trials_from_run(run_path) for run_id, run_path in run_paths.items()
    }

    run_trials = {
        run_id: pd.DataFrame(trials) for run_id, trials in run_trials.items() if trials
    }

    for run_id, df in run_trials.items():
        df["run_id"] = run_id

    df = pd.concat(run_trials.values())
    df.set_index("trialId", inplace=True)
    df.to_csv("trials.csv", index=True)


if __name__ == "__main__":
    main(prog_name="roardb")  # pragma: no cover
