from datetime import date

import click

from chess_analyzer import (
    download_chess_dot_com,
    download_lichess,
)
from chess_analyzer.analysis import print_summary_report


@click.group()
def download_group():
    pass


@download_group.command()
@click.argument("username")
@click.argument(
    "source", type=click.Choice(["chess.com", "lichess"], case_sensitive=False)
)
@click.argument("start-date", type=click.DateTime(formats=["%Y-%m"]))
@click.argument(
    "end-date", type=click.DateTime(formats=["%Y-%m"]), default=str(date.today())
)
@click.option(
    "--output-dir",
    default="data/",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, writable=True, readable=True
    ),
)
def download(username, source, start_date, end_date, output_dir):
    """
    Download png files for a chess.com user over a date range.

    e.g. chess-analyzer USERNAME YYYY-MM YYYY-MM
    """
    if source == "chess.com":
        download_chess_dot_com.download_main(
            username=username,
            start_datetime=start_date,
            end_datetime=end_date,
            output_dir=output_dir,
        )
    elif source == "lichess":
        download_lichess.download_main(
            username=username,
            start_datetime=start_date,
            end_datetime=end_date,
            output_dir=output_dir,
        )
    else:
        raise Exception(
            "Parameter 'source' must be 'chess.com' or 'lichess' "
            f" got '{source}' instead."
        )

    # TODO add click help


@click.group()
def analyze_group():
    pass


@analyze_group.command()
@click.argument("username")
@click.option(
    "--search-path",
    default="data/*.pgn",
)
def analyze(username, search_path):
    """Run a high-level report on a set of .pgn files."""
    print_summary_report(src=search_path, username=username)


cli = click.CommandCollection(sources=[download_group, analyze_group])
