"""
Functionality for analyzing PNG game data.
"""

import datetime
import glob

import pandas as pd

from chess_analyzer.core import parse_game_file


class AnalyzeGameSet:
    def __init__(self, df):
        self.df = df

    @property
    def best_win(self):
        return self.df[self.df.is_win].sort_values("elo_spread").iloc[0]

    @property
    def game_count(self):
        return len(self.df)

    @property
    def last_game(self):
        return self.df.sort_values("start_datetime").iloc[-1]

    @property
    def last_elo(self):
        return (
            self.last_game.whiteelo
            if self.last_game.is_white
            else self.last_game.blackelo
        )

    @property
    def loss_count(self):
        return len(self.df[~self.df.is_win])

    @property
    def opponent_list(self):
        return list(
            set([item.black if item.is_white else item.white for item in self.df.iloc])
        )

    @property
    def termination_modes(self):
        return self.df.termination_mode.value_counts()

    @property
    def total_gametime(self):
        return str(datetime.timedelta(seconds=int(self.df.gametime.sum())))

    @property
    def win_count(self):
        return len(self.df[self.df.is_win])


def load_games(src):
    """
    Takes a search string and returns a list of PNG string objects.

    Args:
        src (str): A search string that can be passed directly to
            ``glob.glob`` to return a list of files to open. e.g.
            ``data/*.pgn``.

    Returns:
        list: A list of string representations of the PGN files.
    """
    all_games = []
    filename_list = glob.glob(src)
    if len(filename_list) == 0:
        return None
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [f.read()]
    return all_games


def enrich_game_dataframe(df, username):
    """
    Adds additional metadata fields to a dataframe of PNG data.

    Adds the following fields to the input dataframe:

        - color (of the username)
        - ranking (of the username)
        - is_win (for the username)
        - termination_mode
        - whiteelo
        - blackelo
        - is_white
        - elo_spread
        - start_datetime
        - end_datetime

    Args:
        df (pandas.DataFrame): The dataframe of PGN game data.
        username (str): The username of the player we want to analyze.

    Returns:
        pandas.DataFrame: An enriched dataframe
    """
    df["color"] = ["white" if item == username else "black" for item in df.white]
    df["ranking"] = [
        item.whiteelo if item.white == username else item.blackelo for item in df.iloc
    ]
    df["ranking"] = df.ranking.astype(int)
    df["is_win"] = [True if username in item.termination else False for item in df.iloc]
    df["termination_mode"] = [item.split(" ")[-1] for item in df.termination.iloc]
    df["whiteelo"] = df.whiteelo.astype(int)
    df["blackelo"] = df.blackelo.astype(int)
    df["is_white"] = [item.white == username for item in df.iloc]
    df["elo_spread"] = [
        item.whiteelo - item.blackelo
        if item.is_white
        else item.blackelo - item.whiteelo
        for item in df.iloc
    ]
    df["start_datetime"] = [
        datetime.datetime.strptime(
            f"{item.utcdate} {item.utctime}", "%Y.%m.%d %H:%M:%S"
        )
        for item in df.iloc
    ]
    df["end_datetime"] = [
        datetime.datetime.strptime(
            f"{item.enddate} {item.endtime}", "%Y.%m.%d %H:%M:%S"
        )
        for item in df.iloc
    ]
    df["gametime"] = [
        (item.end_datetime - item.start_datetime).seconds for item in df.iloc
    ]
    df["parsed_game"] = [
        [parse_move(item.lstrip() + "]}") for item in df.iloc[0].game.split("]}")[:-1]]
    ]
    return df


def parse_move(move):
    """
    Parse a string representation of a game move into a dictionary.
    Note that this function only works for annotated games (games with
    metadata such as timestamps). Very early chess.com games will break
    this parser because they do not have this metadata.

    Args:
        move (str): The string representation of a move in algebraic
            notation with optional metadata.

    Returns:
        dict: A dictionary representation of the move.

    Examples:
      >>> parse_move("1. e4 {[%clk 0:00:59.9]}")
      {
        "turn": "1",
        "player": "white",
        "move": "e4",
        "meta": {"clk": "0:00:59.9"},
      }
    """
    output = {}
    move = move.split(" ")
    output["turn"] = move[0].strip(".")
    if "..." in move[0]:
        output["player"] = "black"
    else:
        output["player"] = "white"
    output["move"] = move[1]
    if move[2]:
        output["meta"] = {}
        output["meta"][move[2].strip("{[%")] = move[3].strip("]}")
    return output


def print_win_loss_report(analyze_game_set_object):
    print(f"Total Games: {analyze_game_set_object.game_count}")
    print(f"Total Game Time: {analyze_game_set_object.total_gametime}")
    print(
        f"Total Wins: {analyze_game_set_object.win_count} "
        f"({analyze_game_set_object.win_count / analyze_game_set_object.game_count * 100 :.0f}%)"
    )
    print(
        f"Total Losses: {analyze_game_set_object.loss_count} "
        f"({analyze_game_set_object.loss_count / analyze_game_set_object.game_count * 100 :.0f}%)"
    )
    last_game = analyze_game_set_object.last_game
    print(f"Latest ELO: {analyze_game_set_object.last_elo}" f" ({last_game.date})")
    best_win = analyze_game_set_object.best_win
    print(
        f"Best Win: {best_win.elo_spread} - {best_win.white} ({best_win.whiteelo}) vs "
        f"{best_win.black} ({best_win.blackelo}) "
        f"{best_win.result} "
    )


def analysis_main(src, username):
    raw_games = load_games(src)
    if raw_games is None:
        raise FileNotFoundError(f'No files match the search string "{src}"')
    parsed_games = [parse_game_file(item) for item in raw_games]
    df = pd.DataFrame(parsed_games)
    return enrich_game_dataframe(df, username)


def print_summary_report(src, username):
    game_dataframe = analysis_main(src=src, username=username)
    print(f"{len(game_dataframe)} games found in {src}")

    ags = AnalyzeGameSet(df=game_dataframe)
    opponent_df = pd.DataFrame(ags.opponent_list)
    repeat_opponent_df = opponent_df[0].value_counts()[
        opponent_df[0].value_counts() > 1
    ]
    print_win_loss_report(ags)
    print(f"Total Opponents: {len(set(ags.opponent_list))}")
    print(f"Repeat Opponents: {len(repeat_opponent_df)}")
    print("\n")

    print(f"By time control: ")
    for item in game_dataframe.timecontrol.value_counts().index:
        print("\n")
        print(f"Time Control: {item}s")
        print_win_loss_report(
            AnalyzeGameSet(df=game_dataframe[game_dataframe.timecontrol == item])
        )
