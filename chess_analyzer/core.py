"""
Functionality that's used in more than one module.
"""

import os
import re


def get_pgn_output_filename(parsed_game, output_dir, origin):
    """
    Return the default file name for a parsed PGN game.

    Args:
        parsed_game (dict): A dictionary representation of a parsed PNG
            game file.
        output_dir (str): Desired output directory.
        origin (str): Options are `chess.com` or `lichess`.

    Return:
        (str): A complete file path

    Raises:
        (Exception): Raises an exception is an improper optin is passed
            for `origin`.
    """
    if origin == "chess.com":
        selector = "link"
    elif origin == "lichess":
        selector = "site"
    else:
        raise Exception(
            "Parameter 'origin' must be 'chess.com' or 'lichess' "
            f" got '{origin}' instead."
        )
    return os.path.join(
        output_dir,
        f"{parsed_game[selector].split('/')[-1]}.pgn",
    )


def parse_game_file(game):
    """
    Parses a string representation of a PNG file into a dictionary.

    "Good enough" implimentation that avoids having to use a full
    JSON-LD parser library.

    Args:
        game_file (str): The string representation a PGN file.

    Returns:
        dict: A dictionary with all the PGN key-value pairs.
    """
    key_re = re.compile(r"\[(?P<key>\S*)")
    value_re = re.compile(r"\"(?P<value>.+)\"")
    parsed_game = {}
    for row in game.split("\n"):
        if row == "":
            continue
        elif row[0] == "[":
            parsed_game[key_re.match(row).group("key").lower()] = value_re.search(
                row
            ).group("value")
        else:
            parsed_game["game"] = row
    return parsed_game


def write_game_file(filename, game_file):
    """
    Write an output PGN game file.

    Args:
        filename (str): The output filename.
        game_file (str): The PGN file contents.
    """
    with open(filename, "w") as f:
        f.write(game_file)
