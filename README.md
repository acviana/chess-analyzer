# chess-analyzer
A small chess analysis library optimized for chess.com data.

This package has two main functionalities. First, it uses the bulk download endpoint from the chess.com API to download and save any users games as PNG files. The second is to parse the game files into game play metrics. The metrics are calculated using a pandas data frame that can also be used as a data object for further analysis such as in a Jupyter notebook.

### Example CLI Usage

The CLI module allows you to either download chess.com games as PGN files or run a basic analysis on a set of PGN files.

```
$ chess-analyzer --help
Usage: chess-analyzer [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  analyze   Run a high-level report on a set of .pgn files.
  download  Download png files for a chess.com user over a date range.
```

Download png game files from chess.com API.

```
$ chess-analyzer --help
Usage: chess-analyzer [OPTIONS] USERNAME [%Y-%m] [[%Y-%m]]

  Download png files for a chess.com user over a date range.

  e.g. chess-analyzer USERNAME YYYY-MM YYYY-MM

Options:
  --help  Show this message and exit.

$ chess-analyzer acviana 2018-01 2020-05
Found 210 games from 2018-01 to 2020-05
```

Analyzing game files.

```
$ chess-analyzer analyze --help
Usage: chess-analyzer analyze [OPTIONS] USERNAME

  Run a high-level report on a set of .pgn files.

Options:
  --search-path TEXT
  --help              Show this message and exit.

$ chess-analyzer analyze acviana
197 games found in data/*.pgn
Total Games: 197
Total Wins: 102 (52%)
Total Losses: 95 (48%)
Latest ELO: 649 (2020.04.01)
Best Win: -126 - supersnorre (773) vs acviana (647) 0-1
Total Opponents: 190
Repeat Opponents: 7


By time control:


Time Control: 60s
Total Games: 169
Total Wins: 90 (53%)
Total Losses: 79 (47%)
Latest ELO: 649 (2020.04.01)
Best Win: -101 - jogi221 (708) vs acviana (607) 0-1


Time Control: 600s
Total Games: 17
Total Wins: 10 (59%)
Total Losses: 7 (41%)
Latest ELO: 1114 (2019.04.14)
Best Win: -37 - ShabanAli (1151) vs acviana (1114) 0-1


Time Control: 300s
Total Games: 7
Total Wins: 1 (14%)
Total Losses: 6 (86%)
Latest ELO: 924 (2019.07.04)
Best Win: 61 - jessejoe521 (888) vs acviana (949) 0-1

...
```
