import glob

import pandas as pd

from chess_analyzer.core import parse_game_file


def load_games(src):
    all_games = []
    filename_list = glob.glob(src)
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [parse_game_file(f.read())]
    return all_games


def enrich_game_dataframe(df, username):
    df["color"] = ["white" if item == username else "black" for item in df.white]
    df["ranking"] = [
        item.whiteelo if item.white == username else item.blackelo for item in df.iloc
    ]
    df["ranking"] = df["ranking"].astype(int)
    df["is_win"] = [True if username in item.termination else False for item in df.iloc]
    df["termination_mode"] = [item.split(" ")[-1] for item in df.termination.iloc]
    # df["date"] = pd.to_datetime(df.date)
    # df["utcdate"] = pd.to_datetime(df.utcdate)
    return df


def main(src, username):
    all_games = load_games(src)
    df = pd.DataFrame(all_games)
    print(df.loc[0])
    return enrich_game_dataframe(df, username)


if __name__ == "__main__":
    src = "data/*.pgn"
    username = "acviana"
    game_data = main(src=src, username=username)
    print(f"{len(game_data)} games found in {src}")
    print(game_data.loc[0])
