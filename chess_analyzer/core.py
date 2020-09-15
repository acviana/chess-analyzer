"""
Functionality that's used in more than one module.
"""

import re


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
