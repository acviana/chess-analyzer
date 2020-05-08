import datetime
import json

import pandas as pd

from chess_analyzer.analysis import (
    AnalyzeGameSet,
    enrich_game_dataframe,
    parse_move,
)
from chess_analyzer.core import parse_game_file


def load_fixture():
    with open("test/test_game.pgn") as f:
        return f.read()


def load_expected_result():
    return {
        "black": "acviana",
        "blackelo": 699,
        "color": "black",
        "currentposition": "6k1/ppp2ppp/2n2n2/8/8/2Q5/PPP2PPP/3q2K1 w - -",
        "date": "2020.04.18",
        "eco": "D00",
        "ecourl": "https://www.chess.com/openings/Queens-Pawn-Opening-Blackmar-Diemer-Gambit-2...dxe4-3.Nc3-Nf6",
        "elo_spread": 75,
        "end_datetime": datetime.datetime(2020, 4, 18, 14, 29, 52),
        "enddate": "2020.04.18",
        "endtime": "14:29:52",
        "event": "Live Chess",
        "game": "1. d4 {[%clk 0:02:59.9]} 1... d5 {[%clk 0:02:59.2]} 2. Nc3 {[%clk 0:02:57.1]} 2... Nf6 {[%clk 0:02:55.7]} 3. e4 {[%clk 0:02:54]} 3... dxe4 {[%clk 0:02:52.7]} 4. Nge2 {[%clk 0:02:45.7]} 4... e6 {[%clk 0:02:28.9]} 5. Nf4 {[%clk 0:02:42.8]} 5... Bd6 {[%clk 0:02:22.8]} 6. Qe2 {[%clk 0:02:36.3]} 6... e5 {[%clk 0:02:17]} 7. Nfd5 {[%clk 0:02:30.5]} 7... exd4 {[%clk 0:02:11.1]} 8. Qxe4+ {[%clk 0:02:24.4]} 8... Be7 {[%clk 0:02:05.6]} 9. Qxd4 {[%clk 0:02:22.1]} 9... O-O {[%clk 0:02:01.8]} 10. Bg5 {[%clk 0:02:00.7]} 10... Be6 {[%clk 0:01:38.8]} 11. Rd1 {[%clk 0:01:52.2]} 11... Nc6 {[%clk 0:01:35]} 12. Qd3 {[%clk 0:01:31.7]} 12... Bxd5 {[%clk 0:01:06.7]} 13. Nxd5 {[%clk 0:01:28.6]} 13... Nxd5 {[%clk 0:00:54.2]} 14. Bxe7 {[%clk 0:01:23.9]} 14... Qxe7+ {[%clk 0:00:50.6]} 15. Be2 {[%clk 0:01:13.4]} 15... Nf6 {[%clk 0:00:47.3]} 16. O-O {[%clk 0:01:05.1]} 16... Rad8 {[%clk 0:00:43.9]} 17. Qh3 {[%clk 0:00:55.8]} 17... Qxe2 {[%clk 0:00:40.8]} 18. Rxd8 {[%clk 0:00:43.2]} 18... Rxd8 {[%clk 0:00:37.2]} 19. Qc3 {[%clk 0:00:08.7]} 19... Rd1 {[%clk 0:00:32.8]} 20. Rxd1 {[%clk 0:00:01.6]} 20... Qxd1+ {[%clk 0:00:31.5]} 0-1",
        "gametime": 339,
        "is_white": False,
        "is_win": True,
        "link": "https://www.chess.com/live/game/4738999062",
        "ranking": 699,
        "result": "0-1",
        "round": "-",
        "site": "Chess.com",
        "start_datetime": datetime.datetime(2020, 4, 18, 14, 24, 13),
        "starttime": "14:24:13",
        "termination": "acviana won on time",
        "termination_mode": "time",
        "timecontrol": "180",
        "timezone": "UTC",
        "utcdate": "2020.04.18",
        "utctime": "14:24:13",
        "white": "compadredoe",
        "whiteelo": 624,
    }


def test_enrich_game_dataframe():
    expected_result = load_expected_result()
    test_fixture = load_fixture()
    parsed_game = parse_game_file(test_fixture)
    df = pd.DataFrame([parsed_game])
    username = "acviana"
    enriched_game = enrich_game_dataframe(df=df, username=username)
    assert enriched_game.loc[0].to_dict() == expected_result


def test_analyze_game_set():
    # Not ideal that this is constructed from fake data but good enough
    # for now.
    input_data = [
        {
            "black": "player2",
            "blackelo": 1001,
            "elo_spread": 1,
            "gametime": 100,
            "is_white": True,
            "is_win": True,
            "start_datetime": datetime.datetime(2009, 9, 17, 21, 40, 19),
            "white": "player1",
            "whiteelo": 1000,
        },
        {
            "black": "player1",
            "blackelo": 1000,
            "elo_spread": 0,
            "gametime": 100,
            "is_white": False,
            "is_win": False,
            "start_datetime": datetime.datetime(2009, 9, 18, 21, 40, 19),
            "white": "player2",
            "whiteelo": 1000,
        },
    ]
    df = pd.DataFrame(input_data)
    game_set = AnalyzeGameSet(df=df)
    assert game_set.best_win.to_dict() == input_data[0]
    assert game_set.game_count == 2
    assert game_set.win_count == 1
    assert game_set.last_elo == 1000
    assert game_set.last_game.to_dict() == input_data[1]
    assert game_set.loss_count == 1
    assert game_set.total_gametime == str(
        datetime.timedelta(seconds=sum([item["gametime"] for item in input_data]))
    )
    assert game_set.opponent_list == ["player2"]


def test_parse_move():

    # Test an clock-annotated move for white
    expected_result = {
        "turn": "1",
        "player": "white",
        "move": "e4",
        "meta": {"clk": "0:00:59.9"},
    }
    assert parse_move("1. e4 {[%clk 0:00:59.9]}") == expected_result

    # Test a clock-annotated move for black
    expected_result = {
        "turn": "1",
        "player": "black",
        "move": "d5",
        "meta": {"clk": "0:02:59.2"}
    }
    assert parse_move("1... d5 {[%clk 0:02:59.2]}") == expected_result
