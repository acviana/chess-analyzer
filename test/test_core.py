import json

import pytest

from chess_analyzer import __version__
from chess_analyzer.core import get_pgn_output_filename, parse_game_file


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


def test_get_pgn_output_filename():

    # Test chess.com
    parsed_game = {"link": "bar"}
    result = get_pgn_output_filename(parsed_game, "/foo", "chess.com")
    assert result, "/foo/bar"

    # Test lichess
    parsed_game = {"site": "bar"}
    result = get_pgn_output_filename(parsed_game, "/foo", "lichess")
    assert result, "/foo/bar"

    # Test an incorrect option
    with pytest.raises(Exception) as excinfo:
        get_pgn_output_filename(parsed_game, "foo/", "bar")
        expected_result = (
            "Parameter 'origin' must be 'chess.com' or 'lichess' got 'foo' instead."
        )
        assert excinfo.value
