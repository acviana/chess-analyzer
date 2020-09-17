from chess_analyzer.download_lichess import split_bulk_file_download


def test_split_bulk_file_download():
    with open("test/test_pgn_game_set_lichess.txt", "r") as f:
        test_data = f.read()
    test_result = split_bulk_file_download(test_data)
    assert len(test_result) == 3
