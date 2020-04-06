from datetime import date

import click

from chess_analyzer.download import download_main


@click.command()
@click.argument("username")
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
def download(username, start_date, end_date, output_dir):
    """
    Download png files for a chess.com user over a date range.

    e.g. chess-analyzer USERNAME YYYY-MM YYYY-MM
    """
    download_main(username, start_date, end_date, output_dir)
