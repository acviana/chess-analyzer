from datetime import datetime

import requests


def download_files_in_date_range(username, start_date, end_date):
    game_file_buffer = ""
    for year in range(start_date.year, end_date.year + 1):
        for month in range(1, 12):
            response = query_bulk_games_endpoint(username, year, month)
            if response.status_code == 404:
                if response.json()["message"] == "Date cannot be set in the future":
                    return game_file_buffer
            if len(response.content) != 0:
                game_file_buffer += response.content.decode()


def query_bulk_games_endpoint(username, year, month):
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}/pgn"
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


def main(username, start_date, end_date):
    game_buffer = download_files_in_date_range(
        username=username, start_date=start_date, end_date=end_date
    )
    games_list = split_builk_file_download(game_buffer)
    for game in games_list:
        parsed_game = parse_game_file(game)
        filename = f"data/{parsed_game['link'].split('/')[-1]}.pgn"
        write_game_file(filename=filename, game_file=game)
    print(
        f"Found {len(games_list)} games from {datetime.strftime(start_date, '%Y-%m')} "
        f"to {datetime.strftime(end_date, '%Y-%m')}"
    )


if __name__ == "__main__":
    start_date = datetime.strptime("2018-01", "%Y-%m")
    end_date = datetime.strptime("2020-04", "%Y-%m")
    main(username="acviana", start_date=start_date, end_date=end_date)
