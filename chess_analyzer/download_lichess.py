import re

import requests

from chess_analyzer.core import (
    get_pgn_output_filename,
    parse_game_file,
    write_game_file,
)


def query_endpoint(username, **kwargs):
    """
    Args:
        username (str):

    Keyword Args:
        All Lichess API endpoint parameters are allowed, see Reference
        notes.

    Returns:
        (requests.response)

    References:
        https://lichess.org/api#operation/apiGamesUser

    Todo:
        Consider implimenting streaming as suggested but Lichess API notes:
        https://requests.readthedocs.io/en/master/user/advanced/#streaming-requests
    """
    return requests.get(
        url=f"https://lichess.org/api/games/user/{username}",
        params=kwargs,
    )  # , stream=True)


def split_bulk_file_download(bulk_file_download):
    """
    Args:
        bulk_file_download (str): A bulk file download from Lichess.

    Returns:
        (list)
    """
    return bulk_file_download.split("\n\n\n")[0:-1]


def download_main(username, start_datetime, end_datetime, output_dir):
    """
    Args:
        username (str): Lichess username.
        start_datetime (str): Starting limit of API query.
        end_datetime (str): Ending limit of APO query.
        output_dir (str): Desired output directory.
    """
    params = {
        "max": None,
        "clocks": True,
        "opening": True,
        "evals": True,
        "since": start_datetime,
        "until": end_datetime,
    }
    response = query_endpoint(username=username, **params)
    game_list = split_bulk_file_download(response.content.decode())
    print(f"Downloaded {len(game_list)} games from Lichess.org")
    for game in game_list:
        parsed_game = parse_game_file(game)
        filename = get_pgn_output_filename(parsed_game, output_dir, "lichess")
        write_game_file(filename=filename, game_file=game)


if __name__ == "__main__":
    download_main("acviana", "2020-01", "2020-09", "data/")
