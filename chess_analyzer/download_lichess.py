import re

import requests

from chess_analyzer.core import (
    get_pgn_output_filename,
    parse_game_file,
    write_game_file,
)


def query_endpoint(username, **kwargs):
    return requests.get(
        url=f"https://lichess.org/api/games/user/{username}",
        params=kwargs,
    )  # , stream=True)


def split_bulk_file_download(bulk_file_download):
    return bulk_file_download.split("\n\n\n")[0:-1]


# add start and end date
def download_main(username, start_datetime, end_datetime, output_dir):
    # since, until
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
    print(f"Downloaded {len(game_list)} games from Lichess.com")
    for game in game_list:
        parsed_game = parse_game_file(game)
        filename = get_pgn_output_filename(parsed_game, output_dir, "lichess")
        write_game_file(filename=filename, game_file=game)


if __name__ == "__main__":
    download_main("acviana", "2020-01", "2020-09", "data/")
