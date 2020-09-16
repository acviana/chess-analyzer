from datetime import (
    datetime,
    timedelta,
)
import re

import responses

from chess_analyzer.download_chess_dot_com import (
    split_bulk_file_download,
    download_files_in_date_range,
)


@responses.activate
def test_download_files_in_date_range():
    username = "username"
    responses.add(responses.GET, url=re.compile(r"https://api.chess.com/\S*"), body="1")

    # Test a 1 month range
    start_datetime = datetime.strptime("2020-02", "%Y-%m")
    end_datetime = datetime.strptime("2020-02", "%Y-%m")
    test_result = download_files_in_date_range(
        username=username, start_datetime=start_datetime, end_datetime=end_datetime
    )
    assert test_result == "1"

    # Test a 3 month range
    start_datetime = datetime.strptime("2020-01", "%Y-%m")
    end_datetime = datetime.strptime("2020-03", "%Y-%m")
    test_result = download_files_in_date_range(
        username=username, start_datetime=start_datetime, end_datetime=end_datetime
    )
    assert test_result == "1" * 3

    # Test a 1 month range
    start_datetime = datetime.strptime("2019-02", "%Y-%m")
    end_datetime = datetime.strptime("2020-02", "%Y-%m")
    test_result = download_files_in_date_range(
        username=username, start_datetime=start_datetime, end_datetime=end_datetime
    )
    assert test_result == "1" * 13

    # Test a 3 month range with one month in the future which should
    # only run two queries. Going +/- 32 days ensures you will always
    # be +/- 1 month becuause no month has 32 days.
    start_datetime = datetime.today() - timedelta(days=32)
    end_datetime = datetime.today() + timedelta(days=32)
    test_result = download_files_in_date_range(
        username=username, start_datetime=start_datetime, end_datetime=end_datetime
    )
    assert test_result == "1" * 2


def test_split_bulk_file_download():
    with open("test/test_pgn_game_set_chess_dot_com.txt", "r") as f:
        test_data = f.read()
    test_result = split_bulk_file_download(test_data)
    assert len(test_result) == 3
