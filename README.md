# chess-analyzer
[![Build Status](https://travis-ci.com/acviana/chess-analyzer.svg?branch=master)](https://travis-ci.com/acviana/chess-analyzer) [![Documentation Status](https://readthedocs.org/projects/chess-analyzer/badge/?version=latest)](https://chess-analyzer.readthedocs.io/en/latest/?badge=latest)

A small chess analysis library optimized for chess.com data.

This package has two main functionalities. First, it uses the bulk download endpoint from the chess.com API to download and save any users games as PNG files. The second is to parse the game files into game play metrics. The metrics are calculated using a pandas data frame that can also be used as a data object for further analysis such as in a Jupyter notebook.

### Example Jupyter Notebook Usage

The core Pandas object from the analysis functionality can be loaded directly into a Jupyter notebook for additional analysis. The following script uses the Seaborn library to generate three histograms of the distribution of a player's ELO spread vs their opponents broken out by total games, wins, and losses.

```python
import pandas as pd
import seaborn as sns
from chess_analyzer.analysis import analysis_main

df = analysis_main(src="data/*.pgn", username="acviana")

sns.distplot(df.elo_spread)
sns.distplot(df[df.is_win].elo_spread)
sns.distplot(df[~df.is_win].elo_spread)

```

![example analysis histogram](https://dl.dropboxusercontent.com/s/w7n6cafk11ailbm/chess-analyzer-example-histo.png "Logo Title Text 1")

### Example CLI Usage

The CLI module allows you to either download chess.com games as PGN files or run a basic analysis on a set of PGN files. All commands contain a `--help` flag with additional information.

Download png game files from chess.com API.

```
$ chess-analyzer acviana 2018-01 2020-05
Found 210 games from 2018-01 to 2020-05
```

Run a basic report against a set of PNG game files.

```
$ chess-analyzer analyze acviana
260 games found in data/*.pgn
Total Games: 260
Total Game Time: 12:28:43
Total Wins: 126 (48%)
Total Losses: 134 (52%)
Latest ELO: 793 (2020.04.12)
Best Win: -126 - supersnorre (773) vs acviana (647) 0-1
Total Opponents: 247
Repeat Opponents: 12


By time control:


Time Control: 60s
Total Games: 220
Total Game Time: 6:57:29
Total Wins: 110 (50%)
Total Losses: 110 (50%)
Latest ELO: 558 (2020.04.12)
Best Win: -101 - Zendinih (696) vs acviana (595) 0-1


Time Control: 600s
Total Games: 17
Total Game Time: 3:24:53
Total Wins: 10 (59%)
Total Losses: 7 (41%)
Latest ELO: 1114 (2019.04.14)
Best Win: -37 - ShabanAli (1151) vs acviana (1114) 0-1


Time Control: 180s
Total Games: 15
Total Game Time: 1:13:20
Total Wins: 4 (27%)
Total Losses: 11 (73%)
Latest ELO: 793 (2020.04.12)
Best Win: 1 - acviana (866) vs Pharells (865) 1-0

...
```
