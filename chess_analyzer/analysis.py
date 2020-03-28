import glob

from download import parse_game_file


def load_games():
    all_games = []
    filename_list = glob.glob("data/*.pgn")
    for filename in filename_list:
        with open(filename, "r") as f:
            all_games += [parse_game_file(f.read())]
    return all_games


def main():
    all_games = load_games()


if __name__ == "__main__":
    main()
