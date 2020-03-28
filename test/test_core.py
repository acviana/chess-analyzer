import json

from chess_analyzer.core import parse_game_file


def load_fixture():
    with open("test/test_game.pgn") as f:
        return f.read()


def load_expected_result():
    with open("test/test_game.json") as f:
        return json.load(f)


def test():
    test_fixture = load_fixture()
    expected_result = load_expected_result()
    parsed_game = parse_game_file(test_fixture)
    assert parsed_game == expected_result
