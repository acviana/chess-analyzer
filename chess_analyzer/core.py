"""
Functionality that's used in more than one module.
"""

def parse_game_file(game_file):
    """
    Parses a string representation of a PNG file into a dictionary.

    "Good enough" implimentation that avoids having to use a full
    JSON-LD parser library.

    Args:
        game_file (str): The string representation a PGN file.

    Returns:
        dict: A dictionary with all the PGN key-value pairs.
    """
    parsed_game = {}
    for item in game_file.split("\n"):
        if item == "":
            continue
        if item[0:2] == "1.":
            parsed_game["game"] = item
        else:
            item = item[1:-1]
            split = item.find(" ")
            parsed_game[item[0:split].lower()] = item[split + 2 : -1]
    return parsed_game
