from chess_analyzer.download import split_bulk_file_download


def test_split_bulk_file_download():
    # with open("test/test_pgn_game_set.txt", "rb") as f:
    with open("test/test_test_test.txt", "r") as f:
        test_data = f.read()
    test_result = split_bulk_file_download(test_data)
    assert len(test_result) == 3
