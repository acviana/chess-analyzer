import json

from chess_analyzer import __version__
from chess_analyzer.core import parse_game_file


def test_version():
    assert __version__ == "0.0.1"


def load_fixture():
    with open("test/test_game.pgn") as f:
        return f.read()


def load_expected_result():
    with open("test/test_game.json") as f:
        return json.load(f)


def test_parse_game_file():
    expected_result = load_expected_result()
    test_fixture = load_fixture()
    parsed_game = parse_game_file(test_fixture)
    assert parsed_game == expected_result
