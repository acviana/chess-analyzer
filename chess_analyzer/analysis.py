import glob

import pandas as pd

from chess_analyzer.core import parse_game_file


def load_games():
    all_games = []
    filename_list = glob.glob("data/*.pgn")
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [parse_game_file(f.read())]
    return all_games


def main():
    all_games = load_games()
    return pd.DataFrame(all_games)


if __name__ == "__main__":
    game_data = main()
    print(game_data.loc[0])
