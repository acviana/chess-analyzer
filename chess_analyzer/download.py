"""
Functionality for downloading and storing data from chess.com
"""

from datetime import datetime
import os

import requests

from chess_analyzer.core import parse_game_file, write_game_file


def download_files_in_date_range(username, start_datetime, end_datetime):
    """
    Iterate :py:func:`chess_analyzer.download.query_bulk_games_endpoint`
    over a date range.

    Args:
        username (str): The chess.com username to query
        start_datetime (datetime.datetime): The first month to query
        end_datetime (datetime.datetime): The last month to query

    Returns:
        str: A string of all the game information from the query period.
    """
    today_datetime = datetime.today()
    game_file_buffer = ""
    for year in range(start_datetime.year, end_datetime.year + 1):
        first_month = start_datetime.month if year == start_datetime.year else 1
        for month in range(first_month, 13):
            if year == today_datetime.year:
                if month == today_datetime.month + 1 or month == end_datetime.month + 1:
                    return game_file_buffer
            response = query_bulk_games_endpoint(username, year, month)
            if len(response.content) != 0:
                game_file_buffer += response.content.decode()


def query_bulk_games_endpoint(username, year, month):
    """
    Get data from the chess.com bulk game API endpoint.

    Args:
        username (str): A valid chess.com username.
        year (str): Year in a YYYY format.
        month (str): Month in a MM format.

    Returns:
        requests.response: A ``requests.response`` object from the
        chess.com bulk download API.
    """
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}/pgn"
    return requests.get(
        url=url,
        headers={
            "Content-Type": "application/x-chess-pgn",
            "Content-Disposition": 'attachment; filename="ChessCom_username_YYYYMM.pgn"',
        },
    )


def split_bulk_file_download(bulk_file_download):
    """
    Split the chess.com bulk download file into individual PGN files.

    Args:
        bulk_file_download (str): The chess.com bulk download data.

    Returns:
        list: A list of individual game data strings.
    """
    return ["[Event" + item for item in bulk_file_download.split("\n\n[Event")]


def download_main(username, start_datetime, end_datetime, output_dir):
    game_buffer = download_files_in_date_range(
        username=username, start_datetime=start_datetime, end_datetime=end_datetime
    )
    games_list = split_bulk_file_download(game_buffer)
    for game in games_list:
        parsed_game = parse_game_file(game)
        filename = os.path.join(
            output_dir,
            f"{parsed_game['link'].split('/')[-1]}.pgn",
        )
        write_game_file(filename=filename, game_file=game)
    print(
        f"Found {len(games_list)} games from {datetime.strftime(start_datetime, '%Y-%m')} "
        f"to {datetime.strftime(end_datetime, '%Y-%m')}"
    )
