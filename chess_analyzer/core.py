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
            parsed_game[item[0:split].lower()] = item[split + 2 : -1]
    return parsed_game
