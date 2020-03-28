import requests


def query_bulk_games_endpoint(username, year, month):
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}/pgn"
    # return url
    return requests.get(
        url=url,
        headers={
            "Content-Type": "application/x-chess-pgn",
            "Content-Disposition": 'attachment; filename="ChessCom_username_YYYYMM.pgn"',
        },
    )


def split_builk_file_download(bulk_file_download):
    games_list = bulk_file_download.split("\n\n[Event")
    games_list = ["[Event" + item for item in games_list]
    return games_list


def write_game_file(filename, game_file):
    with open(filename, "w") as f:
        f.write(game_file)


def parse_game_file(game_file):
    parsed_game = {}
    for item in game_file.split("\n"):
        if item == "":
            continue
        if item[0:2] == "1.":
            parsed_game["game"] = item
        else:
            item = item[1:-1]
            split = item.find(" ")
            parsed_game[item[0:split].lower()] = item[split + 1 : -1]
    return parsed_game


def main():
    for year in [2018, 2019, 2020]:
        for month in range(1, 12):
            response = query_bulk_games_endpoint("acviana", year, month)
            if response.status_code == 404:
                if response.json()["message"] == "Date cannot be set in the future":
                    return
            if len(response.content) != 0:
                games_list = split_builk_file_download(
                    bulk_file_download=response.content.decode()
                )
                for game in games_list:
                    parsed_game = parse_game_file(game)
                    filename = f"data/{parsed_game['link'].split('/')[-1]}.pgn"
                    write_game_file(filename=filename, game_file=game)
            else:
                games_list = []
            print(f"Queried: {year}-{month} found {len(games_list)} games")


if __name__ == "__main__":
    main()
