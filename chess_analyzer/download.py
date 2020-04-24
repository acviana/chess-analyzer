from datetime import datetime
import os

import requests

from chess_analyzer.core import parse_game_file


def download_files_in_date_range(username, start_date, end_date):
    """
    Iterate query_bulk_games_endpoint over a date range.

    Args:
        username (str): The chess.com username to query.
        start_date (datetime.datetime): The first month to query
        end_date (datetime.dateimte: The last month to query

    Returns:
        str: A string of all the game information from the query period.
    """
    game_file_buffer = ""
    for year in range(start_date.year, end_date.year + 1):
        for month in range(1, 12):
            response = query_bulk_games_endpoint(username, year, month)
            # TODO: Fix for loop to never attempt a date in the future.
            if response.status_code == 404:
                if response.json()["message"] == "Date cannot be set in the future":
                    return game_file_buffer
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
        requests.response: A requests.response object.
    """
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}/pgn"
    return requests.get(
        url=url,
        headers={
            "Content-Type": "application/x-chess-pgn",
            "Content-Disposition": 'attachment; filename="ChessCom_username_YYYYMM.pgn"',
        },
    )


def split_builk_file_download(bulk_file_download):
    games_list = bulk_file_download.split("\n\n[Event")
    games_list = ["[Event" + item for item in games_list]
    return games_list


def write_game_file(filename, game_file):
    with open(filename, "w") as f:
        f.write(game_file)


def download_main(username, start_date, end_date, output_dir):
    game_buffer = download_files_in_date_range(
        username=username, start_date=start_date, end_date=end_date
    )
    games_list = split_builk_file_download(game_buffer)
    for game in games_list:
        parsed_game = parse_game_file(game)
        filename = os.path.join(
            output_dir, f"{parsed_game['link'].split('/')[-1]}.pgn",
        )
        write_game_file(filename=filename, game_file=game)
    print(
        f"Found {len(games_list)} games from {datetime.strftime(start_date, '%Y-%m')} "
        f"to {datetime.strftime(end_date, '%Y-%m')}"
    )


if __name__ == "__main__":
    start_date = datetime.strptime("2018-01", "%Y-%m")
    end_date = datetime.strptime("2020-04", "%Y-%m")
    download_main(
        username="acviana", start_date=start_date, end_date=end_date, output_dir="data"
    )
