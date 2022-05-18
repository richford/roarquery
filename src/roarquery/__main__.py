"""Command-line interface."""
from datetime import date

import click

from .runs import get_runs
from .utils import camel_case


@click.version_option()
@click.group(
    epilog="""
\b
Useful definitions:
- trial: a single stimulus/response pair
- run: globally unique collection of successive trials.
       This constitute “running” through the task one time.
- corpus: A named and immutable collection of stimuli
- block: A portion of a run whose stimuli are drawn from only one corpus.
- task: the activity or assessment that was performed in a run (e.g. SWR, PA, SRE, etc.)
- task-variant: a specification of the task, e.g. adaptive vs. random; 1 vs 3 blocks
- school, district, class: all assume the standard meaning
- study: a collection of runs associated with a research project
"""
)
def main() -> None:
    """Roarquery.

    Roarquery is a command-line interface for querying ROAR data in Google Cloud
    Firestore. It has several subcommands, which are listed below.
    """
    pass


@main.command(
    epilog="""
Examples:

  Return trials for the "swr" task in the "validation" study.

    $ roarquery runs --task-id=swr --study-id=validation --return-trials trials.csv

  Return runs for the "sre" task in the "sd" district that started after 2021-05-10.

    $ roarquery runs --task-id=sre --district-id=sd --started-after=2021-05-10 runs.csv
"""
)
@click.option(
    "--roar-uid", type=str, help="Return only runs for the user with this ROAR UID."
)
@click.option("--task-id", type=str, help="Return only runs for this task.")
@click.option("--study-id", type=str, help="Return only runs for this study.")
@click.option("--variant-id", type=str, help="Return only runs for this variant.")
@click.option("--district-id", type=str, help="Return only runs for this district.")
@click.option("--school-id", type=str, help="Return only runs for this school.")
@click.option("--class-id", type=str, help="Return only runs with this class.")
@click.option(
    "--require-completed",
    is_flag=True,
    show_default=True,
    default=False,
    help="Require all runs to be completed.",
)
@click.option(
    "--started-before",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Return only runs started before this date. Format: YYYY-MM-DD.",
)
@click.option(
    "--started-after",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Return only runs started after this date. Format: YYYY-MM-DD.",
)
@click.option(
    "--return-trials",
    is_flag=True,
    default=False,
    help="Return the trials for each run as well.",
)
@click.option(
    "--root-doc",
    type=str,
    default="prod/roar-prod",
    help="The Firestore root document. Returned runs will all be under this document.",
)
@click.argument(
    "output_filename",
    type=click.Path(dir_okay=False, writable=True),
)
def runs(
    roar_uid: str,
    task_id: str,
    study_id: str,
    variant_id: str,
    district_id: str,
    school_id: str,
    class_id: str,
    require_completed: bool,
    started_before: date,
    started_after: date,
    return_trials: bool,
    root_doc: str,
    output_filename: click.Path,
) -> None:
    r"""Return ROAR runs matching certain query parameters.

    The options described below can be combined to return runs that match
    all of the specified query parameters.

    \b
    Arguments:
      OUTPUT FILENAME            Path to the output file to which to save runs/trials.
    """
    query_kwargs = {
        "roar_uid": roar_uid,
        "task_id": task_id,
        "study_id": study_id,
        "variant_id": variant_id,
        "district_id": district_id,
        "school_id": school_id,
        "class_id": class_id,
    }

    # Convert to camelCase and remove None values.
    query_kwargs = {
        camel_case(key): value
        for key, value in query_kwargs.items()
        if value is not None
    }

    if require_completed:
        query_kwargs["completed"] = "true"

    df_trials = get_runs(
        root_doc=root_doc,
        return_trials=return_trials,
        query_kwargs=query_kwargs,
        started_before=started_before,
        started_after=started_after,
    )

    df_trials.to_csv(output_filename, index=True)


if __name__ == "__main__":
    main(prog_name="roarquery")  # pragma: no cover
