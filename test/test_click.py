import os
from unittest import mock

from click.testing import CliRunner

from chess_analyzer.click import (
    analyze,
    download,
    download_main,
    print_summary_report,
)


@mock.patch("chess_analyzer.click.download_main")
def test_download_cli(mock_download):
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("data")
        result = runner.invoke(download, ["username", "2020-01", "2020-08"], ".")
        assert result.exit_code == 0

        # Crash one just for fun
        result = runner.invoke(download, [], ".")
        assert result.exit_code == 2


@mock.patch("chess_analyzer.click.print_summary_report")
def test_analyze_cli(mock_print_summary_report):
    runner = CliRunner()
    result = runner.invoke(analyze, "usename", "search_path")
    assert result.exit_code == 0
