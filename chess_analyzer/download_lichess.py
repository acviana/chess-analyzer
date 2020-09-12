import os
import re

import requests


def query_endpoint(username, **params):
    return requests.get(
        url=f"https://lichess.org/api/games/user/{username}",
        params=params,
        #     # since, until
        #     # params={"max": 5, "clocks": True, "opening": True, "evals": True},
    )  # , stream=True)


def parse_game(game):
    key_re = re.compile(r"\[(?P<key>\S*)")
    value_re = re.compile(r"\"(?P<value>.+)\"")
    parsed_game = {}
    for row in game.split("\n"):
        if row == "":
            continue
        elif row[0] == "[":
            parsed_game[key_re.match(row).group("key")] = value_re.search(row).group(
                "value"
            )
        else:
            parsed_game["game"] = row
    return parsed_game


def split_bulk_file_download(bulk_file_download):
    return bulk_file_download.split("\n\n\n")[0:-1]


def write_game_file(filename, game_file):
    """
    Write an output PGN game file.

    Args:
        filename (str): The output filename.
        game_file (str): The PGN file contents.
    """
    with open(filename, "w") as f:
        f.write(game_file)


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
        parsed_game = parse_game(game)
        filename = os.path.join(
            output_dir,
            f"{parsed_game['Site'].split('/')[-1]}.pgn",
        )
        write_game_file(filename=filename, game_file=game)


if __name__ == "__main__":
    download_main("acviana", "2020-01", "2020-09", "data/")
