from datetime import datetime
import glob

import pandas as pd

from chess_analyzer.core import parse_game_file


def load_games(src):
    all_games = []
    filename_list = glob.glob(src)
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [f.read()]
    return all_games


def enrich_game_dataframe(df, username):
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
        datetime.strptime(f"{item.utcdate} {item.utctime}", "%Y.%m.%d %H:%M:%S")
        for item in df.iloc
    ]
    df["end_datetime"] = [
        datetime.strptime(f"{item.enddate} {item.endtime}", "%Y.%m.%d %H:%M:%S")
        for item in df.iloc
    ]
    df["gametime"] = [
        (item.end_datetime - item.start_datetime).seconds for item in df.iloc
    ]
    return df


def main(src, username):
    raw_games = load_games(src)
    parsed_games = [parse_game_file(item) for item in raw_games]
    df = pd.DataFrame(parsed_games)
    return enrich_game_dataframe(df, username)


if __name__ == "__main__":
    src = "data/*.pgn"
    username = "acviana"
    game_data = main(src=src, username=username)
    print(f"{len(game_data)} games found in {src}")
    print(game_data.loc[0])
