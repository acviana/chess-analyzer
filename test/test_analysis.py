import json

import pandas as pd

from chess_analyzer.analysis import enrich_game_dataframe
from chess_analyzer.core import parse_game_file


def load_fixture():
    with open("test/test_game.pgn") as f:
        return f.read()


def load_expected_result():
    with open("test/test_game_enriched.json") as f:
        return json.load(f)


def test_enrich_game_dataframe():
    expected_result = load_expected_result()
    test_fixture = load_fixture()
    parsed_game = parse_game_file(test_fixture)
    df = pd.DataFrame([parsed_game])
    username = "erik"
    enriched_game = enrich_game_dataframe(df=df, username=username)
    print(enriched_game.loc[0].to_dict())
    print(expected_result)
    assert enriched_game.loc[0].to_dict() == expected_result
